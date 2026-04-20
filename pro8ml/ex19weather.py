import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.metrics import confusion_matrix, accuracy_score

# ---------------------------------------------------------
# 1. 데이터 준비 
# (실제 환경에서는 pd.read_csv('weather.csv') 로 불러오세요)
# ---------------------------------------------------------
# 실행을 확인하실 수 있도록 가상의 날씨 데이터를 생성했습니다.
np.random.seed(42)
df = pd.DataFrame({
    'MinTemp': np.random.uniform(10, 25, 200),
    'MaxTemp': np.random.uniform(20, 35, 200),
    'Humidity': np.random.uniform(30, 90, 200),
    # 종속변수 (0: 비 안 옴, 1: 비 옴)
    'RainTomorrow': np.random.choice([0, 1], 200) 
})

# ---------------------------------------------------------
# 2. 포뮬러(Formula) 생성
# ---------------------------------------------------------
# 모델에 학습시킬 독립변수(X) 리스트
features = ['MinTemp', 'MaxTemp', 'Humidity'] 

# "MinTemp + MaxTemp + Humidity" 형태로 연결
col_select = " + ".join(features) 

# 최종 공식 생성: 종속변수 ~ 독립변수들
my_Formula = 'RainTomorrow ~ ' + col_select 
print(f"📌 적용된 공식: {my_Formula}\n")

# ---------------------------------------------------------
# 3. 모델 생성 및 학습 (Logistic Regression)
# ---------------------------------------------------------
# 분류 문제이므로 OLS가 아닌 Logit을 사용합니다.
model = smf.logit(formula=my_Formula, data=df).fit()

print("\n--- [모델 요약] ---")
print(model.summary())

# ---------------------------------------------------------
# 4. 예측 수행
# ---------------------------------------------------------
# predict()의 결과는 0~1 사이의 '확률값'으로 나옵니다.
pred_probs = model.predict(df)

# 확률이 0.5 이상이면 1(비 옴), 미만이면 0(비 안 옴)으로 분류
pred_class = (pred_probs >= 0.5).astype(int)

# ---------------------------------------------------------
# 5. 분류 정확도 및 모델 평가
# ---------------------------------------------------------
conf_mat = confusion_matrix(df['RainTomorrow'], pred_class)
accuracy = accuracy_score(df['RainTomorrow'], pred_class)

print("\n--- [평가 결과] ---")
print("1. 혼동 행렬 (Confusion Matrix):")
# 결과를 보기 좋게 DataFrame으로 매핑
conf_df = pd.DataFrame(conf_mat, 
                       index=['실제: 비 안옴(0)', '실제: 비 옴(1)'], 
                       columns=['예측: 비 안옴(0)', '예측: 비 옴(1)'])
print(conf_df)

print(f"\n2. 분류 정확도 (Accuracy): {accuracy:.4f} ({accuracy * 100:.2f}%)")