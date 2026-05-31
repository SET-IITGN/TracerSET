def skip_vowel(s):
    result=""
    for char in s:
        if char not in "aeiouAEIOU":
            result=result+char
    return result
s=input()
print(skip_vowel(s))
