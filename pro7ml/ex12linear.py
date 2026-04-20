import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

# 1. 데이터 생성
sample_size = 100
np.random.seed(1)

# 독립변수 x와 종속변수 y 생성 (선형 관계에 노이즈 추가)
x = np.random.normal(0, 10, sample_size)
y = np.random.normal(0, 10, sample_size)

# sklearn 입력 형식을 위해 2차원 배열로 변환
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)

# 2. 데이터 정규화 (MinMaxScaler)
# 데이터를 0과 1 사이의 값으로 변환하여 학습 안정성 확보
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x)

# 3. 모델 생성 및 학습
model = LinearRegression()
model.fit(x_scaled, y)

# 4. 예측 수행
y_pred = model.predict(x_scaled)

# 5. 모델 평가 (Score 정리)


# 결정계수 (R-squared): 1에 가까울수록 모델의 설명력이 높음
r2 = r2_score(y, y_pred)

# 설명 분산 점수 (Explained Variance Score): 모델이 데이터의 변동성을 얼마나 잘 잡아내는지 측정
evs = explained_variance_score(y, y_pred)

# 평균제곱오차 (MSE): 예측값과 실제값 차이의 제곱 평균. 작을수록 우수함
mse = mean_squared_error(y, y_pred)

# 평균제곱근오차 (RMSE): MSE에 루트를 씌워 실제 단위와 맞춘 값
rmse = np.sqrt(mse)

print("--- [회귀 모델 평가 지표 요약] ---")
print(f"1. 결정계수 (R2 Score)        : {r2:.4f}")
print(f"2. 설명 분산 점수 (EVS)       : {evs:.4f}")
print(f"3. 평균제곱오차 (MSE)         : {mse:.4f}")
print(f"4. 평균제곱근오차 (RMSE)      : {rmse:.4f}")

# 6. 시각화
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='skyblue', label='Actual Data', alpha=0.7)
plt.plot(x, model.predict(scaler.transform(x)), color='red', linewidth=2, label='Regression Line')
plt.title("Linear Regression: Actual vs Predicted (Scaled Input)")
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()