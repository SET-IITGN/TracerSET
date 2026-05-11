n=int(input())
c=1
v=n-1
for i in range(1,n+1):
    for j in range(1,2*v+1):
        print(' ',end='')
        
    for j in range(1,c+1):
        if j == c:
            print('*')
        else:
            print('*',end=' ')
    c+=2
    v-=1