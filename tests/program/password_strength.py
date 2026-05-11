def password_strength(password):
    upper=0
    lower=0
    digit=0
    space=0
    length=len(password)
    verdict=""
    
    for i in password:
        if (i >= 'A' and i <= 'Z'):
            upper += 1
        elif (i >= 'a' and i <= 'z'):
            lower += 1
        elif (i >= '0' and i<= '9'):
            digit += 1
        elif (i == ' '):
            space += 1
    
    if (upper > 0 and lower > 0 and digit > 0 and space == 0 and length >= 8):
        verdict="Strong"
    elif (length >=8 and (upper > 0 or lower > 0 or digit > 0 or space == 0)):
        verdict="Moderate"
    elif length<8:
        verdict="Weak"

    #print(upper,lower,digit,space)
    return(verdict)

passwd=input()
verdict=password_strength(passwd)
print(verdict)   
