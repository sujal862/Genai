#Dictionary
chai_order = dict(type="Masala Chai", size="Large", sugar=2)
# another way :
# chai_order = {
#     "type": "Masala Chai",
#     "size": "Large",
#     "sugar": 2
# }

print(chai_order)

chai_recipe = {}
chai_recipe["base"] = "black tea"
chai_recipe["liquid"] = "milk"

print(f"Chai Recipe base: {chai_recipe['base']}")

#to delete
del chai_recipe["base"]

# membership testing
print(f"is sugar in the order? {'sugar' in chai_order}")

#print keys
print(chai_order.keys())

# pop last item
print(chai_order.popitem())

# safe way to get 
print(chai_order.get("size"))      # safe
print(chai_order["size"])          # unsafe