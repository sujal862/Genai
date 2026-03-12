class Encoder:
    
    def __init__(self):
        self.word2id = {}
        self.id2word = {}
        self.vocab_size = 0 # Ye count karta hai kitne unique words hain

    def build_vocab(self, text):
        words = text.split()

        for word in words:
            if word not in self.word2id: #agar word new hai
                self.word2id[word] = self.vocab_size # work ko vocab_size hi id de rha 
                self.id2word[self.vocab_size] = word
                self.vocab_size += 1

    # convert text to numbers
    def encode(self, text):
        words = text.split()
        tokens = []

        for word in words:
            tokens.append(self.word2id[word])

        return tokens


    def decode(self, tokens):
        words = []

        for token in tokens:
            words.append(self.id2word[token])

        return " ".join(words)


# Example
text = "Hello world namaste duniya"

encoder = Encoder()
encoder.build_vocab(text) # Vocabulary build (dictionary)

encoded = encoder.encode(text)
print("Encoded:", encoded)

decoded = encoder.decode(encoded)
print("Decoded:", decoded)