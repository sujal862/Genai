import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

#print("Vocab Size", encoder.n_vocab) # 200019 (200k) : dictionary size

text = "The cat sat on the mat"
tokens = encoder.encode(text)
 
print("tokens:", tokens)

decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450])
print(decoded)