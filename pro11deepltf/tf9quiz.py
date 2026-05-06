import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. 데이터 준비
data = pd.read_csv("https://raw.githubusercontent.com/data-8/materials-fa17/refs/heads/master/lec/galton.csv")
data_male = data[data['gender'] == 'male'].copy()

# 💡 모델 입력을 위해 2차원 배열로 명시적 변환
x_data = data_male['father'].values.reshape(-1, 1)
y_data = data_male['childHeight'].values.reshape(-1, 1)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

# ==========================================
print('\n--- Sequential API 모델 생성 ---')
# ==========================================
model = Sequential()
model.add(Input(shape=(1, )))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='linear'))
print(model.summary())

model.compile(loss='mse', optimizer='adam', metrics=['mse'])

# 💡 validation_split 삭제 (validation_data만 사용)
history = model.fit(
    x_train, 
    y_train, 
    validation_data=(x_test, y_test), 
    epochs=100, 
    batch_size=32, 
    verbose=0 # 출력창이 너무 길어지는 것을 방지 (원하시면 2로 변경)
)



plt.figure(figsize=(8, 5))
plt.plot(history.history['mse'], label='Train MSE', color='blue')
plt.plot(history.history['val_mse'], label='Test MSE', color='red', linestyle='--')
plt.title('Sequential Model MSE (Train vs Test)')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
print('\n--- Functional API 모델 생성 ---')
# ==========================================
inputs = Input(shape=(1, ), name='input_layer') 
x = Dense(units=16, activation='relu', name='hidden_layer1')(inputs)
x = Dense(units=8, activation='relu', name='hidden_layer2')(x)
outputs = Dense(units=1, activation='linear', name='output_layer')(x)

func_model = Model(inputs=inputs, outputs=outputs)
print(func_model.summary())

func_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

# 💡 validation_split 삭제 및 history_func 변수에 저장
history_func = func_model.fit(
    x_train, 
    y_train, 
    validation_data=(x_test, y_test),
    epochs=100, 
    batch_size=32, 
    verbose=0
)



# 💡 history_func.history로 그래프 그리기
plt.figure(figsize=(8, 5))
plt.plot(history_func.history['mse'], label='Train MSE', color='blue')
plt.plot(history_func.history['val_mse'], label='Test MSE', color='red', linestyle='--')
plt.title('Functional Model MSE (Train vs Test)')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()
plt.grid(True)
plt.show()

new_father_height = np.array([[70.0], [75.0]]) # 예: 70인치, 75인치 (2차원 배열 형태 유지)
predicted_son_height = func_model.predict(new_father_height)
from sklearn.metrics import r2_score
print('설명력 :', r2_score(y_test, model.predict(x_test)))
print('설명력 :', r2_score(y_test, func_model.predict(x_test)))
print("\n--- 예측 결과 ---")
print(f"아버지 키 70인치 -> 아들 키 예측: {predicted_son_height[0][0]:.2f}인치")
print(f"아버지 키 75인치 -> 아들 키 예측: {predicted_son_height[1][0]:.2f}인치")