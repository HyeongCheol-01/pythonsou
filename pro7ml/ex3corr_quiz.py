# 상관관계 문제)
# https://github.com/pykwon/python 에 있는 Advertising.csv 파일을 읽어 tv,radio,newspaper 간의 상관관계를 파악하시오. 
# 또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후 TV, radio, newspaper에 대한 영향을 해석하시오.
# 그리고 이들의 관계를 heatmap 그래프로 표현하시오. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

def pro_corrcoef(coef):
    if 0.7<= abs(coef) <= 1:
        return "(강한 상관관계)"
    elif 0.3<= abs(coef) < 0.7:
        return "(약한 상관관계)"
    elif abs(coef) < 0.3:
        return "(상관관계가 거의 없음)"

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head())
print(data.describe())


# 1) tv,radio,newspaper 간의 상관관계를 파악
print('각 제품의 표준편차')
print(np.std(data.tv))
print(np.std(data.radio))
print(np.std(data.newspaper))
print()

print('각 제품의 상관계수')
coef_1 = np.corrcoef(data.tv, data.radio)[0, 1]
coef_2 = np.corrcoef(data.radio, data.newspaper)[0, 1]
coef_3 = np.corrcoef(data.tv, data.newspaper)[0, 1]

print(f"tv와 radio : {coef_1:.6f} / {pro_corrcoef(coef_1)}")
print(f"radio와 newspaper : {coef_2:.6f} / {pro_corrcoef(coef_2)}")
print(f"tv와 newspaper : {coef_3:.6f} / {pro_corrcoef(coef_3)}")
print()

# 2) 또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후 TV, radio, newspaper에 대한 영향을 해석하시오.

print('sales와 제품의 상관계수')
sale_coef_1 = np.corrcoef(data.sales, data.tv)[0, 1]
sale_coef_2 = np.corrcoef(data.sales, data.radio)[0, 1]
sale_coef_3 = np.corrcoef(data.sales, data.newspaper)[0, 1]

print(f"sale와 tv : {sale_coef_1:.6f} / {pro_corrcoef(sale_coef_1)}")
print(f"sale와 radio : {sale_coef_2:.6f} / {pro_corrcoef(sale_coef_2)}")
print(f"sale와 newspaper : {sale_coef_3:.6f} / {pro_corrcoef(sale_coef_3)}")
print()

# 3) 그리고 이들의 관계를 heatmap 그래프로 표현하시오. 

import seaborn as sns
sns.heatmap(data.corr(), annot=True)
# heatmap에 텍스트 표시 추가사항 적용해 보기
corr = data.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)  # 상관계수값 표시
mask[np.triu_indices_from(mask)] = True
# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
fig, ax = plt.subplots()     # Set up the matplotlib figure

sns.heatmap(corr, mask=mask, vmin=-vmax, vmax=vmax, square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    ax.text(i + 0.5, len(corr) - (i + 0.5), corr.columns[i], ha="center", va="center", rotation=45)
    for j in range(i + 1, len(corr)):
        s = "{:.3f}".format(corr.values[i, j])
        ax.text(j + 0.5, len(corr) - (i + 0.5), s, ha="center", va="center")
ax.axis("off")
plt.show()



