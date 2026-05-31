f=int(input())
c=(5/9)*(f-32)
c=round(c,2)

print(c)
if c <= 0:
    print('Freezing weather')
elif 0 < c <= 10:
    print('Very Cold weather')
elif 10 < c <= 20:
    print('Cold weather')
elif 20 < c <= 30:
    print('Normal in Temp')
elif 30 < c <= 40:
    print("It's Hot")
elif c > 40:
    print("It's Very Hot")
    