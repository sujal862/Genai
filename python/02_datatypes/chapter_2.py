#in Set() : mutable the memoryy address is same , but the value is changing

spice_mix = set()
print(f"Initial spice mix id: {id(spice_mix)}")
print(f"Initial spice mix id: {spice_mix}")
spice_mix.add("Ginger")
spice_mix.add("cardamon")
print(f"Initial spice mix id: {id(spice_mix)}")
print(f"Initial spice mix id: {spice_mix}")