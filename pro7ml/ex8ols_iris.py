# 단순선형회귀 - iris dataset
# 상관관계가 약한 경우와 강한 경우로 회귀분석모델을 생성 후 비교

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

iris = sns.load_dataset('iris')




result1 = smf.ols(formula='sepal_length ~ sepal_width', data = iris).fit()
print(result1.summary())
print('R-sqquared :', result1.rsquared)
print('p_value :', result1.pvalues)
#시각화
plt.scatter(iris.sepal_width, iris.sepal_length)
plt.plot(iris.sepal_width, result1.predict(), color='r')
plt.show()


result2 = smf.ols(formula='sepal_length ~ petal_length', data = iris).fit()
print(result2.summary())
print('R-sqquared :', result2.rsquared)
print('p_value :', result2.pvalues)     #  1.038667e-47 < 0.05 이 모델은 유의함
#시각화
plt.scatter(iris.petal_length, iris.sepal_length)
plt.plot(iris.petal_length, result2.predict(), color='r')
plt.show()

print('실제값 :', iris.sepal_length[:10].values)
print('예측값 :', result2.predict()[:10])



# 새로운 값으로 예측
new_data = pd.DataFrame({'petal_length': [1.1,0.5,6.0]})
y_pred = result2.predict(new_data)
print('예측결과:', y_pred)

column_select = "+".join(iris.columns.difference(['sepal_length','sepal_width','species']))
print(column_select)
result3 = smf.ols(formula='sepal_length ~' + column_select, data=iris).fit()
print(result3.summary())