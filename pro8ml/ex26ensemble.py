import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

print("=== [ex26ensemble] 앙상블(Voting)과 Stratified K-Fold 교차검증 ===")

# 1. 데이터 로드 및 분할
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# stratify=y 옵션: Train과 Test 세트에도 원본 데이터의 양성/악성 비율을 동일하게 유지해 줍니다.
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# 2. 개별 모델(Weak Learner) 생성
# 특성이 다른 3가지 모델을 준비합니다.
lr_model = LogisticRegression(max_iter=10000, random_state=42)
dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
knn_model = KNeighborsClassifier(n_neighbors=5)

# 3. 앙상블 모델 (Voting Classifier) 생성
# estimators: 투표에 참여할 모델들의 이름과 객체를 리스트로 묶어줍니다.
# voting='soft': 각 모델이 예측한 '확률'을 평균 내어 최종 결과를 결정합니다. (보통 hard보다 성능이 좋습니다)
voting_model = VotingClassifier(
    estimators=[('LR', lr_model), ('DT', dt_model), ('KNN', knn_model)],
    voting='soft'
)

# 4. Stratified K-Fold 설정 (모의고사 출제 방식)
# 일반 KFold와 달리, 쪼개진 각 폴드(모의고사 문제지)마다 정답(양성/악성)의 비율을 똑같이 맞춰줍니다.
skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 5. 개별 모델과 앙상블 모델 성능 비교 (교차 검증)
models = [lr_model, dt_model, knn_model, voting_model]
model_names = ['로지스틱 회귀', '결정 트리', 'KNN(최근접 이웃)', '👑 앙상블 (Soft Voting)']

print("\n--- [Stratified 5-Fold 교차검증 평균 정확도] ---")
# cross_val_score를 사용하면 for문으로 직접 폴드를 쪼갤 필요 없이 한 줄로 점수를 계산해 줍니다!
for model, name in zip(models, model_names):
    scores = cross_val_score(model, x_train, y_train, cv=skfold, scoring='accuracy')
    print(f"{name:15s} : {scores.mean():.4f}")

# 6. 최상의 모델(앙상블)로 Test 데이터 최종 평가
print("\n--- [최종 실전 Test 데이터 예측 성능] ---")
# 앙상블 모델을 Train 데이터 전체로 한 번 더 학습시킵니다.
voting_model.fit(x_train, y_train)
pred = voting_model.predict(x_test)

print(f"✅ 앙상블 모델 최종 정확도: {accuracy_score(y_test, pred):.4f}")