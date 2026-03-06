# MRO is the algorithm Python uses to decide the order in which classes are searched.
# Python solves the diamond problem using MRO

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

d = D() 
d.show() # MRO order is : D → B → C → A   so, Python finds show() in B first.