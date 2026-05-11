n = int(input())

a = [tuple(map(int, input().split())) for _ in range(n)]

mini, minv = float('inf'), -1
for i in range(n):
    for j in range(i+1, n):
        if (a[i][0] - a[j][0]) ** 2 + (a[i][1] - a[j][1]) ** 2 < mini:
            mini = (a[i][0] - a[j][0]) ** 2 + (a[i][1] - a[j][1]) ** 2
            minv = a[i], a[j]

print(minv)