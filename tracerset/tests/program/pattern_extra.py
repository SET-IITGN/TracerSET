n=int(input())
c=1
v=n-1
i=1
while i<=n:
    j=1
    while j<=2*v:
        print(' ',end='')
        j=j+1
    j=1    
    while j<=c:
        if j==c:
            print('*')
        else:
            print('*',end=' ')
        j=j+1
    c+=2
    v-=1
    i=i+1
    
