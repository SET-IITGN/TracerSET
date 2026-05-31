import subprocess
import sys
n=int(input())
W=[]
f=open('students_data.txt','w')
for _ in range(n):
    k=input()
    L=k.split(',')
    D={}
    D['Id']=int(L[0].strip())
    D['Name']=L[1]
    D['Subject']=[L[2]]
    D['TotalMarks']=int(L[3].strip())
    flag=0
    for i in W:
        if (i['Id']==D['Id']):
            if (D['Subject'][0] not in i['Subject']):
                i['Subject'].extend(D['Subject'])
                i['TotalMarks'] += D['TotalMarks']
                flag=1
                break
            else:
                flag=2
                break
    if flag==0:
        W.append(D)
    f.write(k+'\n')
f.close()

f=open('students_data.txt','w')
for i in W:
    f.write("{'Id':"+str(i['Id'])+",'Name':"+i['Name']+",'Subject':"+str(i['Subject'])+",'TotalMarks': "+str(i['TotalMarks'])+"}\n")
f.close()

subprocess.run(["du","-b","students_data.txt"], stdout = sys.stdout)
subprocess.run(["cat","students_data.txt"], stdout = sys.stdout)