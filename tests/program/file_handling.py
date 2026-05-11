import subprocess
import sys

def satisfy(a,k):
    sum=0
    res=False
    for i in a:
        sum += 1 if ((i.islower()) and (i not in 'aeiou')) else 0
    if sum==k:
        res=True
    return(res)

n=int(input())
L=[]
f=open('user_input.txt','w')
for i in range(n):
    x=input()
    f.write(x+'\n')
    L.append(x)
k=int(input())
T=[]
for i in L:
    for j in i.split():
        if ((j not in T) and (satisfy(j,k)==True)):
            T.append(j)
f.close()
subprocess.run(["du","-b","user_input.txt"], stdout = sys.stdout)
print(T)