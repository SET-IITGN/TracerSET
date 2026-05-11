n = int(input())
k = 1
a = n
sum = 0

while k<=n and a>=1:
    sum += k/a
    k = k+1
    a = a-1

print(round(sum,2))