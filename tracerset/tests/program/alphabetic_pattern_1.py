n = int(input())
s = 65
for i in range(1,n+1):
    for j in range(i):
        print(chr(s),end=' ')
        s += 1
    s=65
    print()
