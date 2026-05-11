n=int(input())
lines=[]
l1=[]
for i in range(n):
    line=input()
    lines.append(line)
    
f=open('file.txt', 'w')
for line in lines:
    f.write(line+'\n')
f.close()

f=open('file.txt', 'r')
a=f.read().split()
a.sort()
print("[", end='')
for i in range(0,len(a),1):
    if i!=len(a)-1:
        print(a[i], end=', ')
    else:
        print(a[i], end='')
    
print(']')

import subprocess

import sys

subprocess.run(["du","-a","file.txt"], stdout = sys.stdout)
    