def fun(a,b,c=9):
    temp=a
    a=b
    b=temp
    s=a+b
    return s
        
def main():
    a=3
    b=4
    c=5
    fun(a=6,b=c,c=b)

if __name__ == "__main__":
    main()
