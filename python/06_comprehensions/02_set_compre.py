nums = [1, 2, 2, 3, 3, 4]

#set comprehension : [expression for item in iterable if condition]
#Removes duplicates automatically.
unique_squares = {x*x for x in nums}
print(unique_squares)


# good example 
recipes = {
    "Masala Chai": ["ginger", "cardamon", "clove"],
    "Elaichi Chai": ["cardamon", "milk"],
    "Spicy Chai": ["ginger", "black pepper", "clove"], 
}

unique_spices = {spice for ingredients in recipes.values() for spice in ingredients}
print(unique_spices)