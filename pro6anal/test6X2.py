# 이원카이제곱 
# 동질성 검정(Homogeneity Test): 서로 다른 두 개 이상의 집단에서 추출한 범주형 데이터의 분포가 동일한지, 
# 즉 표본들이 동질적인지를 교차표(Contingency Table)를 사용하여 검정하는 통계 방법
# 분포 비율 차이 검정
# 두 집다 이상에서 각 범주 집단 간의 비율이 서로 동일한가를 검정

# 동질성 검정 실습 1:
# 교육방법(독립변수)에 따른 교육생들의 만족도(종속변수) 분석 동질성 검정
# survey_method csv

# 귀무 : 교육방법에 따른 교육생들의 만족도에 차이가 없다.
# 대립 : 교육방법에 따른 교육생들의 만족도에 차이가 있다.
import pandas as pd
import scipy.stats as stats

# 만족도에 대한 설문조사 수집 자료
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv")
print(data.head(3))
print(data['method'].unique())  #[1 2 3]
print(data['survey'].unique())  #[1 2 3 4 5]

ctab = pd.crosstab(index=data['method'], columns=data['survey'])
print(ctab)
ctab.index = ["방법1","방법2","방법3"]
ctab.columns = ['매우만족','만족','보통','불만족','매우불만족']
print(ctab) # 분포 비율

chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f"chi2: {chi2:.4f} p-value: {p:.7f} 자유도(dof): {dof}")
# chi2: 6.5447 p-value: 0.5864574 자유도(dof): 8
print("expected:\n", expected)  # 예측 비율

#해석 : 유의수준 0.05< p:0.5864574 이므로 귀무 채택 

print('--------')
# 동질성 검정 실습 2) 연련대별 sns이용률의 동질성 검정
# 20대에서 40대까지 연령대별로 서로 조금씩 그 트겅이 다른 SNS 서비스들에 대해 이용 현황을
# 조사한 자료를 바탕으로 연령대별로 홍보전략을 세우고자 한다
# 연령대별로 이용 현황이 서로 동일한지 검정해 보도록 하자

# 귀무 : 연령대별로 sns 서비스별 이용율 현황은 동일(동질)하다.
# 대립 : 연령대별로 sns 서비스별 이용율 현황은 동일(동질)하지 않다.

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv")
print(data.head())

print(data["age"].unique())     # [1 2 3] 20, 30, 40
print(data["service"].unique())   # ['F' 'T' 'K' 'C' 'E']

ctab2 = pd.crosstab(index=data['age'], columns=data['service'])
print(ctab2)
chi2, p, dof, expected = stats.chi2_contingency(ctab2)
print(f"chi2: {chi2} p-value: {p} 자유도(dof): {dof}")
# chi2: 102.75202494484225 p-value: 1.1679064204212775e-18 자유도(dof): 8
# 판정 : p-value: 1.1679064204212775e-18 < 0.05 이므로 귀무가설 기각
# 연령대별로 sns서비스별 이용율 현황은 동일하지 않다. 의견을 인정함

print("~~~~~~~~~~")
print("전체 건수 : ", len(data))    # 1439
# 위 자료는 샘플 자료이겠으나 모집단이라 가정하고 샘플링 후 검정
samp_data = data.sample(n=500, replace=True, random_state=1)
print(samp_data.head(), ' ', len(samp_data))

ctab3 = pd.crosstab(index=samp_data['age'], columns=samp_data['service'])
print(ctab3)
chi2, p, dof, expected = stats.chi2_contingency(ctab3)
print(f"chi2: {chi2} p-value: {p} 자유도(dof): {dof}")



