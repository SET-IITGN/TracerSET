n=int(input())
for i in range(1,n+1):
    for j in range(1,i+1):
        print(i,end=' ')
    for k in range(j+1,n+1):
        print(k,end=' ')
    print('')
    