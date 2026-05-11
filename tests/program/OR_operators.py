n = int(input())
sum = 0
d = 0
k = n

while k:
    d = d+1
    k = k//10

i=1
while i<=n:
    sum = sum | i
    i=i+1

print(sum * d)
