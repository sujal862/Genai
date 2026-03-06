a = "Aromatic and Bold"
#slice : first:end:step
print(f"First word: {a[0:8]}")
print(f"last word: {a[12:]}")
print(f"rev word: {a[::-1]}")
 
# encoding é a special character, python converts it into bytes
label_text = "Chai Spécial"

encoded = label_text.encode("utf-8")
print(f"Encoded: {encoded}")

decoded = encoded.decode("utf-8")
print(f"Encoded: {decoded}")