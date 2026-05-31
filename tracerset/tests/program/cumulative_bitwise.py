a=int(input())
b=int(input())
i=a
s1=0
s2=-1 #This is initialization is corrected by Bhavay Goyal. Thank you for catching this bug!
while i<=b:
    if i%2==0:
        s1=s1|i
        if i!=b:
            print(s1*~a,end=',')
        else:
            print(s1*~a,end='')
    else:
        s2=s2&i
        if i!=b:
            print(s2*~b,end=',')
        else:
            print(s2*~b,end='')
    i=i+1
