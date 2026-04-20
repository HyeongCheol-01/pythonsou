import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster # fcluster 추가

iris = load_iris()
x = iris.data
y = iris.target
labels = iris.target_names

pd.set_option('display.max_columns', None) # opnion -> option 수정
df = pd.DataFrame(x, columns=iris.feature_names)
print(df.head(3))

# 스케일링 - 권장
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# 계층적 군집
z = linkage(x_scaled, method='ward')

# 덴드로그램
plt.figure(figsize=(12,5))
dendrogram(z)
plt.title('아이리스로 계층적 군집')
plt.xlabel('샘플')
plt.ylabel('거리(유클리드)')
plt.show()

# 덴드로그램을 잘라서 최대 3개의 군집 만들기
clusters = fcluster(Z=z, t=3, criterion='maxclust')

# 데이터프레임에 군집 결과 추가
df['cluster'] = clusters # 문법 오류 수정
print(df.head(3))
print(df.tail(3))

# 2개 feature 시각화(산점도)
plt.figure(figsize=(6,5))
sns.scatterplot(x=x_scaled[:, 0], y=x_scaled[:, 1], hue=clusters, palette='Set1') # y축 슬라이싱 수정
# hue=clusters : 군집결과에 따라 색을 달리 표시, palette='Set1' : 색상
plt.title('군집결과')
plt.xlabel('feature1')
plt.ylabel('feature2')
plt.show()

print('실제 라벨 : ', y[:10])
print('군집 결과 : ', clusters[:10])

print('\n군집 결과 검증---')
print('교차표 - 실제 라벨 vs 군집 결과')
ct = pd.crosstab(y, clusters)
print(ct)

# col_0   1   2   3
# row_0
# 0      49   1   0
# 1       0  27  23   # versicolor : 많이 섞임
# 2       0   2  48   # 잘 분류

# row_0(실제 라벨):0-setosa, 1-versicolor, 2-virginica
# col_0(군집 결과): 1-cluster 1, 2-cluster 2, 3-cluster 3
# setosa는 완벽히 분리되었고, virginica는 일부 섞인 결과 보임

print('교차표 보조 설명 : 각 실제 클래스가 갖아 많이 속한 군집')
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idmax()
    print(f'실제 클래스 {i} -> 군집 {max_cluster} (갯수:{ct.iloc[i].max()})')
    
# 정량적 평가 : 군집 결과가 실제 정답과 얼마나 유사한 지를 수치로 표현
from sklearn.metrics import adjusted_mutual_info_score, normalized_mutual_info_score
#adjusted_mutual_info_score :ARI 같은 그룹끼리 잘 묶였는지 평가
ari = adjusted_mutual_info_score(y, clusters)
print('평가지표 ari', ari)  #0.7이상 매우 잘됨

nmi = normalized_mutual_info_score(y, clusters)
print('평가지표 nmi', nmi)  # 0~1사이 완벽
