chai_menu = {"masala": 30, "ginger": 40}

try:
    chai_menu["elaichi"]
except KeyError:
    print("The Key not exsist")

print("Hello chai code")


#  - - - - - - - - - - - - - - - - - - - - - - - - -



def serve_chai(flavor):
    
    try:
        # Try block: yaha normal code run hota hai
        print(f"Preparing {flavor} chai...")

        # Agar flavor "unknown" hai to error raise karenge
        if flavor == "unknown":
            raise ValueError("We don't know that flavor")

    except ValueError as e:
        print("Error:", e)

    else:
        # Ye tab run hota hai jab try block me koi error nahi aata
        print(f"{flavor} chai is served")

    finally:
        # Ye block hamesha run hota hai
        print("Next customer please")


# Function call with valid flavor
serve_chai("masala")

print("------")

# Function call with invalid flavor
serve_chai("unknown")