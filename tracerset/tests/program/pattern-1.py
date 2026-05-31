n=int(input())

i=0
while i<n:
    j=i
    while j<n+i:
        print(j,end=' ')
        j=j+1
    i=i+1
    print('')
