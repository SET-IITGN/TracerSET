size = int(input())
 
# printing the inverted triangle
for a in range(0, size):
    for b in range(a, size):
        print(" ", end = "")
    for b in range(1, (a * 2)): 
        print("*", end = "") 
    print("")
 
# printing rest of the heart
for a in range(size, int(size / 2) - 1 , -2):
 
    # printing the white space right-triangle
    for b in range(1, size - a, 2):  
        print(" ", end = "")
 
    # printing the first trapezium
    for b in range(1, a + 1): 
        print("*", end = "")
 
    # printing the white space triangle
    for b in range(1, (size - a) + 1): 
        print(" ", end = "")
 
    # printing the second trapezium
    for b in range(1, a): 
        print("*", end = "")
 
    # new line
    print("")