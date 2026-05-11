def calculate_average_grade(t):
    t=sorted(t)
    return sum(t)/len(t)

n=int(input())
d={}
for i in range(n):
    roll=int(input())
    name=input()
    grades=tuple(map(int,input().split(',')))
    d[name]=calculate_average_grade(grades)
for i in d:
    print(i+':',d[i])