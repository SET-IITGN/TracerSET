bs=float(input())
gs=0.0
hra=0.0
da=0.0

if (bs <= 10000):
    hra=0.2*bs
    da=0.8*bs
elif (bs > 10000 and bs <= 20000):
    hra=0.25*bs
    da=0.9*bs
else:
    hra=0.3*bs
    da=0.95*bs
    
ga=round((bs+hra+da),2)
print(ga)