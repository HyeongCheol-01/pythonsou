import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier

print("=== [ex25_with_gridsearch] GridSearchCV를 활용한 과적합 분석 ===")

# 1. 데이터 로드 및 분할
cancer = load_breast_cancer()
x_train, x_test, y_train, y_test = train_test_split(cancer.data, cancer.target, test_size=0.3, random_state=42)

# 2. 결정 트리 모델 생성 (기본)
dtree = DecisionTreeClassifier(random_state=42)

# 3. GridSearchCV 설정 (max_depth 1~10 탐색)
parameters = {'max_depth': range(1, 11)}

# ★ 핵심 포인트: return_train_score=True 를 켜야 Train 점수가 기록되어 그래프를 그릴 수 있습니다!
grid_dtree = GridSearchCV(
    dtree, 
    param_grid=parameters, 
    cv=5, 
    return_train_score=True  # 이 옵션이 없으면 Test(Validation) 점수만 저장됩니다.
)

# 4. 학습 (for문 없이 이 한 줄로 1~10 깊이까지 교차 검증 및 최적화 완료)
print("GridSearchCV 교차 검증 학습 중...")
grid_dtree.fit(x_train, y_train)

# 5. GridSearchCV 결과 기록장(cv_results_) 열어보기
# 결과를 다루기 쉽도록 pandas DataFrame으로 변환합니다.
results = pd.DataFrame(grid_dtree.cv_results_)

# 그래프를 그리기 위해 필요한 데이터만 쏙쏙 뽑아냅니다.
depth_settings = results['param_max_depth']
train_scores = results['mean_train_score'] # Train 데이터에 대한 5번의 교차검증 평균 점수
test_scores = results['mean_test_score']   # Test(Validation) 데이터에 대한 5번의 교차검증 평균 점수

# 6. 최적의 파라미터 확인
best_depth = grid_dtree.best_params_['max_depth']
print(f"\n✅ GridSearchCV가 찾은 최적의 트리의 깊이: {best_depth}")
print(f"✅ 최고 교차 검증 정확도: {grid_dtree.best_score_:.4f}")

# 7. 과적합(Overfitting) 시각화
plt.figure(figsize=(10, 6))

# Train과 Test 점수 그리기
plt.plot(depth_settings, train_scores, label='Train 평균 점수 (암기력)', marker='o', color='blue')
plt.plot(depth_settings, test_scores, label='Test 평균 점수 (응용력)', marker='s', color='orange')

plt.title('GridSearchCV를 이용한 트리의 깊이별 과적합 분석', fontsize=15)
plt.xlabel('트리의 최대 깊이 (max_depth)', fontsize=12)
plt.ylabel('평균 분류 정확도 (Accuracy)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# GridSearchCV가 찾은 '가장 좋은 지점'에 빨간 점선 긋기
plt.axvline(x=best_depth, color='red', linestyle=':', linewidth=2, label=f'GridSearch 1등 (depth={best_depth})')

plt.legend()
plt.show()