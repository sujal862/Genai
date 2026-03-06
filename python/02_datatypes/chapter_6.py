essential_spices = {"cardamon", "ginger", "cinnamon"}
optional_spices = {"cloves", "ginger", "black pepper"}

# | = (Pipe Operator) it does union, union means combining two sets and removing duplicates.
all_spices = essential_spices | optional_spices
print(f"All spices: {all_spices}")

# Intersection
common_spices = essential_spices & optional_spices
print(f"common spices: {common_spices}")