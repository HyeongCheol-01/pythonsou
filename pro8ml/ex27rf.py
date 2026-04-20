#RandomForest 분류알고리즘
# Random Forest는 앙상블(Ensemble) 기법 중 하나로, 
# 여러 개의 결정 트리(Decision Tree)를 조합하여 더 강력하고 안정적인 예측 모델을 만드는 방법
# 앙상블(Ensemble)은 머신 러닝에서 여러 개의 개별 모델을 조합하여 
# 더 강력하고 안정적인 모델을 구축하는 기법을 말합니다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # 시각화를 위한 matplotlib
import koreanize_matplotlib # 한글 깨짐 방지
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns # [추가됨] 고급 시각화를 위한 Seaborn

print("=== [ex27rf] 타이타닉 데이터 랜덤 포레스트 분석 ===")

# ---------------------------------------------------------
# 1. 데이터 로드 및 전처리
# ---------------------------------------------------------
df=pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv")

# 분석에 사용할 열에 결측치가 있는 행 제거
df=df.dropna(subset=['Pclass','Age','Sex'])

# 향후 경고 방지를 위해 .copy()를 붙이는 것이 안전합니다.
df_x = df[['Pclass', 'Age','Sex']].copy()

# 정답지(Target) 변수 추출
df_y = df['Survived']

# Sex열 : Label Encoding(문자범주형 -> 정수형)
encoder = LabelEncoder()
df_x.loc[:,'Sex'] = encoder.fit_transform(df_x['Sex'])  # feature

# ---------------------------------------------------------
# 2. Train / Test 데이터 분할
# ---------------------------------------------------------
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=42)

# ---------------------------------------------------------
# 3. 모델 생성 및 학습 (3개 변수 버전)
# ---------------------------------------------------------
model = RandomForestClassifier(criterion='gini', random_state=12, n_estimators=500)
model.fit(train_x, train_y)

# ---------------------------------------------------------
# 4. 예측 및 평가
# ---------------------------------------------------------
pred = model.predict(test_x)
acc = accuracy_score(test_y, pred)
print(f"✅ 기본 3개 변수 모델 정확도: {acc:.4f}\n")

# ---------------------------------------------------------
# 5. 특성 중요도 시각화 (Matplotlib 버전)
# ---------------------------------------------------------
importances = model.feature_importances_
feature_importances_df = pd.DataFrame({
    'Feature': df_x.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(8, 4))
plt.barh(feature_importances_df['Feature'], feature_importances_df['Importance'], color='skyblue')
plt.gca().invert_yaxis() 
plt.title('타이타닉 생존 예측 특성 중요도 (3개 변수)', fontsize=15)
plt.xlabel('중요도 (Importance)', fontsize=12)
plt.ylabel('특성 이름 (Feature)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# =========================================================
# 6. 전체 변수 대상으로 확장하여 중요도 확인
# =========================================================
print("\n=== [변수 확장 모델 적용] ===")

# 새로운 데이터프레임 구성 (6개 변수)
df_imsi = df[['Pclass', 'Age','Sex','Fare','SibSp','Parch']].copy()

# Sex열 다시 인코딩
df_imsi.loc[:,'Sex'] = encoder.fit_transform(df_imsi['Sex'])

# 변수가 늘어났으므로 데이터를 다시 쪼개고, 모델을 새로 학습
train_x2, test_x2, train_y2, test_y2 = train_test_split(df_imsi, df_y, test_size=0.3, random_state=42)

# 새로운 모델 객체 생성 및 학습
model_full = RandomForestClassifier(criterion='gini', random_state=12, n_estimators=500)
model_full.fit(train_x2, train_y2)

# 새로운 모델 성능 확인
pred2 = model_full.predict(test_x2)
print(f"✅ 확장된 6개 변수 모델 정확도: {accuracy_score(test_y2, pred2):.4f}\n")

# 새로운 모델에서 특성 중요도 추출
importances2 = model_full.feature_importances_

# 컬럼명 + 중요도 (sort_values 사용)
feature_df = pd.DataFrame({
    'feature': df_imsi.columns,
    'importance': importances2
}).sort_values(by='importance', ascending=False)

print("--- [전체 변수별 중요도 순위] ---")
print(feature_df)

# =========================================================
# [추가됨] 7. 확장된 모델의 특성 중요도 시각화 (Seaborn 버전)
# =========================================================
plt.figure(figsize=(8, 5))

# Seaborn의 barplot 사용
# x축엔 중요도 수치, y축엔 특성 이름을 넣으면 자동으로 수평 막대 그래프를 그려줍니다.
# palette='viridis' 등 다양한 색상 테마를 적용할 수 있습니다.
sns.barplot(x='importance', y='feature', data=feature_df, palette='viridis')

plt.title('타이타닉 생존 예측 특성 중요도 (6개 변수 - Seaborn)', fontsize=15)
plt.xlabel('중요도 (Importance)', fontsize=12)
plt.ylabel('특성 이름 (Feature)', fontsize=12)

# 레이아웃 겹침 방지 및 여백 자동 조절
plt.tight_layout() 
plt.show()