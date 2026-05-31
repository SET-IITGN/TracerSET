n=int(input())
s=0
for i in range(n,0,-1):
    for j in range(1,i+1):
        s += 1
        print(s,end=' ')
    print('')
        