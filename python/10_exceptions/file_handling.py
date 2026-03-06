# file = open("order.txt", "w")
# try:
#     file.write("masala")
# finally:
#     file.close()


# modern way 
with open("order.txt", "w") as file:
    file.write("ginger")