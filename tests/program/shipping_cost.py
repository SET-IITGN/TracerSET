def shipping_cost(w):        
    if w <= 2.0:
        return 6.0
    elif w <= 5.0:
        return 5.0
    elif w <= 10.0:
        return 4.0
    else:
        return 3.0

weight = float(input())
if weight <= 0.0:
    print (-1)
else:
    print (shipping_cost(weight)*weight)
