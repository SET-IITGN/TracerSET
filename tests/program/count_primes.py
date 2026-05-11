def isPrime(n):
    if n==1:
        return False
    if n==2:
        return True
    for i in range(2,n-1):
        if n%i==0:
            return False
    return True
n = int(input())
s=0
for i in range(1,n+1):
    if isPrime(i):
        if '3' in str(i):
            s+=1
print(s)