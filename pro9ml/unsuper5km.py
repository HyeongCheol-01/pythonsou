from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 데이터 준비
students = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1,1)
print('점수 :\n', scores)

# 2. KMeans 모델 작성 및 학습 (k=3)
kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)
km_clusters = kmeans.fit_predict(scores)

# 3. 결과를 데이터프레임으로 정리
# 컬럼명을 한글에서 영문으로 통일하면 관리가 더 편합니다.
df = pd.DataFrame({'student': students, 'score': scores.flatten(), 'cluster': km_clusters})

# 군집별 점수 평균 계산
grouped = df.groupby('cluster')['score'].mean()
print("\n[군집별 점수 평균]")
print(grouped)

# 4. 시각화
x_position = np.arange(len(students))
y_scores = scores.ravel()

plt.figure(figsize=(10, 6))

colors = ['red', 'green', 'blue']
# 학생별 군집 색으로 구분해 산점도 출력
for i, (x,y,cluster) in enumerate(zip(x_position,y_scores, km_clusters)):
    plt.scatter(x,y,color=colors[cluster],s=100)
    plt.text(x,y +1.5, students[i])

# 중심점 (Centroids) 시각화
centers = kmeans.cluster_centers_  # 모델이 계산한 군집별 평균 점수

for center in centers:
    # 1. 중심점을 가로 지르는 점선 표시 (해당 군집의 평균 수준)
    plt.scatter(len(students)//2, center[0], marker='X', c='black', s=200)

# 그래프 서식 설정

plt.xlabel('학생 (인덱스)')
plt.ylabel('점수')
plt.xticks(x_position, students) # x축을 s1, s2... 이름으로 표시
plt.grid(True)
plt.show()