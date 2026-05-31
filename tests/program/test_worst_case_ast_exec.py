class A:
    def f(self, x):
        return [i * x for i in range(x)]

a = A()
b = a.f(3)
