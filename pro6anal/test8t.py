# * 단일 모집단의 평균에 대한 가설검정(one samples t teset) 
# 실습 예제 1 
# A 중학교 1학년 1반 학생들의 시험결과가 담긴 파일을 읽어 처리 
# 국어 점수 평균검정(80) student csv

# 귀무 : 학생들의 국어점수 평균은 80이다.
# 대립 : 학생들의 국어점수 평균은 80이 아니다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

pd.set_option('display.max_columns', None)
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv")
print(data.head())
print(data.describe())
print(data['국어'].mean())  # 72.9
print(len(data))    # 20    30행이 넘으면 중심극한정리에 의해 정규성을 따른다고 가정
# 30개가 넘지 않으므로 정규성 검정 실시
# Shapiro-Wilk 검정은 가설검정의 방법으로 데이터가 정규분포를 가지는 지에 대해 검정
# p값은 alpha 0.05보다 커야 정규성을 따른다고 할 수 있다.
print(stats.shapiro(data['국어'])) # pvalue=0.0129597
# alpha 0.05 > pvalue=0.0129597 정규성을 만족하지 않음

# 정규성을 만족하지 못한 경우 대안 (Wilcoxon)
# Wilcoxon : 비모수 검정 방법으로 정규성이 없을 때 적절한 선택이 될 수 있다.
wilcox_result = wilcoxon(data['국어'] - 80)
print("wilcox_result :", wilcox_result)
# wilcox_result: statistic=(74.0), pvalue=(0.39777620658898905)
# alpha 0.05 < pvalue=0.39777   이므로 귀무가설 채택

print()
result = stats.ttest_1samp(data['국어'], popmean=80)
print("result:", result)
#  TtestResult statistic = -1.3321801 pvalue=0.1985605
# alpha 0.05 < pvalue=0.1985605     이므로 귀무가설 채택

# 결론 : 정규성은 부족하나 귀무가설 채택이라는 동일 결론을 얻음
# 표본 수가 크다면 그냥 ttest_1samp을 써도 된다.
# 보고소 작성 시에는 "shapiro-wilk검정 결과 정규성 가정이 다소 위배되었으나
# 비모수 검정(wilcoxon) 결과도 동일하므로  ttest_1samp 결과를 신뢰할 수 있다."라고 명시한다.

print("--------------")
# 실습예제 2
# 여아신생아 몸무게의 평균 검정 수행 babyboom csv
# 여아신생아의 몸무게는 평균이 2800(g)으로 알려져 왔으나 이보다 더 크다는 주장이 나왔다.
# 표본으로 여아 18 명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검정해 보자

# 귀무 : 여아신생아의 몸무게는 평균이 2800(g)이다.
# 대립 : 여아신생아의 몸무게는 평균이 2800(g) 보다 크다.
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv")
print(data2.head(3))
print(data2.describe())
print()
fdata = data2[data2.gender == 1] # 여아:1, 남아:2
print(fdata, ' ', len(fdata)) # 18
print('여아 몸무게 평균 : ', np.mean(fdata.weight))   #  3132.4444
# 2800과 3132는 평균에 차이가 있는가?
print('여아 몸무게 표준편차 : ', np.std(fdata.weight))  #   613.7878

# One-sample t-test
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print("result2 :", result2)
# result : statistic=2.23318, pvalue=0.039268 np=17
# 해석1 (p값) : alpha 0.05 > pvalue=0.039268 이므로 귀무가설 기각 
# 해석2 (t분포표) : t값 2.23318, df=17, alpha=0.05, cv(임계값)?1.740 이므로 귀무가설 기각
#                  t값이 cv 값 오른쪽(귀무 기각영역)

print("~~~~~~~~~~~~~~~")
#선행조건인 정규성 검정을 한 경우
print(stats.shapiro(fdata['weight']))  # pvalue=0.0179847
# alpha 0.05 > pvalue=0.0179847 정규성을 만족하지 않음

# 정규성을 만족여부 시각화 1
sns.histplot(fdata['weight'], kde=True) # 왜곡된 데이터 분포를 확인
plt.show()

# 정규성을 만족여부 시각화 2 Quantile-Quantile plot
stats.probplot(fdata['weight'], plot=plt)   # Q-Q plot 상에서 잔차가 정규성을 만족하지 못함
plt.show()

# 정규성 만족 못해 wilcoxon 비모수 검정
result3 = wilcoxon(fdata['weight']-2800)
print("result3: ", result3)
# statistic=37.0, pvalue=0.034233
# 해석3 (p값) : alpha 0.05 > 0.034233 이므로 귀무가설 기각






