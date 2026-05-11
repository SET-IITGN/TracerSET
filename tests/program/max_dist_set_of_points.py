n = int(input())
l = []
for i in range(n):
    l.append(tuple(map(int,input().split())))
maxi = -1e9
max_ans = []
for i in range(len(l)):
    for j in range(i+1,len(l)):
        dist = ((l[i][1]-l[j][1])**2+(l[i][0]-l[j][0])**2)**0.5
        if dist>maxi:
            maxi = dist
            max_ans = [l[i], l[j]]
print(round(maxi,2))
print(max_ans[0], max_ans[1])