import subprocess
import sys

n=int(input())
f=open('text_file.txt','w')
line=[]
F=[]
for i in range(n):
    line=input()
    F.append(line+'\n')
f.close()
k=int(input())

d={}
for line in F:
    for word in line.split():
        d[word]=d.get(word,0)+1
print(d)

for i in range(len(F)):
    F[i]=F[i].split()

count=0
for i in range(len(F)):
    for word,freq in d.items():
        if freq > k:
            while F[i].count(word) != 0:
                F[i].remove(word)
    count+=len(F[i])
    F[i]=' '.join(F[i])+'\n'

f=open('text_file.txt','w')    
for i in range(len(F)):
    f.write(F[i])
f.close()

subprocess.run(["du","-b","text_file.txt"], stdout = sys.stdout)
print(count)