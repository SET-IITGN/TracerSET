a = [1, 2, 3]
b = a
c = b

print(id(a))
print(id(b))
print(id(c))

print(repr(a))
print(repr(b))
print(repr(c))

x = []

def f():
    a = x
    b = a
    print(a, b)

f()
