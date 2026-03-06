sugar_amount = 2 # sugar_amount points(refers) to the object(2)
print(f"Intial sugar: {sugar_amount}")

sugar_amount = 12
print(f"Second Intial sugar: {sugar_amount}") #it makes sugar_amount point to a new object 12

print(f"ID of 2: {id(2)}") # 2 and 12 are integer objects
print(f"ID of 12: {id(12)}") 

#i.e int are imutable so the in memory of 2 object the value is not chaged , instead a new obj 12 is made and pointed

