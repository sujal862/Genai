from functools import wraps

def require_admin(func):
    @wraps(func)
    def wrapper(user_role):
        if user_role != "admin":
            print("Acess denied: Admins only")
        else:
            return func(user_role) # return time pa hi call ho ja rha 
    return wrapper

@require_admin
def acess_tea_inventory(role):
    print("Acess granted to tea inventory")

acess_tea_inventory("user")
acess_tea_inventory("admin")