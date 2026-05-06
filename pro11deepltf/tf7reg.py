# 단순선형회귀 모델 작성
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
import numpy as np

# feature, label을 2차원 형태로 입력하기 위함
xdata = np.array([1,2,3,4,5], dtype='float32').reshape(-1,1)
ydata = np.array([1.2,2.0,3.0,3.5,5.5]).reshape(-1,1)
print('상관 계수 :', np.corrcoef(xdata.ravel(), ydata.ravel()))

model = Sequential()
model.add(Input(shape=(1, )))
model.add(Dense(units=5, activation='relu'))
model.add(Dense(units=1, activation='linear')) # 'linear':계산된 값을 그대로 출력
print(model.summary())

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])
# loss = 'mse' : 회귀분석 모델에서는 mean_squared_error 사용

model.fit(x=xdata, y=ydata, epochs=10, batch_size=1, verbose=1, shuffle=True)
# shuffle=True : default

loss_eval = model.evaluate(x=xdata, y=ydata)
print('loss_eval :', loss_eval)

pred = model.predict(xdata)
print('pred :', pred.ravel())
print('real :', ydata.ravel())

print('결정계수(R2, 설명력)')
from sklearn.metrics import r2_score
print('설명력 :', r2_score(ydata, pred))

import matplotlib.pyplot as plt
plt.scatter(xdata, ydata, color ='r', marker='o', label='real')
plt.plot(xdata, pred, 'b--', label='pred')
plt.show()

# 새로운 값으로 추추