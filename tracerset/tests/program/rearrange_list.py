nums = list(map(int, input().split(' ')))
L=[[],[],[]]
for i in nums:
    if i < 0:
        L[0].append(i)
    elif i==0:
        L[1].append(i)
    else:
        L[2].append(i)

L=L[0]+L[1]+L[2]
print(L)