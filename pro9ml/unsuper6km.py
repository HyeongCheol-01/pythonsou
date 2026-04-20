from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import koreanize_matplotlib

# --- 1. 데이터 생성 (1~20라인) ---
np.random.seed(0)
n_customers = 200 
annual_spending = np.random.normal(50000, 15000, n_customers)
monthly_visits = np.random.normal(5, 2, n_customers)

annual_spending = np.clip(annual_spending, 0, None)
monthly_visits = np.clip(monthly_visits, 0, None)

df = pd.DataFrame({'annual_spending': annual_spending, 'monthly_visits': monthly_visits})

# --- 2. [첫 번째 시각화] 원본 데이터 분포 확인 (~30라인) ---
plt.figure(figsize=(8, 5))
plt.scatter(df['annual_spending'], df['monthly_visits'], c='gray', alpha=0.5)
plt.title("시각화 1: 군집화 전 원본 데이터")
plt.xlabel("연간 지출액")
plt.ylabel("월 방문 횟수")
plt.grid(True, linestyle=':', alpha=0.7)
plt.show() # 첫 번째 그래프 출력

# --- 3. 데이터 전처리 및 모델 학습 (35~45라인) ---
scaler = StandardScaler()
df_scaled = df

kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)
df['cluster'] = kmeans.fit_predict(df_scaled)

# --- 4. [두 번째 시각화] 군집 결과 및 중심점 확인 (~60라인) ---
plt.figure(figsize=(8, 5))
colors = ['red', 'green', 'blue']
for i in range(3):
    cluster_data = df[df['cluster'] == i]
    plt.scatter(cluster_data['annual_spending'], cluster_data['monthly_visits'], 
                c=colors[i], label=f'군집 {i}', edgecolors='w')

# 중심점 복원 및 시각화
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='yellow', marker='*', s=200, 
            edgecolors='black', label='중심점(평균)')

plt.title("시각화 2: K-Means 군집화 완료")
plt.xlabel("연간 지출액")
plt.ylabel("월 방문 횟수")
plt.legend()
plt.show() # 두 번째 그래프 출력

# 5. 결과 요약 출력
print("\n[군집별 성격 요약]")
print(df.groupby('cluster').mean())