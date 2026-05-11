def star_hash(n,c):
    for i in range(1,n+1):
        for j in range(1,i+1):
            print(c,end='')
        print('')

def print_pattern(m, n):
    if not ((m == 12 or m == 21) and (n>0 and n<=20)):
        print(-1)
        return
    if m == 12:
        star_hash(n,'*')
        star_hash(n,'#')
    elif m == 21:
        star_hash(n,'#')
        star_hash(n,'*')
        
m = int(input())
n = int(input())
print_pattern(m, n)