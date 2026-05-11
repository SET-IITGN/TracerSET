S=input()
score_p1=0
score_p2=0
ctr=0
turn=0
ctr=0
while len(S)!=0:
    turn=(turn+1)%2
    k=ord(S[0])
    S=S[1:]
    if(k%2==0):
        S=S[::-1]
    match turn:
        case 1:
            score_p1 += k
        case 0:
            score_p2 += k
            
print(str(score_p1-score_p2))