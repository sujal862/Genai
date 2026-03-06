# Inheritance
class Chai:  # Parent class
    def __init__(self, type_):
        self.type = type_

    def prepare(self):
        print(f"Preparing {self.type} chai...")


class MasalaChai(Chai):  # Child class inherits Chai
    def add_masala(self):
        print("Adding masala")

#Composition : A class contains another class as a component.
class ChaiShop:
    chai_cls = Chai # chai_cls now contains the refrence of Chai class

    def __init__(self):
        self.ch = self.chai_cls("Regular") # Chai class constructor called / now Chai class obj is created and stored in "ch" var

    def serve(self):
        print(f"Serving {self.ch.type} chai in the shop")
        self.ch.prepare()




cup = MasalaChai("haldi")
shop = ChaiShop()

cup.prepare()        # inherited from Chai
cup.add_masala()  # defined in MasalaChai
shop.serve()


