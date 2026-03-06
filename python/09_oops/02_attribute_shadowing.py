class Chai:
    temperature = "hot"
    strength = "Strong"


cutting = Chai()

print(cutting.temperature)

cutting.temperature = "Mild"

print("After changing ", cutting.temperature)
print("Direct look into the class ", Chai.temperature)

del cutting.temperature
print(cutting.temperature) # the value fallback to class(chai) after obj is deleted