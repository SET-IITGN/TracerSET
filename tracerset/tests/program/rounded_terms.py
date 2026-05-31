a=float(input())
b=float(input())
h=float(input())

a=a+h
while a<b:
    if a+h<b:
        print(round(a,6),end=",")
    else:
        print(round(a,6),end="")
    a=a+h
