class A:
    def __init__(self, x):
        self.x = x

p = A(10)
q = p
p.x = 99
