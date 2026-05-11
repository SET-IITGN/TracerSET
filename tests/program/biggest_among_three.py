a=int(input())
b=int(input())
c=int(input())

biggest=-1
if a<b:
    biggest=b
    if c>biggest:
        biggest=c
else:
    biggest=a
    if c>biggest:
        biggest=c
print(biggest)
