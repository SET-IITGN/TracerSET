from math import sqrt

a = int(input())
b = int(input())
c= int(input())

if a==0 and b==0:
    print("NO SOLUTION")
elif a==0:
    print("ONLY ONE REAL ROOT", round(-c/b,2))
else:
    k = ((b**2)-(4*a*c))
    if k<0:
        print("NO REAL ROOTS")
    else:
        x1 = round((-b + sqrt(k))/(2*a),2)
        x2 = round((-b - sqrt(k))/(2*a),2)
        print("TWO REAL ROOTS", x1, x2)
