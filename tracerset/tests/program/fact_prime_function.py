def isPrime(x):
    res=False
    if x<2:
        res=False
    else:
        i=2
        c=0
        while i<x:
            if x%i==0:
                c=c+1
            i=i+1
        if c==0:
            res=True
        else:
            res=False
    return(res)

def fact(k):
    f=0
    if k<=1:
        f=1
    else:
        i=1
        f=1
        while i<=k:
            f=f*i
            i=i+1
    return(f)

n=int(input())
s=0

while n>0:
    c=n%10
    if isPrime(c)==True:
        s=s+fact(c)
    n=n//10

print(s)
    
