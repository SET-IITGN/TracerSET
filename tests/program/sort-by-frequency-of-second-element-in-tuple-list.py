def xsort(t):
    d={}
    for i in t:
        if i[1] in d.keys():
            d[i[1]]+=1
        else:
            d[i[1]]=1
    
    for i in range(len(t)-1):
        for j in range(i+1,len(t)):
            if d[t[i][1]]<d[t[j][1]]:
                temp=t[j]
                t[j]=t[i]
                t[i]=temp
    return t
        
n=int(input())
t=[]
for i in range(n):
    m=input()
    n=input()
    a=(m,n)
    t.append(a)
t=xsort(t)
for i in t:
    x=[str(i[0]),str(i[1])]
    print(tuple(x))
