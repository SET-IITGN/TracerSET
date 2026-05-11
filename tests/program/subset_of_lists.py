n = list(map(int, input().strip().split()))
print("[]")
for i in range (len(n)):
    print([n[i]])
    for j in range (i+1,len(n)):
        print([n[i], n[j]])
        for k in range (j+1, len(n)):
            print([n[i], n[j], n[k]])
            for l in range (k+1, len(n)):
                print([n[i], n[j], n[k], n[l]])
                for m in range (l+1, len(n)):
                    print([n[i], n[j], n[k], n[l], n[m]])