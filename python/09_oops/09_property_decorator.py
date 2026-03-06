class TeaLeaf:

    def __init__(self, age):
        # store the real value in a hidden variable
        # we use _age instead of age to avoid recursion with property
        self._age = age


    @property # (getter)
    def age(self):
        # this method runs when we access leaf.age 
        # but we can access it like a normal variable
        return self._age


    @age.setter
    def age(self, age):
        # this method runs when we assign value like leaf.age = 3

        # validation: allow only age between 1 and 5
        if 1 <= age <= 5:
            self._age = age
        else:
            #raise is used to manually throw an error (exception) in Python.
            raise ValueError("Tea leaf age must be between 1 and 5 years")


# creating object
leaf = TeaLeaf(3)

# accessing property (calls getter method)
print(leaf.age)

# setting new value (calls setter method)
leaf.age = 4
print(leaf.age)

# invalid value (will raise error)
# leaf.age = 10