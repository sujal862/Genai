# Basic list operations
ingredients = ["water", "milk", "black tea"]
ingredients.append("sugar")
print(f"Ingredients are: {ingredients}")

ingredients.remove("water")
print(f"Ingredients are: {ingredients}")


# Working with multiple lists
spice_options = ["ginger", "cardamom"]
chai_ingredients = ["water", "milk"]

chai_ingredients.extend(spice_options)
print(f"chai: {chai_ingredients}")

chai_ingredients.insert(2, "black tea")
print(f"chai: {chai_ingredients}")


# Removing last element
last_added = chai_ingredients.pop()
print(f"{last_added}")
print(f"chai: {chai_ingredients}")


# Reverse and sort
chai_ingredients.reverse()
print(f"chai: {chai_ingredients}")

chai_ingredients.sort()
print(f"chai: {chai_ingredients}")


# Numeric list operations
sugar_levels = [1, 2, 3, 4, 5]
print(f"Maximum sugar level: {max(sugar_levels)}")
print(f"Minimum sugar level: {min(sugar_levels)}")


# Combining lists (Operator Overloading)
base_liquid = ["water", "milk"]
extra_flavor = ["ginger"]

full_chai = base_liquid + extra_flavor
print(f"Full chai ingredients: {full_chai}")

strong_brew = ["black tea", "water"] * 3
print(f"String brew: {strong_brew}")