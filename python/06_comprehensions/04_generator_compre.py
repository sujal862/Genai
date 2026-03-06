# It does NOT store all values in memory.
# It generates values one by one when needed.  == memory efficient

nums = [1, 2, 3, 4]

gen = (x * x for x in nums)

# lazy evaluation : It does NOT compute everything immediately. It computes only when requested.
print(list(gen))