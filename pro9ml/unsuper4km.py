# 실습 1 - make_blobs 사용
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

x, _ = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
print(x[:3], ' ', x.shape) #(150,2)

#산점도
plt.scatter(x[:,0], x[:,1], c='gray', marker='o', s=50)
plt.grid(True)
plt.show()

#KMeans 모델 작성
# cluster의 중심을 선택하는 방법
#init_centroid = 'random' # cluster의 중심을 임의로 선택
init_centroid = 'k-means++' # cluster의 중심을 k-means++로 선택
#kmodel = KMeans(n_clusters=3, init=init_centroid, n_init=10, random_state=0)
#n_init 10 : KMeans를 10회 실행 - 가장 좋은 결과(오차 최소값)를 선택
kmodel = KMeans(n_clusters=3, init=init_centroid, random_state=0)
pred = kmodel.fit_predict(x)   # 클러스터링으로 구분한 결과 얻기
print('pred:', pred)

# 각 그룹별 보기
# print(x[pred==0])
# print(x[pred==1])
# print(x[pred==2])
print('중심점 :', kmodel.cluster_centers_)

# 시각화
plt.scatter(x[pred==0, 0], x[pred==0, 1], c='red', marker='o', s=50, label='Cluster 0')
plt.scatter(x[pred==1, 0], x[pred==1, 1], c='green', marker='s', s=50, label='Cluster 1')
plt.scatter(x[pred==2, 0], x[pred==2, 1], c='blue', marker='v', s=50, label='Cluster 2')
plt.scatter(kmodel.cluster_centers_[:, 0], kmodel.cluster_centers_[:, 1], c='black', marker='+', s=60, label='Center')
plt.title('K-Means Clustering Result')
plt.legend()
plt.grid(True)
plt.show()

# KMeans의 k값은? elbow or silhoutte 기법을 이용해 k값 얻기
def elbow(x):
    sse = []
    for i in range(1,11):
        km = KMeans(n_clusters=i, init=init_centroid, random_state=0)
        km.fit(x)
        sse.append(km.inertia_)
    plt.plot(range(1,11), sse, marker='o')
    plt.xlabel('군집수')
    plt.ylabel("SSE")
    plt.show()
    
elbow(x)