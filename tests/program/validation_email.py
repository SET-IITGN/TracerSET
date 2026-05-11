import subprocess
import sys

x=int(input())
z=[]
l=0
with open ('file.txt','w') as d:
    for i in range(x):
        y=input()
        d.write(y)
        z.append(y)
for j in z:
    if '@' in j:
        a=True
    else:
        a=False
    try:
        p=j.index('@')
        if '.' in j[p:]:
            b=True
        else:
            b=False
    except:
        b=False
   
    for k in j:
        if k.isalpha() or 48<=ord(k)<=57 or k=='.' or k=='+' or k=='@':
            c=True
        else:
            c=False
            break
    if a and b and c:
        l=l+1
print(l)

subprocess.run(["du","-a","file.txt"], stdout = sys.stdout)