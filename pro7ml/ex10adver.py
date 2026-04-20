import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 1. 데이터 로드 (Advertising 데이터셋)
# 1~4열(TV, Radio, Newspaper, Sales)만 선택하여 로드
advdf = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv", usecols=[1,2,3,4])

# 2. 데이터 기초 탐색
print("--- 데이터 상위 3행 및 구조 ---")
print(advdf.head(3), advdf.shape)
print("\n--- 데이터 요약 정보 ---")
print(advdf.info())

# 3. 상관관계 분석
# 변수들 간의 선형적 관계 확인 (Sales와 TV의 높은 상관관계 확인 가능)
print("\n--- 상관계수 행렬 ---")
print(advdf.corr())

# 4. 선형 회귀 모델 생성 및 학습 (단순 선형 회귀: sales ~ tv)
# 공식: Sales = Intercept + (tv * Slope)
lm = smf.ols(formula='sales ~ tv', data=advdf).fit()

# 5. 회귀 분석 결과 출력
print("\n--- 회귀 분석 전체 결과 요약 ---")
print(lm.summary())

print("\n--- 회귀 계수(Coefficients) 테이블 ---")
print(lm.summary().tables[1])

# 6. 새로운 데이터를 통한 예측 준비 (예제: 상위 3개 데이터 활용)
x_new = pd.DataFrame({'tv': advdf.tv[:3]})
print("\n--- 예측을 위한 새로운 데이터(TV 광고비) ---")
print(x_new)

# 7. 예측 수행
pred = lm.predict(x_new)
print("\n--- 예측된 Sales 값 ---")
print(pred)

# (선택 사항) 시각화: 회귀선 확인
# sns.regplot(x='tv', y='sales', data=advdf)
# plt.title("TV 광고비에 따른 판매량 회귀 분석")
# plt.show()