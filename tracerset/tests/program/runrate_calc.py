L=input().split()

def req_run_rate(tar,curr,rem):
    if rem==0:
        print('NA',end='')
        exit()
    else:
        print(str(round((tar-curr)/rem,2)),end=' ')


ts=int(L[0])
cs=int(L[1])
co=int(L[2])
n=int(L[3])

S=[]
for _ in range(n):
    S.append([])

if (co >= 50):
    print('NA',end='')
    exit()
req=req_run_rate(ts,cs,50-co)
    
for i in range(1,n+1):
    L=input().split()
    if 'W' in L:
        while (L.count('W')!=0):
            L.remove('W')
    cs+=sum([int(i) for i in L])
    co+=1
    req=req_run_rate(ts,cs,50-co)