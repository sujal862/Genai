# nonlocal
def update_counter():
    count = 0
    def increment():
        # "Hey, don't create a new local variable named count. Use the count from the outer function."
        nonlocal count # now this count variable refers to outer count variable
        count += 1
        return count
    return increment # returns the increment function


counter = update_counter() # Now counter becomes the increment function.
print(counter())
print(counter())
print(counter())


# Global ex
chai_type = "Plain"

def front_desk():
    def kitchen():
        global chai_type
        chai_type = "Irnai" # changes the global variable

    kitchen()

front_desk()
print("Final global chai:", chai_type)