n=int(input())

for i in range(1,n+1):
    num=65
    for j in range(n,0,-1):
        if j<=i:
            print(chr(num),end=' ')
            num+=1
        else:
            print(' ',end=' ')
    print('')
            
