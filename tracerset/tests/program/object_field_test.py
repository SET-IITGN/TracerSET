class A:
    
    def __init__(self):
        self.a=5
        self.b=7   
    def update_a_by(self,val):
        self.a=self.a+val
    def update_b_by(self,val):
        self.b=self.b+val
    def display_state(self):
        print(f"a={self.a}, b={self.b}")
        
def main():
    x = A()
    x.update_b_by(8)
if __name__ == "__main__":
    main()
