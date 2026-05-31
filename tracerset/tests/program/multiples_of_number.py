nums = list(map(float, input().split(' ')))
for i in range(len(nums)):
    if i!=len(nums)-1:
        diff=abs(nums[i]-nums[i+1])
        summ=nums[i]+nums[i+1]
        diff=round(diff,2)
        summ=round(summ,2)
        if diff>summ:
            print('NONE')
        else:
            L=[]
            j=diff
            if diff == 0.00:
                L.append(0)
            else:
                ctr=1
                while j<=summ:
                    L.append(j)
                    ctr+=1
                    j=round(diff*ctr,2)
            L.sort()
            print(*L)