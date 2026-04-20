import numpy as np
from scipy import stats
import pandas as pd
data= pd.read_csv()
#공분산
print(np.cov(data.친밀도, data.적절성))
print(np.cov(data.친밀도, data.만족도))
print(data.cov)


#상관계수
print(np.corrcoef(data.친밀도, data.적절성))
print(np.corrcoef(data.친밀도, data.만족도))
print()
print(data.corr())
print(data.corr(method='pearson'))  # 변수 연속형
print(data.corr(method='spearman')) # 변수 서열형
print(data.corr(method='kendall'))

# 만족도에 따른 다른 특성 사이의 상관관계
co_re = data.corr()
print(co_re['만족도'].sort_values(ascending=False))