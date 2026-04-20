# 방법4 make_regression 사용. model 생성 X


from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# IQ에 따른 시험 점수 예측
score_iq = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/score_iq.csv")
print(score_iq.head(3))
print(score_iq.info())
x = score_iq.iq
y = score_iq.score
print(x[:3])
print(y[:3])

print('상관 계수 : ', np.corrcoef(x,y)[0,1])
print(score_iq[['iq','score']].corr())

# plt.scatter(x,y)
# plt.show()

# 단순 선형회기분석 ( 인간관계가 있다는 가정하에 진행)
model = stats.linregress(x,y)
print(model)
print('기울기', model.slope)
print('절편', model.intercept)
print('p값', model.pvalue)

plt.scatter(x,y)
plt.plot(x,model.slope * x + model.intercept, c='r')
plt.show()




newdf = pd.DataFrame({'iq':[55,66,77,88,150]})
print('점수예측 :\n', np.polyval([model.slope, model.intercept], newdf))