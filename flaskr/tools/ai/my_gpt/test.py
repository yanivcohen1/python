import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as L
from torch.optim import Adam
import tiktoken

class PositionEncoding(nn.Module):
    def __init__(self, d_model=256, max_len=1024):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).float().unsqueeze(1)
        div_term = torch.exp(-torch.arange(0, d_model, 2).float() * (torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, word_embeddings):
        # Supports inputs of shape (seq_len, d_model) or (batch, seq_len, d_model)
        if word_embeddings.dim() == 2:
            seq_len, d = word_embeddings.size()
            return word_embeddings + self.pe[:seq_len, :d]
        elif word_embeddings.dim() == 3:
            b, seq_len, d = word_embeddings.size()
            pe = self.pe[:seq_len, :d].unsqueeze(0)  # (1, seq_len, d)
            return word_embeddings + pe
        else:
            raise ValueError(f"Unsupported embedding tensor shape: {word_embeddings.shape}")

class Attention(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)

    def forward(self, q_emb, k_emb, v_emb, mask=None):
        q = self.W_q(q_emb)
        k = self.W_k(k_emb)
        v = self.W_v(v_emb)
        scores = torch.matmul(q, k.transpose(-2, -1)) / (k.size(-1) ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        return torch.matmul(weights, v)

class DecoderOnlyTransformer(L.LightningModule):
    def __init__(self, vocab_size, d_model=256, max_len=1024):
        super().__init__()
        self.save_hyperparameters()
        self.we = nn.Embedding(vocab_size, d_model)
        self.pe = PositionEncoding(d_model, max_len)
        self.attn = Attention(d_model)
        self.fc = nn.Linear(d_model, vocab_size)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, token_ids):
        # token_ids: (batch, seq_len) or (seq_len,)
        emb = self.we(token_ids)
        emb_pe = self.pe(emb)
        if emb_pe.dim() == 2:
            seq_len = emb_pe.size(0)
            mask = torch.tril(torch.ones(seq_len, seq_len, device=emb_pe.device)).logical_not()
        else:
            b, seq_len, _ = emb_pe.size()
            mask = torch.tril(torch.ones(seq_len, seq_len, device=emb_pe.device)).logical_not()
            mask = mask.unsqueeze(0).expand(b, seq_len, seq_len)
        attn_out = self.attn(emb_pe, emb_pe, emb_pe, mask)
        logits = self.fc(attn_out + emb_pe)
        return logits

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=1e-4)

    def training_step(self, batch, batch_idx):
        input_ids, target_ids = batch  # both (batch, seq_len)
        logits = self.forward(input_ids)
        b, seq_len, vocab = logits.size()
        loss = self.loss_fn(logits.view(b * seq_len, vocab), target_ids.view(-1))
        self.log('train_loss', loss)
        return loss

    def generate(self, input_ids, max_new_tokens=50):
        self.eval()
        if input_ids.dim() == 1:
            generated = input_ids.unsqueeze(0).to(self.device)
        else:
            generated = input_ids.to(self.device)
        for _ in range(max_new_tokens):
            logits = self.forward(generated)  # (b, seq, vocab)
            next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)  # (b, 1)
            generated = torch.cat([generated, next_token], dim=1)
        return generated

# Load JSON-formatted QA data and tokenize using GPT-2 BPE
def load_qa_data(file_path, encoder, seq_len):
    inputs, targets = [], []
    pad_id = encoder.eot_token_id if hasattr(encoder, 'eot_token_id') else encoder.encode('\n')[0]
    with open(file_path, 'r') as f:
        data = json.load(f)
    for item in data:
        context_ids = encoder.encode(item['context'])
        question_ids = encoder.encode(item['question'])
        answer_ids = encoder.encode(item['answers'])
        tokens = context_ids + question_ids + answer_ids
        # pad or truncate to seq_len+1
        if len(tokens) < seq_len + 1:
            tokens += [pad_id] * (seq_len + 1 - len(tokens))
        tokens = tokens[:seq_len + 1]
        inp = torch.tensor(tokens[:seq_len])
        tgt = torch.tensor(tokens[1:seq_len+1])
        inputs.append(inp)
        targets.append(tgt)
    return inputs, targets


def main():
    from torch.utils.data import DataLoader, TensorDataset

    # Hyperparameters
    seq_len = 512
    d_model = 256
    max_len = seq_len + 50
    batch_size = 4
    epochs = 3
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = current_dir + '/datasets/resonning.json'

    # GPT-2 BPE encoder
    encoder = tiktoken.get_encoding("gpt2")
    vocab_size = encoder.n_vocab

    # Prepare data
    inputs, targets = load_qa_data(data_file, encoder, seq_len)
    dataset = TensorDataset(torch.stack(inputs), torch.stack(targets))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Model
    model = DecoderOnlyTransformer(vocab_size=vocab_size, d_model=d_model, max_len=max_len)

    # Trainer
    trainer = L.Trainer(max_epochs=epochs)
    trainer.fit(model, loader)

    # Example generation on first sample
    sample_input = inputs[0]
    out_ids = model.generate(sample_input, max_new_tokens=20).squeeze(0)
    text_out = encoder.decode(out_ids.tolist())
    print("Generated QA:", text_out)

if __name__ == '__main__':
    main()
