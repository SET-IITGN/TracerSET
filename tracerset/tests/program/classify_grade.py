def classify_grade(g):
    if g<0 or g>100:
        return -1
    elif g >=90:
        return 'A'
    elif g>=80:
        return 'B'
    elif g>=70:
        return 'C'
    else:
        return 'D'

n=int(input())
print(classify_grade(n))
