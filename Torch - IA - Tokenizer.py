import torch
import torch.nn as nn
import tiktoken
import math

class GPT2(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding = nn.Embedding(50257, 768)
        self.position_embedding = nn.Embedding(1024, 768)
        self.blocks = nn.ModuleList([Block() for _ in range(12)])
        self.ln_f = nn.LayerNorm(768)
        self.lm_head = nn.Linear(768, 50257)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, x):
        output = self.token_embedding(x)
        position = torch.arange(x.shape[1])
        position_embeding = self.position_embedding(position)
        x = output + position_embeding
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        x = self.lm_head(x)
        return x

    def train_model(self, x, epochs, optimizer, loss_fn):
        for _ in range(epochs):
            for key, value in x:
                key = key.to(self.device)
                value = value.to(self.device)
                output = self.forward(key)
                value = value.to(self.device)
                loss = loss_fn(output, value)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

class MLA(nn.Module):
    def __init__(self):
        super().__init__()
        self.qkv = nn.Linear(768, 2304)
        self.proj = nn.Linear(768, 768)
        self.num_heads = 12
        self.head_dim = 64
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, x):
        qkv = self.qkv(x)
        q, k, v = torch.chunk(qkv, 3, dim=-1)
        seq_len = x.shape[0]
        q = q.view(seq_len, self.num_heads, self.head_dim).transpose(0, 1)
        k = k.view(seq_len, self.num_heads, self.head_dim).transpose(0, 1)
        v = v.view(seq_len, self.num_heads, self.head_dim).transpose(0, 1)
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
        scores = torch.softmax(scores, dim=-1)
        output = (scores @ v).transpose(0, 1).contiguous().view(seq_len, 768)
        output = self.proj(output)
        return output

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(768, 3072),
            nn.GELU(),
            nn.Linear(3072, 768)
        )
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, x):
        return self.layers(x)

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(768)
        self.mla = MLA()
        self.ln2 = nn.LayerNorm(768)
        self.mlp = MLP()

    def forward(self, x):
        x = x + self.mla(self.ln1(x))
        return  x + self.mlp(self.ln2(x))

class dataLoader(torch.utils.data):
    def __init__(self, tokens, seq_lenght):
        self.tokens = tokens
        self.seq_lenght = seq_lenght

    def __len__(self):
        return len(self.tokens) - self.seq_lenght

    def __getitem__(self, item):
        return [self.tokens[item: item + self.seq_lenght], self.tokens[item + 1: item + self.seq_lenght + 1]]

    def data