import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
import statsmodels.api as sm
import koreanize_matplotlib

# 1. 데이터 로드 (statsmodels 내장 데이터셋 활용)
# mtcars: 32개 자동차 모델의 11개 성능 지표를 담은 데이터셋
mtcars = sm.datasets.get_rdataset("mtcars").data

print("--- [1] 데이터셋 구조 확인 ---")
print(mtcars.head(3))
print(f"데이터 크기: {mtcars.shape}")

# 2. 독립변수(X)와 종속변수(y) 설정
# hp(마력), wt(무게)를 독립변수로, mpg(연비)를 종속변수로 설정
# sklearn 모델 입력을 위해 X는 2차원 배열 형태여야 함
X = mtcars[['hp', 'wt']]
y = mtcars['mpg']

# 3. 모델 생성 및 학습
model = LinearRegression()
model.fit(X, y)

# 4. 예측 수행
y_pred = model.predict(X)

# 5. 모델 평가 (Evaluation Score 정리)
# 결정계수 (R-squared): 1에 가까울수록 모델의 설명력이 높음
r2 = r2_score(y, y_pred)

# 설명 분산 점수 (EVS): 모델이 데이터의 변동성을 얼마나 잘 잡아내는지 측정
evs = explained_variance_score(y, y_pred)

# 평균제곱오차 (MSE): 예측 오차의 제곱 평균. 작을수록 우수함
mse = mean_squared_error(y, y_pred)

# 평균제곱근오차 (RMSE): MSE에 루트를 씌워 실제 단위와 맞춘 값
rmse = np.sqrt(mse)

print("\n--- [2] 회귀 모델 평가 결과 ---")
print(f"1. 결정계수 (R2 Score)        : {r2:.4f}")
print(f"2. 설명 분산 점수 (EVS)       : {evs:.4f}")
print(f"3. 평균제곱오차 (MSE)         : {mse:.4f}")
print(f"4. 평균제곱근오차 (RMSE)      : {rmse:.4f}")

# 6. 회귀 계수(Coefficient) 및 절편(Intercept) 확인
print("\n--- [3] 모델 파라미터 ---")
print(f"절편(Intercept): {model.intercept_:.4f}")
for col, coef in zip(X.columns, model.coef_):
    print(f"{col} 변수 계수: {coef:.4f}")

# 7. 시각화: 실제값 vs 예측값 비교
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, color='blue', alpha=0.6, label='실제 vs 예측')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='이상적 예측선')

plt.title("mtcars 연비 예측 성능 분석", fontsize=14)
plt.xlabel("실제 연비 (Actual MPG)", fontsize=12)
plt.ylabel("예측 연비 (Predicted MPG)", fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.show()