import numpy as np
from scipy import stats

midterm = np.array([80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80])
final = np.array([90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95])

# 귀무 : 중간고사와 기말고사 성적의 차이가 없다.
# 대립 : 중간고사와 기말고사 성적의 차이가 있다.


# 정규성 검정
diff = final - midterm
shapiro_test = stats.shapiro(diff)

print(f"차이값의 정규성 검정 p-value: {shapiro_test.pvalue:.4f}")
# p 0.3011 > 0.05 정규성 만족

t_stat, p_val = stats.ttest_rel(midterm, final)

print(f"t-통계량: {t_stat:.4f}")
print(f"p-value: {p_val:.4f}")


# 결론: p-value가 0.05보다 작으므로 귀무가설을 기각
# 즉, 이 학급의 중간고사와 기말고사 성적 사이에는 유의미한 차이가 있으며 
# 학업능력이 변화했다고 볼 수 있음
