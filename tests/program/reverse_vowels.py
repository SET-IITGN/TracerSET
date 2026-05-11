S=input()
vowels='aeiouAEIOU'
S=list(S)
pos=[]
vow=[]
for i in range(len(S)):
    if S[i] in vowels:
        pos.append(i)
        vow.append(S[i])

pos=pos[::-1]
for i in range(len(pos)):
    S[pos[i]]=vow[i]
for i in S:
    print(i,end='')