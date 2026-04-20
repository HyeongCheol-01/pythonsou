import os
os.environ['OMP_NUM_THREADS'] = '1'
# KMeans : iris dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
# adjusted_rand_score : 군집 vs 실제 라벨 비교
# normalized_mutual_info_score : 정보량 기반 유사도(같은 정보 공유
# silhouette_score : 군집 자체 품질 평가(군집에 잘 속해 있는가 확인)
from sklearn.decomposition import PCA # 4차원 -> 2차원으로 압축

iris = load_iris()
x = iris.data
y = iris.target
feature_names = iris.feature_names

df = pd.DataFrame(x, columns=feature_names)
print('iris data shape :', x.shape) #(150, 4)

# 스케일링
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
print(x_scaled[:2]) 
# [[-0.90068117  1.01900435 -1.34022653 -1.3154443 ]

# KMeans 모델
k = 3
kmeans = KMeans(
    n_clusters=k, init='k-means++', n_init=10, random_state=42
    # n_init = 10  KMeans를 10회 실행 - 가장 좋은 결과(오차 최소값)를 선택
)

clusters = kmeans.fit_predict(x_scaled)
df['cluster'] = clusters
print('클러스터 중심 값:', kmeans.cluster_centers_)

# 시각화(PCA기반. 왜? 4개의 영을 2차원차트에 표현 불가. 그래서 두개로 표현
# PCA (여기서는 시각화용으로 준비함)
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
print('pca 설명 분산 비율 : ', pca.explained_variance_ratio_) # [0.72962445 0.22850762] 
print(x_pca[:2]) # [[-2.26470281  0.4800266 ]

plt.figure(figsize=(6,5))
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:,1], hue=clusters, palette='viridis', s=60)
plt.title('KMeans Clustering')
plt.xlabel('PC1(제1주성분)')
plt.ylabel('PC2(제2주성분)')
plt.show()

# 실제 라벨과 군집 비교(교차표)
ct=pd.crosstab(y,clusters)
print(ct)
# col_0   0   1   2   군집번호
# row_0
# 0       0  50   0     setosa
# 1      39   0  11     versicolor 섞임
# 2      14   0  36     virginica 섞임
# 행 : 실제라벨(iris)

print('클래스별 대표 군집')
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f'실제 클래스 {i} -> 군집 {max_cluster}')
# 실제 클래스 0 -> 군집 1
# 실제 클래스 1 -> 군집 0
# 실제 클래스 2 -> 군집 2

print('정량 평가 ---')
ari = adjusted_rand_score(y, clusters)
nmi = normalized_mutual_info_score(y, clusters)
sil_score = silhouette_score(x_scaled, clusters)
print(f'ARI : {ari:.4f}') # 0.6201
print(f'NMI : {nmi:.4f}') # 0.6595
print(f'Silhouette_Scores : {sil_score:.4f}') # 0.4599
#군집 자체 품질 평가 : 0.4599 <- 1에 근사할수록 좋음. 0또는 음수면 잘못된 군집
# 좋은 굱비이란 군집 내 요소끼리는 가깝고, 다른 군집 간에는 거리가 멀다.

# k=3을 사용했는데 과연 3 이 합리적인지 확인 : 엘보우
initia_list = [] # 각 데이터가 속한 클러스터 중심까지의 거리 제곱합
k_range = range(1, 10)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(x_scaled)
    initia_list.append(km.inertia_)
    
plt.figure(figsize=(6,4))
plt.plot(k_range, initia_list, marker='o')
plt.title('엘보우 기법')
plt.xlabel('클러스터 수(k)')
plt.ylabel('initia')
plt.show()  # k가 3인 경우가 가장 적당


#실제 vs 군집 비교 시각화
plt.figure(figsize=(12,5))
#실제 라벨
plt.subplot(1,2,1)
sns.scatterplot(x=x_pca[:,0], y=x_pca[:,1], hue=y, palette='Set1')
plt.title('실제 라벨')

#군집 결과
plt.subplot(1,2,2)
sns.scatterplot(x=x_pca[:,0], y=x_pca[:,1], hue=clusters, palette='Set1')
plt.title('군집 결과')
plt.show()

# 클러스터별 평균 분석
pd.set_option('display.max_columns', None)
clusters_mean = df.groupby('cluster').mean()
print('클러스터별 평균:', clusters_mean)

# 군집 3개 : 군집 간 평균차이 검정(ANOVA)
# 귀무 : 군집 간 평균에 차이가 없다.
# 연구 : 군집 간 평균에 차이가 있다.
from scipy.stats import f_oneway

for col in feature_names:   # 각 군집별 데이터 분리
    group0 = df[df['cluster']==0][col]
    group1 = df[df['cluster']==1][col]
    group2 = df[df['cluster']==2][col]
    # ANOVA 수행
    f_stat, p_val = f_oneway(group0,group1,group2)
    print(f'{col} : f-statistic:{f_stat:.4f}, p_value:{p_val:.4f}')
    
    #해석
    if p_val >= 0.05:
        print('군집 간 평균에 차이가 없다.')
    else:
        print("군집 간 평균에 차이가 있다.")
        
# KMeans 가 꽃받침, 꽃잎 길이/너비를 제대로 군집분석 했음을 알 수 있다.

# 사후 검정
from statsmodels.stats.multicomp import pairwise_tukeyhsd
print('\n' + '='*60)
print('세부 군집 간 차이 분석 (Tukey HSD Post-hoc Test)')
print('='*60)
feature = feature_names[2]
tukey = pairwise_tukeyhsd(endog=df[feature], groups=df['cluster'], alpha=0.05)
    
# 2. 결과 출력
print(f'\n[ {feature} ] 컬럼의 군집 간 비교:')
print(tukey) 

tukey.plot_simultaneous(figsize=(6,4))
plt.title(f'tukeyhsd - {feature}')
plt.xlabel('평균 차이')
plt.show()

print()
# 군집별 Boxplot
for col in feature_names:
    plt.figure(figsize=(5,3))
    sns.boxplot(x='cluster', y=col, data=df)
    plt.title(f'{col} by cluster')
    plt.show()
    
print() # 클러스터 평균분석 마지막 열에 Type 추가
clusters_mean['label'] = ['Type A', 'Type B', 'Type C']
print(clusters_mean)
