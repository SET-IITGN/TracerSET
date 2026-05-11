import math

def EOQ(d,s,h):
    k=(2*d*s)/h
    res=math.sqrt(k)
    return(res)

def TBO(d,s,h):
    k=(2*s)/(d*h)
    res=math.sqrt(k)
    return(res)

d=int(input())
s=int(input())
h=int(input())

k=0.1
sum=0.0

while k <= 1.0:
    sum += k*EOQ(d,s,h) + (1-k)*TBO(d,s,h)
    k += 0.1

sum=round(sum,2)
print(sum)
