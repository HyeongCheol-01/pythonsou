import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib # 한글 폰트 깨짐 방지
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor # Classifier가 아닌 Regressor 사용!
from sklearn.metrics import mean_squared_error, r2_score

print("=== [ex30rf_regressor] 랜덤 포레스트 회귀 (캘리포니아 집값 예측) ===")

# ---------------------------------------------------------
# 1. 데이터 로드 및 확인
# ---------------------------------------------------------
print("캘리포니아 주택 데이터를 불러오는 중입니다...")
# as_frame=True 옵션을 주면 곧바로 Pandas DataFrame 형태로 꺼낼 수 있습니다.
california = fetch_california_housing(as_frame=True)

X = california.data     # 8개의 독립변수 (특성)
y = california.target   # 종속변수 (집값, 단위: 10만 달러)

print(f"데이터 크기: {X.shape}")
print(X.head(3))

# ---------------------------------------------------------
# 2. Train / Test 데이터 분할
# ---------------------------------------------------------
# 집값 예측 같은 회귀 문제에서는 stratify 옵션을 쓰지 않습니다! (연속된 숫자라 비율을 나눌 수 없음)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------------------------------------------------
# 3. 랜덤 포레스트 회귀 모델 생성 및 학습
# ---------------------------------------------------------
# n_estimators=100: 100개의 회귀 트리를 만들어 평균값을 예측합니다.
rf_model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)

print("\n모델 학습 중...")
rf_model.fit(X_train, y_train)

# ---------------------------------------------------------
# 4. 예측 수행 및 성능 평가
# ---------------------------------------------------------
y_pred = rf_model.predict(X_test)

# 회귀 모델의 대표적인 평가 지표 계산
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse) # MSE에 루트를 씌워 실제 집값 단위와 맞춤
r2 = r2_score(y_test, y_pred) # 설명력 (1에 가까울수록 좋음)

print("\n--- [모델 예측 성능 평가] ---")
print(f"✅ 평균제곱근오차 (RMSE): {rmse:.4f} (약 {rmse * 100000:,.0f} 달러의 예측 오차)")
print(f"✅ 결정계수 (R-squared) : {r2:.4f} (모델이 집값 변동의 약 {r2 * 100:.1f}%를 설명함)")

# 실제 집값과 예측 집값 슬쩍 비교해보기 (앞에서 5개만)
print("\n[실제값 vs 예측값 샘플]")
sample_comparison = pd.DataFrame({'실제 집값': y_test.values[:5], '예측 집값': y_pred[:5]})
print(sample_comparison)

# ---------------------------------------------------------
# 5. 특성 중요도 (Feature Importance) 시각화
# ---------------------------------------------------------
importances = rf_model.feature_importances_

feature_imp_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 5))
plt.barh(feature_imp_df['Feature'], feature_imp_df['Importance'], color='coral')
plt.gca().invert_yaxis() 
plt.title('캘리포니아 집값 예측 - 랜덤 포레스트 특성 중요도', fontsize=15)
plt.xlabel('중요도 (Importance)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()