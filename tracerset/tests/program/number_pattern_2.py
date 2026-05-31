n=int(input())

X=[]
for i in range(2*n):
    if i%2!=0:
        X.append(i)
X=X[::-1]

for i in range(n):
    for j in range(1,2*n-X[i]):
        print(' ',end='')
    print(*range(1,X[i]+1))