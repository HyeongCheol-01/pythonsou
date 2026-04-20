





import statsmodels.api as sm
from sklearn.datasets import make_regression
import numpy as np

np.random.seed(12)

#모델 맛보기
# 방법1 : make_regression 사용. model 생성 x
x, y, coef = make_regression(n_samples=50, n_features=1, bias=100, coef=True)
print(x)    # [-1.70073563]
print()
print(y)    # [ -52.17214291   39.34130801  128.51235594
print()
print(coef) # 89.47430739278907
# y = wx + b
y_pred = 89.47430739278907 * -1.70073563 + 100
print('예측값 :', y_pred)

xx=x
yy=y

print('\n방법2 : LinearRegression 사용. model 생성 O')
from sklearn.linear_model import LinearRegression
model = LinearRegression()
fit_model = model.fit(xx, yy)  # 최소제곱법으로 기울기, y절편을 반환
print('기울기(slope) :', fit_model.coef_)
print('절편(bias) :', fit_model.intercept_)
# 예측값 확인 함수
y_newpred = fit_model.predict(xx[[0]])
print('예측값1',y_newpred)
y_newpred2 = fit_model.predict(np.array([[0.12345]]))
print('예측값2',y_newpred2)

print('\n방법3 : ols 사용. model 생성 O')
# 잔차제곱합(RSS)을 최소화하는 가중치 벡터를 행렬 미분으로 구하는 방법
import statsmodels.formula.api as smf
print(xx.ndim)  # 2
x1 = xx.flatten()   # 차원 축소 xx.ravel()
print(x1.ndim)  # 1
y1=yy

import pandas as pd
data = np.array([x1,y1])
df = pd.DataFrame(data.T)
df.columns=['x1','y1']
print(df.head(3))

model2 = smf.ols(formula="y1 ~ x1", data=df).fit()
print(model2.summary())
print('기울기',model2.params['x1'])
print('절편',model2.params['Intercept'])
# 예측값 확인
new_df = pd.DataFrame({'x1':[-1.70073563, -0.67794537]})    # 기존 자료 검증
print('예측값1', model2.predict(new_df))
new_df2 = pd.DataFrame({'x1':[0.1245,0.2345]}) # 새로운 자료 검증
print('예측값2', model2.predict(new_df2))
