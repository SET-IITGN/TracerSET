str=input()
t=()
for i in range(0,len(str)):
    first=str[0:i]
    second=str[i+1:]
    if (str[i] in first or str[i] in second) and str[i] not in t:
        t+=(str[i],)

print(t)
        