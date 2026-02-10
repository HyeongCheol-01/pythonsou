class Car:
    handle = 1
    speed = 0

    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def showData(self):
        km = "킬로미터"
        msg = "속도:" + str(self.speed) + km
        return msg

    def printHandle(self):
        return self.handle
    
print(Car.handle) # 원형(prototype) 클래스의 멤버 호출
car1 = Car('tom', 10) # 생성자 호출 후 객체 생성(인스턴스화)
print('car1 객체 주소:', car1)
print('car1 :', car1.name, ' ', car1.speed, car1.handle)
car1.color = '파랑'
print('car1.color : ', car1.color)

car2 = Car('John', 20) # 생성자 호출 후객체 생성(인스턴스화)
print('car2 객체주소:',car2)
print('car2 :', car2.name, ' ', car2.speed, car2.handle)

print(Car, car1, car2)
print(id(Car), id(car1), id(car2))
print(car1.__dict__)
print(car2.__dict__)

print('---메소드---------------')
print('car1 speed: ' , car1.showData())
print('car2 speed: ' , car2.showData())
car1.speed = 80
car2.speed = 110

print('car1.handle :', car1.printHandle())
print('car2.handle :', car2.printHandle())