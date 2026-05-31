s=input()
c=0
m=0
for i in s:
    if i.islower():
        c+=1
        if c>m:
            m=c
    else:
        c=0
        
print(m)
