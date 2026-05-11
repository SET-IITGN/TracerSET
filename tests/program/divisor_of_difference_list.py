nums = list(map(int, input().split(' ')))
for i in range(len(nums)):
    if i!=len(nums)-1:
        diff=abs(nums[i]-nums[i+1])
        L=[]
        for j in nums:
            if (j!=0 and diff%j == 0):
                L.append(j)
        L.sort()
        if(len(L)!=0):
            print(*L)
        else:
            print('0')