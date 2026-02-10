
from abc import *
class Employee(metaclass=ABCMeta): #추상클래스
    def __init__(self,irum,nai):
        self.irum = irum
        self.nai = nai

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def data_print(self): 
        pass

    def irumnai_print(self):
        print('이름 :', self.irum + ', 나이 :', self.nai, end=', ')

class Temporary(Employee):
    def __init__(self, irum, nai, ilsu, ildang):
        Employee.__init__(self, irum, nai)
        self.ilsu = ilsu
        self.ildang = ildang

    def pay(self):
        return self.ilsu * self.ildang

    def data_print(self):
        super().irumnai_print()
        print('월급 :', self.pay())

class Regular(Employee):
    def __init__(self, irum, nai, salary):
        Employee.__init__(self, irum, nai)
        self.salary = salary

    def pay(self): 
        pass

    def data_print(self):
        super().irumnai_print()
        print('급여 :', self.salary)

class Salesman(Regular):
    def __init__(self, irum, nai, salary, sales, commission):
        Employee.__init__(self, irum, nai)
        self.sales = sales
        self.salary = salary
        self.commission = commission

    def pay(self): 
        return self.salary +(self.commission * self.sales)

    def data_print(self):
        super().irumnai_print()
        print('수령액 :', int(self.pay()))

t = Temporary('홍길동',25,20,150000)
r = Regular('한국인', 27, 3500000)
s = Salesman('손오공', 29, 1200000, 5000000, 0.25)

t.data_print()
r.data_print()
s.data_print()
