import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
# [수정됨] StratifiedKFold를 추가로 가져옵니다!
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("=== [ex29rf_adult] 파이프라인 + GridSearchCV + StratifiedKFold 완결판 ===")

# ---------------------------------------------------------
# 1. 데이터 로드 및 분할 
# ---------------------------------------------------------
print("OpenML에서 Adult 데이터를 다운로드 중입니다...")
adult = fetch_openml(name='adult', version=2, as_frame=True, parser='auto')

X = adult.data
y = adult.target

# 정답지(y) 변환: '>50K'는 1, '<=50K'는 0
y = (y == '>50K').astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------------------------------------------------
# 2. 전처리 파이프라인 구축
# ---------------------------------------------------------
numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X_train.select_dtypes(include=['object', 'category']).columns

# 숫자형 전처리
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# 범주형 전처리
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# ---------------------------------------------------------
# 3. ColumnTransformer로 두 파이프라인 합치기
# ---------------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# ---------------------------------------------------------
# 4. 최종 모델 파이프라인 생성
# ---------------------------------------------------------
clf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier(random_state=42, n_jobs=-1))
])

# =========================================================
# 5. 하이퍼파라미터 튜닝 (GridSearchCV + StratifiedKFold)
# =========================================================
param_grid = {
    'model__n_estimators': [100, 200],         # 숲의 나무 개수
    'model__max_depth': [None, 5, 10],         # 트리의 최대 깊이
    'model__class_weight': [None, 'balanced']  # 클래스 불균형 보정
}

# ⭐ [수정됨] StratifiedKFold 설정
# n_splits=3: 3등분으로 쪼갭니다.
# shuffle=True: 쪼개기 전에 데이터를 골고루 섞어주어 편향을 방지합니다.
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

# GridSearchCV 설정
grid = GridSearchCV(
    estimator=clf_pipeline,     
    param_grid=param_grid,      
    cv=cv,                     # ⭐ 직접 만든 StratifiedKFold 객체를 cv에 넣어줍니다!
    scoring='roc_auc', 
    n_jobs=-1            # 모든 cpu 사용       
)

print("\nGridSearchCV 하이퍼파라미터 튜닝 및 학습 시작... (잠시만 기다려주세요!)")
grid.fit(X_train, y_train)

# ---------------------------------------------------------
# 6. 최적화 결과 확인 및 최종 평가
# ---------------------------------------------------------
print("\n--- [GridSearchCV 탐색 결과] ---")
print(f"✅ 찾아낸 최적의 파라미터:\n {grid.best_params_}")
print(f"✅ 최고 교차 검증 정확도: {grid.best_score_:.4f}")

# 1등을 한 최적의 파이프라인(전처리기 + 튜닝된 모델)을 꺼내서 최종 실전 예측
best_pipeline = grid.best_estimator_
y_pred = best_pipeline.predict(X_test)

print("\n--- [최종 실전 Test 예측 결과] ---")
print(f"👑 최적화된 파이프라인 실전 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[상세 분류 보고서]")
print(classification_report(y_test, y_pred, target_names=['<=50K', '>50K']))