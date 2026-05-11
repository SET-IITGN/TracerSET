t1 = input().split(',')
t2 = input().split(',')

subset = True

for i in t1:
    if i not in t2:
        subset = False

print(subset)
