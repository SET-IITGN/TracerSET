import subprocess
import sys

i=int(input())
f=open("file.txt",'a')
l=[]
le=[]
for n in range(i):
    s=input()
    l.append(s.split())
    le.append(len(s.split()))
    f.write(s)
a=min(le)
ans=[["" for x in range(len(l))] for i in range(a)]
for i in range(0,len(l)):
    for j in range(0,a):
        ans[j][i]=l[i][j]
f.close()
for i in ans:
    print(*i)
    
subprocess.run(["du","-a","file.txt"], stdout = sys.stdout)