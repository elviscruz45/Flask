class Student:
    
    def __init__(self, name):
        self.casa = name

    @property
    def names(self):
        return self.casa
    
    
s = Student('Steve')
print(s.casa )
print(s.names )