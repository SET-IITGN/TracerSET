l = input().split()
n = input()
found = False
for i in range(0, len(l)):
    if (n == l[i]):
        print(i)
        found = True
        break
if found == False:
    print(-1)
