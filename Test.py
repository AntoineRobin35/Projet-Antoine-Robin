    import cupy as cp

    class Datapipeline:
        def __init__(self, batch_size, vocab_size, seq_len, dmodel):
            self.batch_size = batch_size
            self.vocab_size = vocab_size
            self.seq_len = seq_len
            self.dmodel = dmodel


        @staticmethod
        def dataloading():
            with open("TyniShakspeare.txt", "r") as f:
                text = f.read()
                return text

        def vocabeloading(self):
            text = self.dataloading()
            lettre = []
            vocab = []
            for char in text:
                lettre.append(char)
            vocab.append(set(sorted(lettre)))
            self.vocab_size = len(vocab)
            return vocab

        def vocabtodico(self):
            vocab = self.vocabeloading()
            dico = {}
            for char in vocab[0]:
                dico[char] = len(dico)
            return dico

        def dicotovocab(self):
            vocab = self.vocabeloading()
            dico = {}
            for char in vocab[0]:
                dico[len(dico)] = char
            return dico

        def encode(self):
            dico = self.vocabtodico()
            text = self.dataloading()
            textencode = []
            for char in text:
                textencode.append(dico[char])
            textencode = cp.array(textencode)
            return textencode

        def decode(self, text):
            dico = self.dicotovocab()
            textdecode = []
            for nbr in text:
                textdecode.append(dico[nbr])
            textdecode = cp.array(textdecode)
            return textdecode

        def dataset(self):
            textencode = self.encode()
            x = []
            y = []
            batchx = []
            batchy = []
            for i in range(len(textencode) - self.seq_len):
                x.append(textencode[i:i + self.seq_len])
                y.append(textencode[i + 1:i + self.seq_len + 1])

            for i in range(len(x) // self.batch_size):
                i = i * self.batch_size
                batchx.append(x[i:i + self.batch_size])
                batchy.append(y[i:i + self.batch_size])

            dataset = cp.array([batchx, batchy])
            return dataset

    class Attention:
        def __init__(self, seq_len, dk, dv, dmodel):
            self.seq_len = seq_len
            self.dmodel = dmodel
            self.dk = dk
            self.dv = dv
            self.wq = cp.random.rand(self.dmodel, self.dk)
            self.wk = cp.random.rand(self.dmodel, self.dk)
            self.wv = cp.random.rand(self.dmodel, self.dv)

        def softmax(self, x):
            return cp.exp(x) / cp.sum(cp.exp(x), axis=1, keepdims=True)

        def forward(self, x):
            Q = x @ self.wq
            K = x @ self.wk
            V = x @ self.wv

            S = Q @ K.transpose(1, 2) / cp.sqrt(self.dk)

            mask = cp.tril(cp.ones((self.seq_len, self.seq_len)))
            S = cp.where(mask == 0, -cp.inf, S)

            A = self.softmax(S)

            O = A @ V
            return O

        def backward(self, x):
            self.wq += 

    class GPT:
        def __init__(self):
            self.batch_size = 128
            self.vocab_size = None
            self.seq_len = 32
            self.dmodel = 32
            self.dk = 16
            self.dv = 16
            self.E = cp.random.rand(self.vocab_size, self.dmodel)

        def forward(self, dataset):
            for batchx, batchy in dataset:
                batchx = self.E[batchx]