def fun(a,b,c=9):
    temp=a
    a=b
    b=temp
    s=a+b
    return s
        
def main():
    fun(b=5,a=4)

if __name__ == "__main__":
    main()
