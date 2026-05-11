string = input()
d={}
vowels = ('a','e','i','o','u')
for i in string:
    char = i.lower()
    if char in vowels:
        if char not in d:
            d[char]=1
        else:
            d[char]+=1
print(d)