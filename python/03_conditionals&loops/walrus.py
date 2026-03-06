# walrus operator :=  
# Assignment Expression Operator

value = 13

# 👉 Assign the value after evaluation
# 👉 And use it immediately

# Calculate 13 % 5
# Store result in remainder
# Use that value inside if
if (remainder := value % 5):
    print(f"Not divisible, remainder is {remainder}")