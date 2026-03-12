from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI() # Ye OpenAI client object banata hai

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small" # Ye model text ko numeric vector(small dimension) me convert karta hai.
)

print("Vector Embeddings: ", response.data[0].embedding)


class Encoder:
    
    def __init__(self):
        self.word2id = {}
        self.id2word = {}
        self.vocab_size = 0

    def build_vocab(self, text):
        words = text.split()

        for word in words:
            if word not in self.word2id:
                self.word2id[word] = self.vocab_size
                self.id2word[self.vocab_size] = word
                self.vocab_size += 1


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
encoder.build_vocab(text)

encoded = encoder.encode(text)
print("Encoded:", encoded)

decoded = encoder.decode(encoded)
print("Decoded:", decoded)