guest_list = list(input().split(' '))
G=[]

for i in guest_list:
    if i not in G:
        G.append(i)

print(G)