x = input().strip("(").strip(")").split(",")
for i in range(len(x)):
    x[i] = int(x[i])

y = tuple(x)
max = float('-inf')
for i in range(len(y)):
    for j in range(len(y)):
        if i == j :
            continue
        else:
            if y[i]*y[j]>max:
                max = y[i]*y[j]

print(f'Maximum product: {max}')