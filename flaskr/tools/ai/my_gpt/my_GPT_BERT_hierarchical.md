https://aainabajaj39.medium.com/the-journey-from-vanilla-neural-network-to-bert-architecture-nlu-572e280a94b4
https://www.youtube.com/watch?v=t45S_MwAcOw

## My GPT hierarchical breakdown of the blocks of google BERT (Bidirectional Encoder Representations from Transformer):

```
BertForQuestionAnsweringWithReasoning
├── bert: BertModelCustom
│   ├── embeddings: BertEmbeddings
│   │   ├── word_embeddings: Embedding
│   │   ├── position_embeddings: Embedding
│   │   ├── token_type_embeddings: Embedding
│   │   ├── LayerNorm: LayerNorm
│   │   └── dropout: Dropout
│   ├── encoder: BertEncoder
│   │   └── layers: ModuleList [12 x BertLayer]
│   │       └── BertLayer (repeated 12 times)
│   │           ├── attention: BertAttention
│   │           │   ├── self: BertSelfAttention
│   │           │   │   ├── query: linear
│   │           │   │   ├── key: linear
│   │           │   │   ├── value: linear
│   │           │   │   └── dropout: Dropout
│   │           │   └── output: BertSelfOutput
│   │           │       ├── dense: linear
│   │           │       ├── LayerNorm: LayerNorm
│   │           │       └── dropout: Dropout
│   │           ├── intermediate: BertIntermediate
│   │           │   ├── dense: linear
│   │           │   └── intermediate_act_fn: nn.GELU(dense(hidden_states))
│   │           └── output: BertOutput
│   │               ├── dense: linear
│   │               ├── LayerNorm: LayerNorm
│   │               └── dropout: Dropout
│   └── pooler: BertPooler
│       ├── dense: linear
│       └── activation: nn.Tanh(dense(cls_token))
├── qa_outputs: linear_layer (768-in, 2-out)
└── reasoning_output: linear_layer (768-in, 3-out)
```

Below is a step‑by‑step walkthrough of the entire script, broken into logical blocks, with a high‑level diagram of how data flows through the model at inference time.

---

## 1. Custom Output Container

```python
class QuestionAnsweringModelOutput:
    def __init__(self, loss=None, start_logits=None, end_logits=None,
                 hidden_states=None, attentions=None, reasoning_logits=None):
        self.loss = loss
        self.start_logits = start_logits
        self.end_logits = end_logits
        self.hidden_states = hidden_states
        self.attentions = attentions
        self.reasoning_logits = reasoning_logits
```

* **Purpose**: Wraps everything the QA‑with‑reasoning model produces into a single object.

  * `start_logits` / `end_logits`: scores over each token being start/end of answer.
  * `reasoning_logits`: classification over “factual”, “causal”, “comparative” reasoning.
  * `loss`: when training, combined answer‑span + reasoning loss.

---

## 2. BERT Configuration

```python
class BertConfigCustom:
    def __init__(self, vocab_size=30522, hidden_size=768, …, reasoning_vocab_size=3):
        # Standard BERT hyperparameters…
        self.reasoning_vocab_size = reasoning_vocab_size
```

* Encapsulates model hyperparameters (dimensions, dropout rates, number of layers, etc.)
* Extended to include `reasoning_vocab_size` for the extra classification head.

---

## 3. Embeddings

```python
class BertEmbeddings(nn.Module):
    def __init__(self, config):
        self.word_embeddings    = Embedding(vocab_size, hidden_size)
        self.position_embeddings= Embedding(max_pos, hidden_size)
        self.token_type_embeddings = Embedding(type_vocab_size, hidden_size)
        self.LayerNorm = LayerNorm(hidden_size)
        self.dropout   = Dropout(hidden_dropout_prob)
    def forward(self, input_ids, token_type_ids=None):
        # sum word + position + type embeddings
        embeddings = words + positions + types
        embeddings = LayerNorm(embeddings)
        return dropout(embeddings)
```

* **Word embeddings** map token IDs → vectors.
* **Position embeddings** inject sequence order.
* **Token‑type embeddings** (segment IDs) differentiate “question” vs. “context”.
* They’re summed, normalized, then dropped‑out.

---

## 4. Multi‑Head Self‑Attention

### 4.1. Query/Key/Value & Heads

```python
class BertSelfAttention(nn.Module):
    def __init__(…):
        self.num_heads = config.num_attention_heads
        self.head_dim  = hidden_size // num_heads
        self.query, self.key, self.value = Linear→hidden_size
```

* Projects each position’s hidden vector into Q, K, V of shape `(batch, seq, heads, head_dim)`.
* **Scaled dot‑product**:

  $$
    \mathrm{scores} = \frac{Q\,K^T}{\sqrt{\mathrm{head\_dim}}}
  $$
* Applies optional attention mask (to ignore padding).
* Softmax → attention weights → dropout → weighted sum with V → recombine heads.

### 4.2. Residual + LayerNorm

```python
class BertSelfOutput(nn.Module):
    def forward(self, hidden_states, input_tensor):
        hidden = dense(hidden_states)
        hidden = dropout(hidden)
        return LayerNorm(hidden + input_tensor)
```

* Follows “Attention → Dense → Dropout → Add & Norm” pattern.

---

## 5. Transformer Layer & Encoder Stack

```python
class BertLayer(nn.Module):
    def __init__(…):
        self.attention   = BertAttention(config)
        self.intermediate = Linear→intermediate_size + GELU
        self.output      = BertOutput(config)

    def forward(self, hidden_states, attention_mask=None):
        attention_output    = self.attention(hidden_states, attention_mask)
        intermediate_output = self.intermediate(attention_output)
        return self.output(intermediate_output, attention_output)
```

* **BertAttention** = Self‑attention + output projection.
* **BertIntermediate** = feed‑forward “dense → activation”.
* **BertOutput** = feed‑forward output projection + add & norm.
* **BertEncoder** stacks `num_hidden_layers` of these.

---

## 6. Pooler

```python
class BertPooler(nn.Module):
    def forward(self, hidden_states):
        cls_token = hidden_states[:, 0]
        return tanh(dense(cls_token))
```

* Takes the `[CLS]` token’s final hidden state and projects it for sentence‑level tasks (here, reasoning classification).

---

## 7. Full BERT Model

```python
class BertModelCustom(nn.Module):
    def forward(self, input_ids, attention_mask, token_type_ids):
        emb = self.embeddings(input_ids, token_type_ids)
        seq_out, all_hidden = self.encoder(emb, extended_mask)
        pooled = self.pooler(seq_out)
        return seq_out, pooled, all_hidden
```

* **Outputs**:

  * `seq_out` – per‑token embeddings for QA head.
  * `pooled` – `[CLS]` embedding for reasoning head.
  * `all_hidden` – list of hidden states at each layer (not used downstream here).

---

## 8. QA + Reasoning Head

```python
class BertForQuestionAnsweringWithReasoning(nn.Module):
    def __init__(…):
        self.bert = BertModelCustom(config)
        self.qa_outputs       = Linear(hidden_size → 2)   # start/end logits
        self.reasoning_output = Linear(hidden_size → n_labels)

    def forward(self, input_ids, …, start_positions=None, end_positions=None, reasoning_labels=None):
        seq_out, pooled, _ = self.bert(...)
        logits = self.qa_outputs(seq_out)         # shape (B, L, 2)
        start_logits, end_logits = split(logits)  # each (B, L)
        reasoning_logits = self.reasoning_output(pooled)  # (B, n_labels)

        if training: compute CrossEntropyLoss for start, end, and reasoning
        return QuestionAnsweringModelOutput(...)
```

* **Span prediction**: linear on each token → softmax over positions.
* **Reasoning classification**: linear on pooled CLS → softmax over reasoning types.

---

## 9. Dataset Preparation

```python
class QADatasetWithReasoning(Dataset):
    def __getitem__(self, idx):
        # 1. Tokenize (question, context) with offsets
        # 2. Map character-level answer span → token indices
        # 3. Map reasoning_label string → integer
        return { 'input_ids': …,
                 'attention_mask': …,
                 'start_positions': tensor(i),
                 'end_positions':   tensor(j),
                 'reasoning_labels': tensor(r) }
```

* Uses HuggingFace’s `BertTokenizerFast` to get offset mappings.
* Finds which token covers the answer’s start/end character positions.

---

## 10. Retrieval‑Augmented Inference

1. **Build context embeddings**

   ```python
   CONTEXT_EMB = build_context_embeddings(model, tokenizer, CONTEXTS, device)
   ```

   * Encode each candidate passage once (pooled CLS).

2. **At query time**

   ```mermaid
   flowchart LR
     Q[“Why…?”] -->|tokenize & BERT| Q_emb[(q_emb)]
     Q_emb -->|cosine similarity| sims[sims w/ all contexts]
     sims --> idx{argmax}
     idx --> Ctx[best passage]
     Ctx & Q -->|tokenize & BERT‑QA| span_logits
     span_logits --> Answer[decoded answer span]
   ```

   * Compute question embedding.
   * Rank contexts by cosine similarity.
   * Run QA head on top‑1 context.

---

## 11. End‑to‑End Main Script

1. **Extract passages** from a PDF (`fitz`), chunk into 5‑sentence blocks.
2. **Auto‑generate “toy” QA examples** (question = “What is the main idea…”, answer = first sentence).
3. **Save** as JSON.
4. **Load** into `QADatasetWithReasoning` → `DataLoader`.
5. **Initialize** model, optimizer, build `CONTEXT_EMB`.
6. **Train** for 2 epochs, logging loss.
7. **Inference**: given a hand‑crafted question, retrieve and answer.

---

### Putting It All Together

At **training**, each batch provides both span targets and reasoning labels. The model learns to:

* Point to the correct tokens for answer (via `start_logits`, `end_logits`).
* Classify the “type” of reasoning used (via `reasoning_logits`).

At **inference**, you can:

1. **(Optional)** Build embeddings for a large pool of passages once.
2. **For each new question**:

   * Retrieve the most relevant passage.
   * Run QA head to extract the answer.

This combination of retrieval + QA + reasoning is useful for document‑level question answering where you also want a meta‑explanation of *why* the answer is valid (factual vs. causal vs. comparative).

---

**Key takeaways**:

* The backbone is **vanilla BERT**, re‑implemented from scratch.
* Two “heads” on top:

  1. **Span prediction** (start/end)
  2. **Reasoning classification**
* A simple **retrieval** mechanism selects which context to feed into the QA head.
* The script automates data prep (from PDF) → training → QA inference.
