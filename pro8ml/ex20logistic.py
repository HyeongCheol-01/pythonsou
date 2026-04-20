import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import koreanize_matplotlib
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# =========================================================
# 1. 시각화 함수 정의 (수정 완료된 버전)
# =========================================================
def plot_decision_regionFunc(X, y, classifier, test_idx=None, resolution=0.02, title=''):
    markers = ('s', 'x', 'o', '^', 'v')      
    colors = ('r', 'b', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    Z = classifier.predict(np.array([xx.ravel(), yy.ravel()]).T)
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)   
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], color=cmap.colors[idx], marker=markers[idx], label=cl)

    if test_idx:
        X_test = X[test_idx, :]
        plt.scatter(X_test[:, 0], X_test[:, 1], facecolors='none', edgecolors='black', linewidth=1, marker='o', s=80, label='testset (테스트 데이터)')

    plt.xlabel('꽃잎 길이 (Petal Length - 표준화됨)')
    plt.ylabel('꽃잎 너비 (Petal Width - 표준화됨)')
    plt.legend(loc='upper left')
    plt.title(title)
    plt.show()

# =========================================================
# 2. 데이터 준비 및 전처리
# =========================================================
print("--- [1] 데이터 로드 및 전처리 ---")
iris = load_iris()
# 시각화를 위해 특성 2개(인덱스 2: 꽃잎 길이, 인덱스 3: 꽃잎 너비)만 추출
X = iris.data[:, [2, 3]] 
y = iris.target

# Train / Test 분할 (7:3) - 총 150개 중 Train 105개, Test 45개
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 데이터 표준화(Scaling): 모델 성능 향상 및 시각화 코드의 '_std' 변수명에 맞춤
sc = StandardScaler()
sc.fit(x_train)
x_train_std = sc.transform(x_train)
x_test_std = sc.transform(x_test)

# =========================================================
# 3. 모델 학습 및 평가
# =========================================================
print("--- [2] 로지스틱 회귀 모델 학습 ---")
# 이전 코드에서 작성하신 하이퍼파라미터 적용 (Iris는 클래스가 3개이므로 multinomial이 찰떡입니다!)
model = LogisticRegression(C=0.1, solver="lbfgs", multi_class='multinomial', random_state=0)
model.fit(x_train_std, y_train)

y_pred = model.predict(x_test_std)
acc = accuracy_score(y_test, y_pred)
print(f"✅ 모델 정확도: {acc:.4f}\n")

# =========================================================
# 4. 모델 저장 및 불러오기 (joblib)
# =========================================================
print("--- [3] 모델 저장 및 불러오기 ---")
joblib.dump(model, 'iris_model.pkl')
print("✅ 'iris_model.pkl' 저장 완료")

# 저장된 모델 불러와서 read_model 변수에 담기
read_model = joblib.load('iris_model.pkl')
print("✅ 'iris_model.pkl' 불러오기 완료\n")

# =========================================================
# 5. 결정 경계 시각화
# =========================================================
print("--- [4] 결정 경계 시각화 실행 ---")
# 시각화 함수에 넣기 위해 분할했던 Train과 Test 데이터를 다시 하나로 합침
x_combined_std = np.vstack((x_train_std, x_test_std))
y_combined = np.hstack((y_train, y_test))

# test_idx 설정: Train 데이터가 105개이므로, 105번 인덱스부터 끝(150)까지가 테스트 데이터임
plot_decision_regionFunc(
    X=x_combined_std, 
    y=y_combined, 
    classifier=read_model, 
    test_idx=range(105, 150), 
    title='Iris 로지스틱 회귀 분류 결과 (scikit-learn)'
)