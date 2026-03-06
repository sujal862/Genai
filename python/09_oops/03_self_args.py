class Chaicup:
    size = 150  # class Var

    def describe(self):
        # self refers to the object that calls this method
        return f"A {self.size}ml chai cup"


cup = Chaicup()

# Calling method using object
# Python internally does: Chaicup.describe(cup)
print(cup.describe())

# Calling method directly using class
# We manually pass the object as 'self'
print(Chaicup.describe(cup))


# Creating another object
cup_two = Chaicup()

# Overriding the class variable for this specific object
# Now this object has its own size
cup_two.size = 100

# Calling method using class syntax and passing object
print(Chaicup.describe(cup_two))