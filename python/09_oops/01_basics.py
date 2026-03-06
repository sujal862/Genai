# CLASS = blueprint for creating objects
class Chai:

    # CLASS VARIABLE (shared by all objects)
    shop_name = "Sujal Chai Stall"

    # CONSTRUCTOR (runs automatically when object is created)
    def __init__(self, chai_type, sugar_level):
        # INSTANCE VARIABLES (unique for each object)
        self.chai_type = chai_type
        self.sugar_level = sugar_level

    # METHOD (function inside class)
    def brew(self):
        # self refers to the current object
        print(f"Brewing {self.chai_type} chai with sugar level {self.sugar_level}")

    # Another method
    def show_shop(self):
        print(f"Serving from {Chai.shop_name}")


# CREATING OBJECTS (instances of class)

cup1 = Chai("Masala", 2)
cup2 = Chai("Ginger", 1)

# USING OBJECT DATA
print(cup1.chai_type)   # instance variable
print(cup2.chai_type)

# CALLING METHODS
cup1.brew()
cup2.brew()

# ACCESSING CLASS VARIABLE
print(cup1.shop_name)
print(cup2.shop_name)

# Calling another method
cup1.show_shop()