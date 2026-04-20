import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

print("=== [ex24treeiris] Iris 데이터와 트리 가지치기 ===")

# 1. 데이터 준비
iris = load_iris()
X = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. 모델 생성 (max_depth=3 으로 깊이 제한!)
# 깊이를 제한하면 모델이 단순해져서 새로운 데이터(Test)를 더 잘 맞출 확률이 높아집니다.
tree_model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
tree_model.fit(x_train, y_train)

# 3. 모델 평가
print(f"✅ Train 데이터 정확도: {tree_model.score(x_train, y_train):.4f}")
print(f"✅ Test 데이터 정확도: {tree_model.score(x_test, y_test):.4f}")

# 4. 트리 시각화
plt.figure(figsize=(10, 7))
plot_tree(tree_model, filled=True, feature_names=iris.feature_names, class_names=iris.target_names, rounded=True)
plt.title("Iris 분류 결정 트리 (max_depth=3)", fontsize=15)
plt.show()