import json
import math
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast
from torch.optim import AdamW
import torch.nn.functional as F

# ---------- Custom Output Class -----------
class QuestionAnsweringModelOutput:
    def __init__(self, loss=None, start_logits=None, end_logits=None, hidden_states=None, attentions=None, reasoning_logits=None):
        self.loss = loss
        self.start_logits = start_logits
        self.end_logits = end_logits
        self.hidden_states = hidden_states
        self.attentions = attentions
        self.reasoning_logits = reasoning_logits

# ---------- Custom BERT Implementation ----------
class BertConfigCustom:
    def __init__(self,
                 vocab_size=30522,
                 hidden_size=768,
                 num_hidden_layers=12,
                 num_attention_heads=12,
                 intermediate_size=3072,
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 max_position_embeddings=512,
                 type_vocab_size=2,
                 reasoning_vocab_size=3):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.reasoning_vocab_size = reasoning_vocab_size

class BertEmbeddings(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
        self.token_type_embeddings = nn.Embedding(config.type_vocab_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, input_ids, token_type_ids=None):
        seq_length = input_ids.size(1)
        position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device)
        position_ids = position_ids.unsqueeze(0).expand_as(input_ids)
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        words = self.word_embeddings(input_ids)
        positions = self.position_embeddings(position_ids)
        device = self.token_type_embeddings.weight.device
        token_type_ids = token_type_ids.to(device)
        types = self.token_type_embeddings(token_type_ids)

        embeddings = words + positions + types
        embeddings = self.LayerNorm(embeddings)
        return self.dropout(embeddings)

class BertSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        if config.hidden_size % config.num_attention_heads != 0:
            raise ValueError("Hidden size must be divisible by number of heads")
        self.num_heads = config.num_attention_heads
        self.head_dim = config.hidden_size // self.num_heads

        # Query (Q) – represents what this token is looking for.
        # Key (K) – represents what this token contains.
        # Value (V) – represents the actual content or information of the token.
        self.query = nn.Linear(config.hidden_size, config.hidden_size)
        self.key   = nn.Linear(config.hidden_size, config.hidden_size)
        self.value = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)

    def forward(self, hidden_states, attention_mask=None):
        batch_size, seq_len, _ = hidden_states.size()
        def transpose(x):
            return x.view(batch_size, seq_len, self.num_heads, self.head_dim) \
                    .permute(0, 2, 1, 3)

        Q = transpose(self.query(hidden_states))
        K = transpose(self.key(hidden_states))
        V = transpose(self.value(hidden_states))

        scores = torch.matmul(Q, K.transpose(-1, -2))
        scores = scores / math.sqrt(self.head_dim)
        if attention_mask is not None:
            scores = scores + attention_mask
        probs = torch.softmax(scores, dim=-1)
        probs = self.dropout(probs)

        context = torch.matmul(probs, V)
        context = context.permute(0, 2, 1, 3).contiguous()
        return context.view(batch_size, seq_len, -1)

class BertSelfOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden = self.dense(hidden_states)
        hidden = self.dropout(hidden)
        return self.LayerNorm(hidden + input_tensor)

class BertAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.self = BertSelfAttention(config)
        self.output = BertSelfOutput(config)

    def forward(self, hidden_states, attention_mask=None):
        self_output = self.self(hidden_states, attention_mask)
        return self.output(self_output, hidden_states)

class BertIntermediate(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
        self.intermediate_act_fn = nn.GELU()

    def forward(self, hidden_states):
        return self.intermediate_act_fn(self.dense(hidden_states))

class BertOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self, hidden_states, input_tensor):
        hidden = self.dense(hidden_states)
        hidden = self.dropout(hidden)
        return self.LayerNorm(hidden + input_tensor)

class BertLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = BertAttention(config)
        self.intermediate = BertIntermediate(config)
        self.output = BertOutput(config)

    def forward(self, hidden_states, attention_mask=None):
        attention_output = self.attention(hidden_states, attention_mask)
        intermediate_output = self.intermediate(attention_output)
        return self.output(intermediate_output, attention_output)

class BertEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.layers = nn.ModuleList([BertLayer(config) for _ in range(config.num_hidden_layers)])

    def forward(self, hidden_states, attention_mask=None):
        all_hidden = []
        for layer in self.layers:
            hidden_states = layer(hidden_states, attention_mask)
            all_hidden.append(hidden_states)
        return hidden_states, all_hidden

class BertPooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states):
        cls_token = hidden_states[:, 0]
        return self.activation(self.dense(cls_token))

# Placeholder for full BertModelCustom implementation
class BertModelCustom(nn.Module):
    def __init__(self, config: BertConfigCustom):
        super().__init__()
        self.config = config
        self.embeddings = BertEmbeddings(config)
        self.encoder = BertEncoder(config)
        self.pooler = BertPooler(config)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        if attention_mask is not None:
            extended_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            extended_mask = (1.0 - extended_mask) * -10000.0
        else:
            extended_mask = None

        emb = self.embeddings(input_ids, token_type_ids)
        seq_out, all_hidden = self.encoder(emb, extended_mask)
        pooled = self.pooler(seq_out)
        return seq_out, pooled, all_hidden

# ---------- QA Head with Reasoning ----------
class BertForQuestionAnsweringWithReasoning(nn.Module):
    def __init__(self, config: BertConfigCustom):
        super().__init__()
        self.bert = BertModelCustom(config)
        self.qa_outputs = nn.Linear(config.hidden_size, 2)
        self.reasoning_output = nn.Linear(config.hidden_size, config.reasoning_vocab_size)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None,
                start_positions=None, end_positions=None, reasoning_labels=None):
        seq_out, pooled, _ = self.bert(input_ids, attention_mask, token_type_ids)
        logits = self.qa_outputs(seq_out)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        reasoning_logits = self.reasoning_output(pooled)

        loss = None
        if start_positions is not None and end_positions is not None:
            loss_fct = nn.CrossEntropyLoss()
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            loss = (start_loss + end_loss) / 2
            if reasoning_labels is not None:
                reason_loss = loss_fct(reasoning_logits, reasoning_labels)
                loss = loss + reason_loss

        return QuestionAnsweringModelOutput(
            loss=loss,
            start_logits=start_logits,
            end_logits=end_logits,
            hidden_states=None,
            attentions=None,
            reasoning_logits=reasoning_logits
        )

# ---------- Dataset with Reasoning ----------
class QADatasetWithReasoning(Dataset):
    def __init__(self, data, tokenizer: BertTokenizerFast, reasoning_vocab, max_length=256):
        self.data = data
        self.tokenizer = tokenizer
        self.reasoning_vocab = reasoning_vocab
        self.max_length = max_length

    def __len__(self): return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        context = item['context']
        question = item['question']
        answer = item['answers']['text'][0]
        start_char = item['answers']['answer_start'][0]
        end_char = start_char + len(answer)
        reasoning_label = self.reasoning_vocab.get(item.get('reasoning_label', 'factual'), 0)

        enc = self.tokenizer(
            question, context,
            truncation='only_second',
            max_length=self.max_length,
            return_offsets_mapping=True,
            padding='max_length',
            return_tensors='pt'
        )
        offsets = enc.pop('offset_mapping')[0]
        input_ids = enc['input_ids'].squeeze(0)
        attention_mask = enc['attention_mask'].squeeze(0)
        token_type_ids = enc.get('token_type_ids', None)
        if token_type_ids is not None: token_type_ids = token_type_ids.squeeze(0)

        start_pos = end_pos = 0
        for i, (s, e) in enumerate(offsets.tolist()):
            if s <= start_char < e: start_pos = i
            if s < end_char <= e:
                end_pos = i
                break

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'token_type_ids': token_type_ids,
            'start_positions': torch.tensor(start_pos),
            'end_positions': torch.tensor(end_pos),
            'reasoning_labels': torch.tensor(reasoning_label)
        }

# ---------- Inference with Retrieval ----------
CONTEXTS = []
CONTEXT_EMB = None

def build_context_embeddings(model, tokenizer, contexts, device):
    model.eval()
    embs = []
    for ctx in contexts:
        enc = tokenizer(ctx, return_tensors='pt', truncation=True, padding=True, max_length=256).to(device)
        with torch.no_grad():
            _, pooled, _ = model.bert(enc['input_ids'], enc['attention_mask'], enc.get('token_type_ids', None))
        embs.append(pooled.squeeze(0))
    return torch.stack(embs)  # (num_ctx, hidden_size)


def evaluate(question, model, tokenizer, device):
    # Compute question embedding
    enc = tokenizer(question, return_tensors='pt', truncation=True, padding=True, max_length=256).to(device)
    with torch.no_grad():
        _, q_emb, _ = model.bert(enc['input_ids'], enc['attention_mask'], enc.get('token_type_ids', None))
    q_emb = q_emb.squeeze(0)  # (hidden_size)

    # Compute similarities and select best context
    sims = nn.functional.cosine_similarity(q_emb.unsqueeze(0), CONTEXT_EMB, dim=1) # pylint: disable=not-callable
    best_idx = torch.argmax(sims).item()
    context = CONTEXTS[best_idx]

    # Perform QA on selected context
    enc2 = tokenizer(question, context, return_tensors='pt', truncation=True, padding=True, max_length=256).to(device)
    outputs = model(enc2['input_ids'], enc2['attention_mask'], enc2.get('token_type_ids', None))
    start = torch.argmax(outputs.start_logits, dim=1).item()
    end = torch.argmax(outputs.end_logits, dim=1).item() + 1
    answer = tokenizer.decode(enc2['input_ids'][0][start:end])
    return answer, best_idx

# ---------- Main for Document QA with Reasoning ----------
if __name__ == '__main__':
    import fitz
    from nltk.tokenize import sent_tokenize

    # 1. Extract passages
    doc = fitz.open('Alice_in_Wonderland.pdf')
    text = ''.join([p.get_text() for p in doc])
    sentences = sent_tokenize(text)
    CONTEXTS = [' '.join(sentences[i:i+5]) for i in range(0, len(sentences), 5)]

    # 2. Generate QA examples and save
    qa_examples = []
    for i, p in enumerate(CONTEXTS[:10]):
        question = f"What is the main idea in passage {i}?"
        answer = sentences[i*5] if i*5 < len(sentences) else ''
        start_idx = p.find(answer)
        qa_examples.append({
            'context': p,
            'question': question,
            'answers': {'text': [answer], 'answer_start': [start_idx]},
            'reasoning_label': 'factual'
        })
    with open('alice_qa.json', 'w') as f:
        json.dump(qa_examples, f, indent=2)

    # 3. Prepare dataset
    vocab = {'factual': 0, 'causal': 1, 'comparative': 2}
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    dataset = QADatasetWithReasoning(qa_examples, tokenizer, vocab)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    # 4. Initialize model and context embeddings
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    config = BertConfigCustom(reasoning_vocab_size=len(vocab))
    model = BertForQuestionAnsweringWithReasoning(config).to(device)
    CONTEXT_EMB = build_context_embeddings(model, tokenizer, CONTEXTS, device)
    optimizer = AdamW(model.parameters(), lr=3e-5)

    # 5. Train
    for epoch in range(2):
        model.train()
        total_loss = 0
        for batch in loader:
            optimizer.zero_grad()
            out = model(batch['input_ids'].to(device), batch['attention_mask'].to(device), None,
                        batch['start_positions'].to(device), batch['end_positions'].to(device),
                        batch['reasoning_labels'].to(device))
            out.loss.backward()
            optimizer.step()
            total_loss += out.loss.item()
        print(f'Epoch {epoch+1} Loss: {total_loss/len(loader):.4f}')

    # 6. Inference automatic retrieval
    question = "Why did villagers come to the well?"
    answer, idx = evaluate(question, model, tokenizer, device)
    print(f"Selected passage idx: {idx}\nAnswer: {answer}")

# ---------- End of Code ----------
