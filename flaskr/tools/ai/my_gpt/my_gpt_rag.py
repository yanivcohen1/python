import json
import math
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast
from torch.optim import AdamW

# ---------- Custom Output Class ----------
class QuestionAnsweringModelOutput:
    def __init__(self, loss=None, start_logits=None, end_logits=None, hidden_states=None, attentions=None, reasoning_logits=None):
        self.reasoning_logits = reasoning_logits
        self.loss = loss
        self.start_logits = start_logits
        self.end_logits = end_logits
        self.hidden_states = hidden_states
        self.attentions = attentions

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
        self.reasoning_vocab_size = reasoning_vocab_size
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size

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

class QADataset(Dataset):
    """
    Dataset wrapper for SQuAD-style QA data.
    Expects data as a list of dicts: {"context": ..., "question": ..., "answers": {...}}
    """
    def __init__(self, data, tokenizer, max_length=384, doc_stride=128):
        self.examples = []
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.doc_stride = doc_stride

        for entry in data:
            inputs = tokenizer(
                entry['question'], entry['context'],
                truncation="only_second",
                max_length=self.max_length,
                stride=self.doc_stride,
                return_overflowing_tokens=True,
                return_offsets_mapping=True,
                padding="max_length"
            )
            for i, offset in enumerate(inputs['offset_mapping']):
                sample = {
                    'input_ids': torch.tensor(inputs['input_ids'][i]),
                    'attention_mask': torch.tensor(inputs['attention_mask'][i]),
                }
                answer = entry['answers']['text'][0]
                start_char = entry['answers']['answer_start'][0]
                end_char = start_char + len(answer)

                sequence_ids = inputs.sequence_ids(i)
                token_start = 0
                while sequence_ids[token_start] != 1:
                    token_start += 1
                token_end = len(inputs['input_ids'][i]) - 1
                while sequence_ids[token_end] != 1:
                    token_end -= 1

                if not (offset[token_start][0] <= start_char and offset[token_end][1] >= end_char):
                    sample['start_positions'] = torch.tensor(0)
                    sample['end_positions'] = torch.tensor(0)
                else:
                    while token_start < len(offset) and offset[token_start][0] <= start_char:
                        token_start += 1
                    sample['start_positions'] = torch.tensor(token_start - 1)
                    while token_end >= 0 and offset[token_end][1] >= end_char:
                        token_end -= 1
                    sample['end_positions'] = torch.tensor(token_end + 1)

                self.examples.append(sample)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]

class BertForQuestionAnsweringCustom(nn.Module):
    def __init__(self, config: BertConfigCustom):
        super().__init__()
        self.bert = BertModelCustom(config)
        hidden_size = config.hidden_size
        self.qa_outputs = nn.Linear(hidden_size, 2)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)

    def forward(self,
                input_ids=None,
                attention_mask=None,
                token_type_ids=None,
                start_positions=None,
                end_positions=None):
        seq_out, _, _ = self.bert(input_ids, attention_mask, token_type_ids)
        sequence_output = self.dropout(seq_out)
        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits   = end_logits.squeeze(-1)

        loss = None
        if start_positions is not None and end_positions is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss_start = loss_fct(start_logits, start_positions)
            loss_end   = loss_fct(end_logits,   end_positions)
            loss = (loss_start + loss_end) / 2

        return QuestionAnsweringModelOutput(
            loss=loss,
            start_logits=start_logits,
            end_logits=end_logits,
            hidden_states=None,
            attentions=None
        )

# ---------- Training & Evaluation Continued ----------
def train(model, dataloader, optimizer, device):
    model.train()
    total_loss = 0
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        start_positions = batch['start_positions'].to(device)
        end_positions = batch['end_positions'].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            start_positions=start_positions,
            end_positions=end_positions
        )
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(dataloader)

def evaluate(model, tokenizer, question, context, device):
    model.eval()
    inputs = tokenizer(
        question,
        context,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=384
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    token_type_ids = inputs.get('token_type_ids', None)
    if token_type_ids is not None:
        token_type_ids = token_type_ids.to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask, token_type_ids)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        start = torch.argmax(start_logits, dim=1).item()
        end = torch.argmax(end_logits, dim=1).item() + 1
        answer = tokenizer.decode(input_ids[0][start:end])
    return answer

# ---------- Chain-of-Thought Reasoning Modification ----------
class BertForQuestionAnsweringWithReasoning(nn.Module):
    def __init__(self, config):
        super(BertForQuestionAnsweringWithReasoning, self).__init__()
        self.bert = BertModelCustom(config)  # Replaced with custom model
        self.qa_outputs = nn.Linear(config.hidden_size, 2)
        self.reasoning_output = nn.Linear(config.hidden_size, config.reasoning_vocab_size)

    def forward(self, input_ids, attention_mask=None, token_type_ids=None,
                start_positions=None, end_positions=None, reasoning_labels=None):
        outputs = self.bert(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        sequence_output = outputs[0]
        hidden_states = outputs[1] if len(outputs) > 1 else None
        attentions = outputs[2] if len(outputs) > 2 else None

        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)

        # Reasoning prediction (optional label)
        reasoning_logits = self.reasoning_output(sequence_output[:, 0])  # Use [CLS] token

        total_loss = None
        if start_positions is not None and end_positions is not None:
            loss_fct = nn.CrossEntropyLoss()
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            total_loss = (start_loss + end_loss) / 2

            if reasoning_labels is not None:
                reasoning_loss = loss_fct(reasoning_logits, reasoning_labels)
                total_loss += reasoning_loss

        return QuestionAnsweringModelOutput(
            loss=total_loss,
            start_logits=start_logits,
            end_logits=end_logits,
            hidden_states=hidden_states,
            attentions=attentions,
            reasoning_logits=reasoning_logits
        )

# ---------- Dataset Class with Reasoning Support ----------
# from torch.utils.data import Dataset
class QADatasetWithReasoning(Dataset):
    def __init__(self, data, tokenizer, reasoning_vocab, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.reasoning_vocab = reasoning_vocab
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        context = item['context']
        question = item['question']
        answer = item['answers']['text'][0]
        start_char = item['answers']['answer_start'][0]
        end_char = start_char + len(answer)
        reasoning_label = self.reasoning_vocab.get(item.get('reasoning_label', 'factual'), 0)

        encoding = self.tokenizer(
            question,
            context,
            truncation="only_second",
            max_length=self.max_length,
            stride=128,
            return_overflowing_tokens=False,
            return_offsets_mapping=True,
            padding="max_length",
            return_tensors="pt"
        )

        offset_mapping = encoding.pop("offset_mapping")[0]
        input_ids = encoding["input_ids"][0]
        start_positions = end_positions = 0

        for i, (start, end) in enumerate(offset_mapping):
            if start <= start_char < end:
                start_positions = i
            if start < end_char <= end:
                end_positions = i
                break

        encoding = {k: v.squeeze(0) for k, v in encoding.items()}
        encoding["start_positions"] = torch.tensor(start_positions)
        encoding["end_positions"] = torch.tensor(end_positions)
        encoding["reasoning_labels"] = torch.tensor(reasoning_label)

        return encoding

# ---------- Sample Reasoning Data Entry ----------
# Add to train_data.json
# {
#   "context": "Alan Turing created the Turing Machine. The Turing Machine inspired computer science.",
#   "question": "Why is Alan Turing important in computer science?",
#   "answers": {"text": ["The Turing Machine inspired computer science"], "answer_start": [41]},
#   "reasoning_label": "causal"
# }

# Reasoning types example:
# "reasoning_vocab_size": 3
# 0 = factual, 1 = causal, 2 = comparative

# You would need to encode these reasoning types numerically when building your dataset.
# ---------- Entry Point ----------
if __name__ == "__main__":
    import os
    import random
    from tqdm import tqdm

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Load data
    with open(current_dir + "/datasets/train_resening_data.json") as f:
        data = json.load(f)

    # Tokenizer and Config
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    config = BertConfigCustom()

    # Dataset and DataLoader
    dataset = QADataset(data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # Model and Optimizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BertForQuestionAnsweringWithReasoning(config).to(device)
    optimizer = AdamW(model.parameters(), lr=3e-5)

    # Train
    for epoch in range(20):
        loss = train(model, dataloader, optimizer, device)
        print(f"Epoch {epoch+1}: loss = {loss:.4f}")

    # Save model
    # os.makedirs("models/qa_model", exist_ok=True)
    torch.save(model.state_dict(), current_dir + "/models/gpt_resening_model.pth")
    tokenizer.save_pretrained(current_dir + "/models/qa_model")


    # Example of reasoning
    question = "Where is the Eiffel Tower?"
    context = "The Eiffel Tower is in Paris. It is one of the most visited landmarks in the world."
    answer = evaluate(model, tokenizer, question, context, device)
    print(f"Q: {question}\nA: {answer} \n\n")

    # Example of reasoning
    question = "Where is the most visited landmarks in the world?"
    context = "The Eiffel Tower is in Paris. It is one of the most visited landmarks in the world."
    answer = evaluate(model, tokenizer, question, context, device)
    print(f"Q: {question}\nA: {answer}")
