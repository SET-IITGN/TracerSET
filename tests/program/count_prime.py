n = int(input())
s=0
i=1
s=0
while i<=n:
    j=2
    f=1
    while j<i and f==1:
        if i%j==0:
            f=0
        j=j+1
    if f==1:
        p=0
        k=i
        while k>0:
            r=k%10
            if r==3:
                p=p+1
            k=k//10
        if p>0:
            s=s+1
    i=i+1
    
print(s)
