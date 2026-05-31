class Animal:
    
    def __init__(self):
        print("explicit constructor")
    
    def sound(self):  # Added 'self' parameter
        print("Animal made a sound!")
        
def main():
    print("Inside main()")
    a = Animal()
    a.sound()

if __name__ == "__main__":
    main()
