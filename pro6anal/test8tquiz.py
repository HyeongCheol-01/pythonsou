import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

# [one-sample t 검정 : 문제1]  
# 영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다. 
# 한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다. 
# 연구소의 발표결과가 맞는지 새로 개발된 백열전구를 임의로 수집하여 수명 시간 관련 자료를 얻었다. 
# 한국 연구소의 발표가 맞는지 새로운 백열전구의 수명을 분석하라.
# 수집된 자료 :  305 280 296 313 287 240 259 266 318 280 325 295 315 278
# 귀무 300시간이다.
# 대립 300시간이 아니다
data = [305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]
print(stats.shapiro(data))
# pvalue=0.820861 >0.05 정규성 만족함
result = stats.ttest_1samp(data, popmean=300)  # (데이터, 예상평균값(모수의 평균))
print(result)
# statistic=-1.55643, pvalue0.1436062
# 해석 : 유의수준 0.05 < pvalue 0.1436 귀무가설 채택 



# [one-sample t 검정 : 문제2] 
# 국내에서 생산된 대다수의 노트북 평균 사용 시간이 5.2 시간으로 파악되었다. A회사에서 생산된 노트북 평균시간과 차이가 있는지를 검정하기 위해서 A회사 노트북 150대를 랜덤하게 선정하여 검정을 실시한다.  
# 실습 파일 : one_sample.csv
# 참고 : time에 공백을 제거할 땐 ***.time.replace("     ", ""),
#           null인 관찰값은 제거.

# 귀무가설: A회사 노트북의 평균 사용 시간은 5.2시간이다. 
# 대립가설: A회사 노트북의 평균 사용 시간은 5.2시간이 아니다.
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/one_sample.csv")
data2['time'] = data2['time'].str.replace(" ", "")
data2['time'] = data2['time'].replace('', np.nan)
data2 = data2.dropna(subset=['time'])
data2['time'] = data2['time'].astype(float)
print(stats.shapiro(data2['time']))
# pvalue=0.7242 >0.05 정규성 만족함
result2 = stats.ttest_1samp(data2['time'], popmean=5.2)  # (데이터, 예상평균값(모수의 평균))
print(result2)
# statistic=3.94605, pvalue0.0001416
# 해석 : 유의수준 0.05 > pvalue 0.001416 귀무가설 기각 5.2시간 아님





# [one-sample t 검정 : 문제3] 
# https://www.price.go.kr/tprice/portal/main/main.do 에서 
# 메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
# 정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)
# 귀무가설: 평균 미용 요금이 15000원이다. 
# 대립가설: 평균 미용 요금이 15000원이 아니다.
df = pd.read_excel('개인서비스지역별_동향[2026-02월]331-0시52분.xls', header=1)
print(df)
price_list = []
for col in df.columns:
    try:
        val = float(col)
        if val > 1000: 
            price_list.append(val)
    except ValueError:
        continue
data3 = pd.Series(price_list)
print(stats.shapiro(data3))
# pvalue=0.08795 >0.05 정규성 만족함
result3 = stats.ttest_1samp(data3, popmean=15000)  # (데이터, 예상평균값(모수의 평균))
print(result3)
# statistic=7.1743, pvalue3.2057661925789937e-06
# 해석 : 유의수준 0.05 > pvalue 3.2057661925789937e-06 귀무가설 기각 15000원이 아님