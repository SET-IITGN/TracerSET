import subprocess
import sys

f=open('file.txt','a')
n=int(input())
arr=[]
for i in range(n):
    f.write(input()+'\n')

    
f.close()

subprocess.run(["du","-a","file.txt"], stdout = sys.stdout)
f=open('file.txt','r')
a=f.readlines()
b=[i[:-1:] for i in a]
for i in range(0,len(a)):
    if i%2==0:
        print(b[i])
f.close()