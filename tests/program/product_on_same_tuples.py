l = list(map(int, input().split()))
n = len(l)
ans = 0

for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                f={}
                f[str(a)]=0
                f[str(b)]=0
                f[str(c)]=0
                f[str(d)]=0
                L=list(f.keys())
                if len(L)==4:
                    if l[a]*l[b]==l[c]*l[d]:
                        ans+=1
print(ans)