import math

def isPerfect(n):
    s=0
    for i in range(1,n):
        if n%i==0:
            s+=i
  
    if s==n:
        return True
    else:
        return False

a=int(input())
b=int(input())

if b<a: 
    print("INVALID INPUT")
    exit()

if a <= 0:
    a *= -1
    b += a+1
    a = 1

print(a)
print(b)

i=a
while i<=b:
    if isPerfect(i) == True:
        print(round(math.log(i),2))
    i=i+1
