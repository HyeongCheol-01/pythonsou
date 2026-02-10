# Module : 소스 코드의 재사용을 가능하게 하며, 소스 코드를 하나의 이름 공간으로 구분하고 관리.
# 하나의 파일은 하나의 모듈이 된다.
# 표준 모듈, 사용자 작성 모듈, 제3자 모듈(third party)로 구분 할 수 있다.
print(print.__module__) #builtins

print('뭔가를 하다가... 외부 모듈사용하기')
import sys
print(sys.path)
a=5
if a>7:
    sys.exit()

import math
print(math.pi)

import calendar
calendar.setfirstweekday(6)
calendar.prmonth(2026,2)
del calendar

import random  #모듈
print(random.random())
print(random.randrange(1,10))

from random import random, choice, randrange # from 모듈 import 멤버
from random import *
print(random())
print(randrange(1,10))
print('end')
