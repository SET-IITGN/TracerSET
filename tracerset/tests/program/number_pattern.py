n=int(input())
L=[]
for i in range(n):
    L.append([i+1])
    
X=[]
for i in range(2*n):
    if i%2!=0:
        X.append(i)
        
for i in range(n):
    for j in range(1,n):
        if j%2!=0:
            L[i].append(L[i][len(L[i])-1]+2*n-X[i])
        else:
            L[i].append(L[i][len(L[i])-1]+X[i])
    
for i in L:
    print(*i)