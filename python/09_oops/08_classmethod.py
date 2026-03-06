# # Use class method when the method needs to modify or access class-level data.
# class Chai:

#     shop_name = "Tea House"
#     @classmethod
#     def change(cls): # All objects see this change
#         cls.shop_name = "coffe house"
#     @classmethod 
#     def show_shop(cls):
#         print(cls.shop_name)


# cup1 = Chai()
# cup2 = Chai()

# cup1.change()
# cup2.show_shop()





# Class method is use in real life for alternative(2nd) constructor
# All constructors finally call __init__
class ChaiOrder:

    def __init__(self, tea_type, sweetness, size):
        self.tea_type = tea_type
        self.sweetness = sweetness
        self.size = size
    
    @classmethod # 2nd constructor using dict
    def from_dict(cls, order_data):
        # cls(...) calls the class constructor equivalent to ChaiOrder(...)
        return cls( 
            order_data["tea_type"],
            order_data["sweetness"],
            order_data["size"],
        )
    
    @classmethod # 3rd constructor using string
    def from_string(cls, order_string):
        tea_type, sweetness, size = order_string.split(",")
        return cls(tea_type, sweetness, size) # calls chaiorder constructor


# Using dictionary constructor
order1 = ChaiOrder.from_dict({
    "tea_type": "Masala",
    "sweetness": "Medium",
    "size": "Large"
})

# Using string constructor
order2 = ChaiOrder.from_string("Ginger,Low,Small")


print(order1.tea_type, order1.sweetness, order1.size)
print(order2.tea_type, order2.sweetness, order2.size)