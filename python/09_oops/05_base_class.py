class Chai:

    def __init__(self, type_, strength):
        self.type = type_
        self.strenght = strength

# using super()
class GingerChai(Chai):
    def __init__(self, type_, strength, spice_level):
        super().__init__(type_, strength)
        self.spice_level = spice_level