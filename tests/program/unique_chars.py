str=input()
d={}
for i in str:
    d[i] = d.get(i,0) + 1

d=sorted(d.keys())
print(tuple(d))
