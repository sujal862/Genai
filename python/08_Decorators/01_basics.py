from functools import wraps

#decorators : A function that modifies another function.
def my_decorator(func):
    @wraps(func) #Now wraps copies metadata(name, doc..etc) from func to wrapper
    def wrapper():
        print("Before function runs")
        func()
        print("after function runs")
    return wrapper

@my_decorator
def greet():
    print("Hello from decorators class from chaicode")

# the above line is similar to (in easy):
# greet = my_decorator(greet) # The original greet function gets replaced with (greet → wrapper)

greet()
print(greet.__name__) # output will be wrapper if we would not use @wraps(func)




# What wraps Actually Does
# Copies metadata from original function to wrapper so the decorated function still behaves like the original

# wrapper.__name__ = func.__name__
# wrapper.__doc__ = func.__doc__
# wrapper.__module__ = func.__module__