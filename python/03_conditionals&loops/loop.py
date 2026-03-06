for token in range(1, 11) :
    print(f"Serving chai to Token #{token}")

#Enumerate(iterable, start=?) 
#is used to: Loop over a list AND get the index + value at the same time.
menue = ["Green", "Lemon", "Spiced"]

for idx, item in enumerate(menue, start=1):
    print(f"{idx} : {item} chai")


#zip(*iterables) : is used to: Combine multiple iterables (lists, tuples, etc.) element-wise.
#It pairs elements based on their position (index).
names = ["Sujal", "Rahul", "Aman"]
scores = [85, 90, 78]

for name, score in zip(names, scores):
    print(name, score)

#for-else : else block runs only if the loop completes normally without encountering break statement
for i in range(5):
    print(i)
else:
    print("Loop finished normally")