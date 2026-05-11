n=int(input())
s=0
c=0
try:
    while True:
        c=c+1
        k=int(input())
        if k%2!=0:
            c=c-1
            continue
        s=s+k
        #print(f"{c} {k} {s}")
        if s>=n:
            break
    print(c)
except:
    print("Stuart Kaal Aana!")
