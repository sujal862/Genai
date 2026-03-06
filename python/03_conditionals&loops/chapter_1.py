order_amount = int(input("Enter the order amount: "))

# ternary operator
delivery_fees = 0 if order_amount > 100 else 30
print(f"Delivery fees: {delivery_fees}")

