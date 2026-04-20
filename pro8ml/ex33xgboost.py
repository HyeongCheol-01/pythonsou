# kaggle의 Snatander customer satisfaction dataset
# 산탄데르 은행의 고객만족 여부 분류 처리
# 클래스 명은 target이고 0:만족 1:불만족

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from xgboost import plot_importance
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns',None)

df= pd.read_csv("train.csv")

# 전체 데이터에서 만족과 불만족의 비용
print(df['TARGET'].value_counts())  # 0:73012, 1:3008
unsatisfied_cnt = df[df['TARGET'] == 1].TARGET.count()
total_cnt = df.TARGET.count()
print(f'불만족 비율은 {unsatisfied_cnt/total_cnt}')

df['var3'].replace(-999999,2,inplace=True)
df.drop('ID', axis=1, inplace=True) # ID는 식별자이므로


# feature/ label 분리
x_features = df.iloc[:,:-1]
y_label = df.iloc[:,-1]

# train /test split
x_train, x_test, y_train, y_test =train_test_split(x_features,y_label, test_size=0.1, stratify=y_label, random_state=12)
train_cnt = y_train.count()
test_cnt = y_test.count()
print('학습데이터 레이블 값 분포 비율')

xgb_clf = XGBClassifier(n_estimators=5, random_state=12, eval_metric='auc')

xgb_clf.fit(x_train, y_train, eval_set=[(x_test,y_test)])
xgb_roc_score= roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:,1])
print(f'xgb_roc_score: {xgb_roc_score:.5f}')

xgb_clf2 = XGBClassifier(n_estimators=5, random_state=12, max_depth=5, min_child_weight=3, colsample_bytree=0.5)
xgb_clf2.fit(x_train, y_train, eval_set=[(x_test,y_test)])
xgb_roc_score2= roc_auc_score(y_test, xgb_clf2.predict_proba(x_test)[:,1], average='weighted')

pred2 = xgb_clf2.predict(x_test)