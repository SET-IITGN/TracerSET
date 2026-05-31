hardness = int(input())
carbon_content = float(input())
tensile_strength = int(input())

grade = 5

if hardness > 50 and carbon_content < 0.7 and tensile_strength > 5600:
    grade = 10
elif hardness > 50 and carbon_content < 0.7:
    grade = 9
elif carbon_content < 0.7 and tensile_strength > 5600:
    grade = 8
elif hardness > 50 and tensile_strength > 5600:
    grade = 7
elif hardness > 50 or carbon_content < 0.7 or tensile_strength > 5600:
    grade = 6

print(grade)
