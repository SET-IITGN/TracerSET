S1=input()
S2=input()
d1={}
d2={}
def isIsomorphic(S1,S2):
    for i in range(len(S1)):
        d1[S1[i]]=S2[i]
        d2[S2[i]]=S1[i]
    return(len(d1)==len(d2))

if(isIsomorphic(S1,S2)==True):
    print('Yes')
else:
    print('No')