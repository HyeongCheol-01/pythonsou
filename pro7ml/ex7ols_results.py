# 단순선형회귀 : ols의 Regression Results의 이해
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinking_water.csv")




model=smf.ols(formula='만족도 ~ 적절성', data=df).fit()
print(model.summary())
print('parameters :', model.params)
print('R-sqquared :', model.rsquared)
print('p_value :', model.pvalues)
print('예측값 :', model.predict()[:5])
print('실제값 :', df.만족도[:5].values)

plt.scatter(df.적절성, df.만족도)
slope, intertception =np.polyfit(df.적절성,df.만족도)
plt.plot(df.적절성)
plt.show()






