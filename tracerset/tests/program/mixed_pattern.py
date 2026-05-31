x=int(input())
if x<=0:
    print('Invalid')
    exit()
y=int(input())
if y<=0:
    print('Invalid')
    exit()
z=int(input())
if z<=0:
    print('Invalid')
    exit()

if x<=0 or y<=0 or z<=0:
    print('Invalid')
    exit()

for i in range(x):
    for j in range(y):
        for k in range(z):
            print('*',end=' ')
        print('#')
    if i%2==0:
        print('%')
    else:
        print('@')