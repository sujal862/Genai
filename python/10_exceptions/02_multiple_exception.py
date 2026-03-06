def process_order(item, quant):
    try:
        price = {"masala": 20}[item]
        cost =  price * quant
        print(f"total cost is {cost}")
    except KeyError:
        print("Sorry that chai is not on menu")
    except TypeError:
        print("Quantity must be in number")
    
process_order("masala", 2)
process_order("masala", "two")







# Note: we can access value of key in dict like this also 
# a = {"b": 2}["b"]
# print(a)