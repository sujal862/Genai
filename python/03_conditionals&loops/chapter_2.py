seat_type = input("Enter seat type (sleeper/AC/Non-AC): ").lower()

# match case
match seat_type:
    case "sleeper":
        print("Sleeper seat selected")
    case "ac":
        print("AC seat selected")
    case "non-ac":
        print("Non-AC seat selected")
    case _:
        print("Invalid seat type")