def skip_consonants(s):
    new = ""
    for char in s:
        if char in "aeiou":
            new+=char
    return new

s = input()
print(skip_consonants(s))
