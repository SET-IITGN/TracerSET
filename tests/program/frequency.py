S=input()
d={}
for i in S:
    d[i]=d.get(i,0)+1

L=[(v,k) for (k,v) in d.items()]
L=sorted(L, reverse=True)
low=L[-1][1]
high=L[0][1]
S=S.replace(high,'\0')
S=S.replace(low,high)
S=S.replace('\0',low)
print(S)