# 공분산 / 상관계수
# 변수가 하나인 경우에는 분산은 거리와 관련이 있다.
# 변수가 두 개인 경우에는 분산은 방향을 가진다.

import numpy as np


# print(np.cov(np.arange(1,6), np.arange(2,7)))
# print(np.cov(np.arange(10,60), np.arange(20,70,10)))
# print(np.cov(np.arange(100,600), np.arange(20,700,100)))
# print(np.cov(np.arange(1,6), (3,3,3,3,3)))
# print(np.cov(np.arange(1,6), np.arange(6,1,-1)))

print()
x = [8,3,6,6,9,4,3,9,3,4]
y = [6,2,4,6,9,5,1,8,4,5]

import matplotlib.pyplot as plt
print('x,y 의 공분산:',np.cov(x,y))
print('x,y 의 상관계수 :', np.corrcoef(x,y))    # 피어슨 상관계수
print('x,y 의 상관계수 :', np.corrcoef(x,y)[0,1])

from scipy import stats
print("scipy 모듈 사용:", stats.pearsonr(x,y))