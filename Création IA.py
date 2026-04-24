import math
import random

donnee = [(1,0), (5,1), (2,0), (8,1)]

class Neurrone:
    def __init__(self):
        self.poids = random.uniform(-1, 1)
        self.bias = random.uniform(-0.1, 0.1)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def forward(self, entree):
        return self.sigmoid(entree * self.poids + self.bias)

    def train(self, x, lr, epochs):
        for i in range(epochs):
            total_loss = 0
            for key, label in x:
                output = self.forward(key)
                erreur = label - output
                derive = (output * (1 - output))
                self.poids += lr * erreur * key * derive
                self.bias += lr * erreur * derive
                total_loss += erreur ** 2
            print(total_loss / len(x))

class NeuronneSortie:
    def __init__(self):
        self.poids1 = random.uniform(-1, 1)
        self.poids2 = random.uniform(-1, 1)
        self.poids3 = random.uniform(-1, 1)
        self.bias = random.uniform(-0.1, 0.1)

    def forward(self, s1, s2, s3):
        return Neurrone.sigmoid(s1 * self.poids1 + s2 * self.poids2 + s3 * self.poids3 + self.bias)

class MLP:
    def __init__(self):
        self.neuronne1 = Neurrone()
        self.neuronne2 = Neurrone()
        self.neuronne3 = Neurrone()
        self.sortie = NeuronneSortie()
        self.s1 = None
        self.s2 = None
        self.s3 = None

    def forward(self, entree):
        self.s1 = self.neuronne1.forward(entree)
        self.s2 = self.neuronne2.forward(entree)
        self.s3 = self.neuronne3.forward(entree)
        return self.sortie.forward(self.s1, self.s2, self.s3)

    def train(self, entree, lr, epochs):
        for i in range(epochs):
            for key, label in entree:
                output = self.forward(key)
                erreur = label - output
                derive = (output * (1 - output))

                self.sortie.poids1 += lr * erreur * self.s1 * derive
                self.sortie.poids2 += lr * erreur * self.s2 * derive
                self.sortie.poids3 += lr * erreur * self.s3 * derive
                self.sortie.bias += lr * erreur * derive

                erreur_cache1 = erreur * derive * self.sortie.poids1
                erreur_cache2 = erreur * derive * self.sortie.poids2
                erreur_cache3 = erreur * derive * self.sortie.poids3

                derive_cache1 = self.s1 * (1-self.s1)
                derive_cache2 = self.s2 * (1-self.s2)
                derive_cache3 = self.s3 * (1-self.s3)


                self.neuronne1.poids += lr * erreur_cache1 * derive_cache1 * key
                self.neuronne2.poids += lr * erreur_cache2 * derive_cache2 * key
                self.neuronne3.poids += lr * erreur_cache3 * derive_cache3 * key

                self.neuronne1.bias += lr * erreur_cache1 * derive_cache1
                self.neuronne2.bias += lr * erreur_cache2 * derive_cache2
                self.neuronne3.bias += lr * erreur_cache3 * derive_cache3


class tokenizer:
    def __init__(self):
        self.vocabulaire = {}
        self.vocabulaire_inverse = {}

    def fit(self, textes):
        index = 0
        for texte in textes:
            for mot in texte.split():
                if mot not in self.vocabulaire:
                    self.vocabulaire[mot] = index
                    index += 1
        self.vocabulaire_inverse = {v: k for k, v in self.vocabulaire.items()}

    def encode(self, texte):
        resultat = []
        for mot in texte.split():
            resultat.append(self.vocabulaire[mot])
        return resultat

    def decode(self, indices):
        resultat = []
        for indice in indices:
            resultat.append(self.vocabulaire_inverse[indice])
        return " ".join(resultat)

class Embedding:
    def __init__(self, vocab_size, embedding_dim):
        self.table = []
        for i in range(vocab_size):
            vecteur = [random.uniform(-1, 1) for _ in range(embedding_dim)]
            self.table.append(vecteur)

    def forward(self, token_id):
        return self.table[token_id]

def dot_product(a, b):
    return sum(ai * bi for ai, bi in zip(a, b))

def softmax(x):
    max_x = max(x)
    exp_x = [math.exp(i - max_x) for i in x]
    total = sum(exp_x)
    return [i / total for i in exp_x]

def attention(q, k, v):
    output = []
    for q_item in q:
        ligne = []
        for k_item in k:
            ligne.append((dot_product(q_item, k_item)) / math.sqrt(len(k[0])))
        scores = softmax(ligne)

        vecteur_final = [0] * len(v[0])
        for i, score in enumerate(scores):
            for j in range(len(v[0])):
                vecteur_final[j] += score * v[i][j]
        output.append(vecteur_final)
    return output

class AttentionHead:
    def __init__(self, embed_dim, head_dim):
        self.wq = [[random.uniform(-1, 1) for _ in range(embed_dim)] for _ in range(head_dim)]
        self.wk = [[random.uniform(-1, 1) for _ in range(embed_dim)] for _ in range(head_dim)]
        self.wv = [[random.uniform(-1, 1) for _ in range(embed_dim)] for _ in range(head_dim)]

    def project(self, x, W):
        return [dot_product(w, x) for w in W]

    def forward(self, x):
        Q = [self.project(token, self.wq) for token in x]
        K = [self.project(token, self.wk,) for token in x]
        V = [self.project(token, self.wv) for token in x]
        return Q, K, V

def relu(x):
    return [i if i > 0 else 0 for i in x]

class FFN:
    def __init__(self, embed_dim, FFN_dim):
        self.w1 = [[random.uniform(-1, 1) for i in range(embed_dim)] for _ in range(FFN_dim)]
        self.w2 = [[random.uniform(-1, 1) for i in range(FFN_dim)] for _ in range(embed_dim)]

    def forward(self, x):
        hiden = [dot_product(w, x) for w in self.w1]
        print(hiden)
        hiden = relu(hiden)
        print(hiden)
        output = [dot_product(w, hiden) for w in self.w2]
        return output

class transformerBlock:
    def __init__(self, embed_dim, ffn_dim, head_dim):
        self.attention_head = AttentionHead(embed_dim, head_dim)
        self.ffn = FFN(embed_dim, ffn_dim)

    def forward(self, x):
        result_attention_head = self.attention_head.forward(x)
        result_attention = attention(result_attention_head[0], result_attention_head[1], result_attention_head[2])
        result_ffn = []
        for i in result_attention:
            result_ffn.append(self.ffn.forward(i))
        return result_ffn




transform = transformerBlock(1, 3, 5)
print(transform.forward([[1, 2, 1, 2], [2, 1, 3, 2]]))
