# 자전거 공유 데이터로 다중선형회귀
# season, holiday, workingday, weather, temp, atemp, humidity, windspeed로 대여횟수(count) 예측
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
import platform

plt.rcParams['axes.unicode_minus'] = False

# 배열자료로 읽기 --> 판다스 안씀
# season(1), holiday(2), workingday(3), weather(4), temp(5), atemp(6), humidity(7), windspeed(8), count(11)
# casual(9), registered(10) 제외 
datas = np.loadtxt(
    "https://raw.githubusercontent.com/pykwon/python/master/data/train.csv",
    delimiter=",", skiprows=1,
    usecols=(1, 2, 3, 4, 5, 6, 7, 8, 11)
)
print(datas[:2], len(datas.shape))

# feature
x_data = datas[:, 0:-1]
print(x_data.shape)  # (N, 8)
scaler = MinMaxScaler(feature_range=(0, 1))
x_data = scaler.fit_transform(x_data)
print(x_data[:2])

# label
y_data = datas[:, -1]
print(y_data[:5])

print('train/test split 없이 모델 작성')
model = Sequential()
model.add(Input(shape=(8,)))
model.add(Dense(units=1, activation='linear'))

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])
hist = model.fit(x_data, y_data, epochs=200, verbose=0)
print('evaluate result:', model.evaluate(x_data, y_data, verbose=0))

pred = model.predict(x_data)
print(f'train/test split 없이 설명력: , {r2_score(y_data, pred)}')

# loss 시각화
plt.plot(hist.history['loss'], 'b', label='loss')
plt.title('Training Loss')
plt.xlabel('epoch')
plt.ylabel('mse loss')
plt.legend()
plt.show()

# 실제 vs 예측 시각화
plt.plot(y_data, 'b', label='real')
plt.plot(pred, 'r--', label='pred')
plt.legend()
plt.show()

print()
print('train/test split을 위한 모델 작성')
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.3, random_state=123, shuffle=False)
print(x_train.shape, x_test.shape)

model2 = Sequential()
model2.add(Input(shape=(8,)))
model2.add(Dense(units=1, activation='linear'))

model2.compile(loss='mse', optimizer='sgd', metrics=['mse'])
hist2 = model2.fit(x_train, y_train, epochs=200, verbose=0,
                    validation_split=0.15)
print('evaluate result:', model.evaluate(x_data, y_data, verbose=0))

pred2 = model2.predict(x_test)
print(f'train/test split 설명력: , {r2_score(y_test, pred2)}')

# loss / val_loss 시각화
plt.plot(hist2.history['loss'], 'b', label='loss')
plt.plot(hist2.history['val_loss'], 'r--', label='val_loss')
plt.title('Training Loss (train/test split)')
plt.xlabel('epoch')
plt.ylabel('mse loss')
plt.legend()
plt.show()

# 실제 vs 예측 시각화
plt.plot(y_data, 'b', label='real')
plt.plot(pred2, 'r--', label='pred2')
plt.legend()
plt.show()

# 딥러닝의 이슈 : 최적화와 일반화

# 새로운 데이터 입력 → 대여횟수 예측
print()
season     = float(input('계절(1=봄, 2=여름, 3=가을, 4=겨울): '))
holiday    = float(input('공휴일(0=평일, 1=공휴일): '))
workingday = float(input('근무일(0=비근무일, 1=근무일): '))
weather    = float(input('날씨(1=맑음, 2=안개, 3=눈/비, 4=폭우): '))
temp       = float(input('기온(섭씨): '))
atemp      = float(input('체감온도(섭씨): '))
humidity   = float(input('습도(0~100): '))
windspeed  = float(input('풍속: '))

new_data = np.array([[season, holiday, workingday, weather, temp, atemp, humidity, windspeed]])
new_data = scaler.transform(new_data)
result = model2.predict(new_data)
print(f'예측 대여횟수: {max(0, result[0][0]):.0f}대')