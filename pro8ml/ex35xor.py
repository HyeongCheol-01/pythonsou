# SVM으로 AND, OR, XOR 연산 처리하기

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import svm, metrics

# 1. 3가지 논리 연산 데이터 준비 (x1, x2, y정답)
# 사용자님이 작성하신 형태를 그대로 활용합니다!
or_data = [
    [0, 0, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

and_data = [
    [0, 0, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 1]
]

xor_data = [
    [0, 0, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]

# 2. 모델 학습 및 평가를 수행하는 함수
def test_logic_gate(name, data):
    # 데이터를 Pandas DataFrame으로 변환
    df = pd.DataFrame(data, columns=['x1', 'x2', 'y'])
    
    # 문제(X)와 정답(y) 분리
    X = df[['x1', 'x2']]
    y = df['y']
    
    # 3. 두 가지 모델 생성
    lr_model = LogisticRegression()     # 선형 모델 (직선 1개만 그을 수 있음)
    svm_model = svm.SVC(kernel='rbf')   # 비선형 모델 (곡선을 그릴 수 있음)
    
    # 4. 학습 (Fit)
    lr_model.fit(X, y)
    svm_model.fit(X, y)
    
    # 5. 예측 (Predict)
    lr_pred = lr_model.predict(X)
    svm_pred = svm_model.predict(X)
    
    # 6. 결과 출력 (metrics.accuracy_score 사용)
    lr_acc = metrics.accuracy_score(y, lr_pred)
    svm_acc = metrics.accuracy_score(y, svm_pred)
    
    print(f"\n--- [{name} 연산] ---")
    print(f"실제 정답 : {y.tolist()}")
    print(f"LR 예측값 : {lr_pred.tolist()} (정확도: {lr_acc * 100:.0f}%)")
    print(f"SVM 예측값: {svm_pred.tolist()} (정확도: {svm_acc * 100:.0f}%)")

# 함수를 호출하여 3가지 연산을 모두 테스트합니다.
test_logic_gate("OR", or_data)
test_logic_gate("AND", and_data)
test_logic_gate("XOR", xor_data)