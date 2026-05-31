T = list(map(int,input().split(' ')))
Tp=[]
Tn=[]
for i in T:
    if(i < 0):
        Tn.append(i)
    else:
        Tp.append(i)

T=[]
for i in range(len(Tp)):
    T.append(Tp[i])
    T.append(Tn[i])

print(T)