s = input()
res = 0
for i in s:
    if not 'A'<=i<='Z':
        print(res)
        exit()
    else:
        res += 1
print(res)
