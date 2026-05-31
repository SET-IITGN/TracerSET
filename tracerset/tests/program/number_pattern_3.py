n=int(input())

for j in range(1,n+1):
    if j==1 or j==n:
        for i in range(1,n+1):
            if i!=n:
                print(i,end=' ')
            else:
                print(i)
    else:
        for i in range(1,n+1):
            if i==1:
                print(i,end=' ')
            elif i==n:
                print(i)
            else:
                print(' ',end=' ')
