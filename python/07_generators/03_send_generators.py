def chai_customer():
    print("Welcome! What chai would you like?")  
    # This runs when generator starts for the first time

    order = yield  
    # Generator pauses here.
    # It waits to RECEIVE a value using .send()
    # That received value will be stored in 'order'

    while True:  
        # Infinite loop — generator keeps running forever

        print(f"Preparing: {order}")  
        # Prints the current order received

        order = yield  
        # Pause again and wait for next order
        # Whatever value is sent using .send()
        # gets stored in 'order'
        

# Create generator object (nothing runs yet)
stall = chai_customer()

# Start the generator manually
# This runs until first 'yield'
next(stall)

# Send value into the paused generator
# "Masala Chai" goes inside and becomes value of 'order'
stall.send("Masala Chai")

# send more values:
stall.send("Green Tea")
stall.send("Black Tea")