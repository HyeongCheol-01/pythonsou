import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

print("=== [ex22tree] 결정 트리(Decision Tree) 기본 ===")

# 1. 데이터 로드 및 분할
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. 결정 트리 모델 생성 및 학습
# criterion='gini' (기본값) 또는 'entropy' 사용 가능
model = DecisionTreeClassifier(random_state=42)
model.fit(x_train, y_train)

# 3. 모델 평가
y_pred = model.predict(x_test)
print(f"✅ 테스트 데이터 정확도: {accuracy_score(y_test, y_pred):.4f}")
print(f"✅ Train 정확도: {model.score(x_train, y_train):.4f} (1.0이 나오면 과적합 의심!)")

# 4. 트리 구조 시각화 (어떤 기준으로 분류했는지 확인)
plt.figure(figsize=(15, 10))
# max_depth=2 까지만 그려서 복잡함을 줄임
plot_tree(model, max_depth=2, filled=True, feature_names=cancer.feature_names, class_names=['악성', '양성'], rounded=True)
plt.title("유방암 진단 결정 트리 (max_depth=2 부분 표시)", fontsize=15)
plt.show()