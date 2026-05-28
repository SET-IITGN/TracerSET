def fun(a,b):
    c=0
    try:
        c=a/b
    except:
        c=0
    return c
    
def gun(a,b):
    k=fun(a,b)
    if k%2==0:
        return 1
    else:
        return -1

if __name__ == "__main__":        
    print(gun(4,0))
