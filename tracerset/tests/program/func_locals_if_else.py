a=6
def f():
    b=7
    c=9
    g()
    if c==8:
        b=7
        c=9
    else:
        if c==6:
            b=c
            b=b+1
            temp=a
            a=b
            b=temp
        else:
            g()
             
def g():
    b=8
    c=5
    if c%2==0:
        c=c-8
    else:
        pass
    
f()

