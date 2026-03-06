#filter : filter(function, iterable) 
#It keeps items that return True.

chai_types = ["light", "kadak", "ginger", "kadak"]

strong_chai = list(filter(lambda chai: chai=="kadak", chai_types))
print(strong_chai)