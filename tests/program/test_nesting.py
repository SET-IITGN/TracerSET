def a(x):
    def b(y):
        def c(z):
            return x + y + z
        return c(y)
    return b(x)

a(5)
