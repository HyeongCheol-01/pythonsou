import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.api import add_constant, qqplot
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

# 1. 모델 학습 (기존 방식 동일)
url = "https://raw.githubusercontent.com/pykwon/python/master/testdata_utf8/Carseats.csv"
df = pd.read_csv(url)
formula = 'Sales ~ CompPrice + Income + Advertising + Population + Price + ShelveLoc + Age + Education + Urban + US'
model = smf.ols(formula=formula, data=df).fit()
fitted = model.predict(df)
residual = model.resid

print("--- [검정 결과 보고서] ---\n")

# [1] 선형성 및 등분산성 시각화

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color': 'red'})
plt.title("선형성 검정 (Residuals vs Fitted)")
plt.xlabel("예측값")
plt.ylabel("잔차")

# [2] 정규성 검정 (Q-Q Plot & Shapiro-Wilk)

plt.subplot(1, 2, 2)
qqplot(residual, line='s', ax=plt.gca())
plt.title("정규성 검정 (Normal Q-Q Plot)")
plt.tight_layout()
plt.show()

shapiro_test = stats.shapiro(residual)
print(f"1. 정규성 (Shapiro-Wilk): p-value = {shapiro_test.pvalue:.4f}")
print("   -> 0.05보다 크면 정규성을 만족합니다.")

# [3] 독립성 검정 (Durbin-Watson)

dw_stat = sms.durbin_watson(residual)
print(f"2. 독립성 (Durbin-Watson): {dw_stat:.4f}")
print("   -> 2에 가까울수록 독립적이며, 보통 1.5~2.5 사이면 만족합니다.")

# [4] 등분산성 검정 (Breusch-Pagan)
bp_test = sms.het_breuschpagan(residual, model.model.exog)
print(f"3. 등분산성 (Breusch-Pagan): p-value = {bp_test[1]:.4f}")
print("   -> 0.05보다 크면 등분산성을 만족합니다.")

# [5] 다중공선성 검정 (VIF)
df_ind = pd.get_dummies(df.drop('Sales', axis=1), drop_first=True)
df_ind = add_constant(df_ind.astype(float))
vifdf = pd.DataFrame()
vifdf['variable'] = df_ind.columns
vifdf['vif_value'] = [variance_inflation_factor(df_ind.values, i) for i in range(df_ind.shape[1])]

print("\n4. 다중공선성 (VIF):")
print(vifdf[vifdf['variable'] != 'const'].sort_values(by='vif_value', ascending=False).head(5))
print("   -> 모든 변수가 10 이하면 안전합니다.")