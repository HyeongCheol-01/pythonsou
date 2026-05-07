import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/zoo.csv")
print(datas.head(3))
print(datas.info())

x_data = datas.iloc[:, :-1].astype("float32").values
y_data = datas.iloc[:, -1].astype("int32").values
print(x_data[0], x_data.shape)
print(y_data[0], sorted(set(map(int, y_data))))

np.random.seed(42)
tf.keras.utils.set_random_seed(42)


x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, \
                                    test_size=0.2, random_state=42, stratify=y_data)
print(x_train.shape, x_test.shape)

model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(units=64, activation='relu'),
    Dropout(rate=0.3),
    Dense(units=32, activation='relu'),
    Dropout(rate=0.3),
    Dense(units=7, activation='softmax')
])
print(model.summary())

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',   # 레이블 원핫 내부적으로 처리
            # loss = 'categorical_crossentropy',    # 레이블 원핫되어 있어야 함
            metrics=['accuracy'])

print("\n--- 모델 학습 시작 ---")
history = model.fit(x_train, y_train, 
                    epochs=100, 
                    batch_size=16, 
                    validation_split=0.2, 
                    verbose=0) # 출력이 길어지므로 0으로 설정. 과정을 보려면 1이나 2로 변경하세요.


test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n최종 테스트 정확도: {test_acc * 100:.2f}%")


plt.figure(figsize=(12, 5))

# Loss 시각화
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

# Accuracy 시각화
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print('\n새로운 값으로 분류 예측')
new_data = np.array([[0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 4., 0., 0., 1.]], dtype='float32')
probs = model.pridict(new_data)
pred_class= (np.argmax(probs))
print('분류 예측 확률: ', probs.ravel())
print('분류 예측 라벨: ', pred_class)