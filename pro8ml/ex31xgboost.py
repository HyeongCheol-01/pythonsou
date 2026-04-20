# pip install xgboost
# pip install lightgbm
# Boosting
# LGBMClassifier # xgboost보다 성능 우수하나 자료가 적으면 과적합 발생
# brest_cancer dataset

import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
from lightgbm import LGBMClassifier

print("=== [ex31xgboost] XGBoost & LightGBM 피처 중요도(%) 비교 ===")

# 1. 데이터 로드 및 확인
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target
feature_names = cancer.feature_names # 피처 이름 미리 저장

# 2. Train / Test 데이터 분할
# test_size=0.2, random_state=12, stratify=y
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12, stratify=y
)

# ---------------------------------------------------------
# 3. XGBoost 모델 생성 및 학습
# ---------------------------------------------------------
xgb_clf = xgb.XGBClassifier(
    booster='gbtree',       
    max_depth=6,            
    n_estimators=100,       
    random_state=12,
    eval_metric='logloss' 
)

print("XGBoost 모델 학습 중...")
xgb_clf.fit(X_train, y_train)
xgb_pred = xgb_clf.predict(X_test)
print(f"✅ XGBoost 예측 정확도: {accuracy_score(y_test, xgb_pred):.4f}")

# ---------------------------------------------------------
# 4. LightGBM 모델 생성 및 학습
# ---------------------------------------------------------
lgbm_clf = LGBMClassifier(
    n_estimators=100,
    random_state=12,
    verbose=-1  
)

print("LightGBM 모델 학습 중...")
lgbm_clf.fit(X_train, y_train)
lgbm_pred = lgbm_clf.predict(X_test)
print(f"✅ LightGBM 예측 정확도: {accuracy_score(y_test, lgbm_pred):.4f}")

# =========================================================
# 5. 피처 중요도(%) 변환 및 fillna(0) 적용 (요청하신 핵심 로직!)
# =========================================================

# 각 모델의 중요도 값을 Series로 만들기 (인덱스는 피처 이름)
xgb_gain = pd.Series(xgb_clf.feature_importances_, index=feature_names)
lgbm_gain = pd.Series(lgbm_clf.feature_importances_, index=feature_names)

# [핵심 1] 각 피처의 기여도를 합이 100이 되도록 비율(%)로 변환
xgb_gain_pct = (xgb_gain / xgb_gain.sum()) * 100
lgbm_gain_pct = (lgbm_gain / lgbm_gain.sum()) * 100

# [핵심 2] DataFrame으로 합치고, 사용되지 않은 피처(NaN)는 fillna(0)으로 채움
comp_df = pd.DataFrame({
    'XGBoost (gain %)': xgb_gain_pct,
    'LightGBM (gain %)': lgbm_gain_pct
}).fillna(0) # 결측치를 0%로 변환

# XGBoost 중요도 기준으로 내림차순 정렬
comp_df = comp_df.sort_values(by='XGBoost (gain %)', ascending=False)

print("\n--- [핵심 피처 중요도 비교 결과 (Top 15)] ---")
# 가독성을 위해 소수점 둘째 자리까지만 출력
print(comp_df.head(15).round(2))