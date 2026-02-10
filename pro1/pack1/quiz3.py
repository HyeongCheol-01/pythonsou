class Animal:
    def move(self):
        pass

class Dog(Animal):
    def name(self):
        print('개')
    def move(self):
        print('move개')

class Cat(Animal):
    def name(self):
        print('고양이')
    def move(self):
        print('move고양이')


class Wolf(Dog,Cat):
    pass

class Fox(Cat,Dog):
    def move(self):
        print('move여우')

    def foxMethod(self):
        self.name
        super().name()
        
        pass


w=Wolf()
w.name()
w.move()

f=Fox()
f.name()
f.move()