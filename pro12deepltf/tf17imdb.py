# imdb dataset으로 이진 분류 : 영화 리뷰(긍정,부정)
# train : 25000, test : 25000

from tensorflow.keras.datasets import imdb
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input, Embedding, LSTM, GlobalAveragePooling1D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# 자주 등장하는 단어 1만개만 사용
num_words = 10000  
(train_data, train_label), (test_data, test_label) = imdb.load_data(num_words = num_words)
print(type(train_data), train_data.shape)
print(type(test_data), test_data.shape)
print(train_data[0], len(train_data[0]))
# 전처리된 데이터로 각 리뷰(단어)사 숫자화
print(train_label[0])

# 참고로 이 리뷰 데이터 한 개를 원래 문장으로 보기
# 각 단어 인덱싱 확인
word_index = imdb.get_word_index()
# print('word_index :', word_index)

sorted_word_index = sorted(word_index.items(), key=lambda x:x[1])
for word, index in sorted_word_index[:10]:
    print(word, index)
    
reverse_word_index = {
    index + 3:word  # 특수 토큰 세 개가 선행 하므로
    for word, index in word_index.items()
}
# 특수 토큰
reverse_word_index[0] = "<PAD>"     # 패딩
reverse_word_index[1] = "<START>"   # 문장 시작
reverse_word_index[2] = "<UNK>"     # 모르는 단어
reverse_word_index[3] = "<UNUSED>"  # 사용 안함
# 0번째 리뷰 문장으로 복원
decord_review = " ".join(
    reverse_word_index.get(i, "?") for i in train_data[0]
    # i에 해당하는 단어가 있으면 그 단어 반환, 없으면 ? 반환
)
print("0번째 문장:",decord_review)
# load_data() 안에서는 0~3번을 특수 토큰으로 쓰기 때문에 실제 리뷰 데이터에서 the는 4
print("0번쨰 라벨:", train_label[0])

# 리뷰 길이 확인
review_len = [len(review) for review in train_data]
print('최소 길이 :', np.min(review_len))
print('최대 길이 :', np.max(review_len))
print('평균 길이 :', np.mean(review_len))
print('중앙 값 :', np.median(review_len))

plt.figure(figsize=(8,5))
plt.hist(review_len, bins=50)
plt.xlabel('리뷰길이')
plt.ylabel('건수')
plt.grid(True)
plt.show()

# padding : 리뷰 문장 길이가 다름. 모델에 넣기 전에 길이를 맞춤
# 각 리뷰를 최대 200 단어 index로 맞춤. 길면 앞부분 자르고, 짧으면 0을 채움
maxlen=200
x_train = pad_sequences(train_data, maxlen=maxlen)
x_test = pad_sequences(test_data, maxlen=maxlen)
y_train = np.array(train_label).astype(np.float32)
y_test = np.array(test_label).astype(np.float32)

# 모델 저장용 폴더 준비
MODEL_DIR = "./imdb_model/"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    
modelpath = "./imdb_model/imdb_best.keras"

model = Sequential([
    Input(shape=(maxlen, )),
    Embedding(
        input_dim=num_words, output_dim=32
        #밀집벡터화 : 실수 기반의 고정 크기에 실수값으로 채움. 예:[0.2, -0.1, 0.03, 0.5 ...]
    ),
    GlobalAveragePooling1D(),
    # 200개의 단어 벡터를 평균내서 리뷰전체를 하나의 32차원 벡터화. 
    Dense(units=32, activation='relu'),
    Dropout(0.3),
    Dense(units=16, activation='relu'),
    Dropout(0.3),
    Dense(units=1, activation='sigmoid')
])
print(model.summary())  # Total params  : 321,601 (1.23MB)

model.compile(optimizer=Adam(learning_rate=0.001), 
            loss='binary_crossentropy', 
            metrics=['accuracy'])
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

checkpoint = ModelCheckpoint(filepath=modelpath, 
                            monitor='val_loss', 
                            save_best_only=True, 
                            verbose=1)

history = model.fit(x_train, y_train, 
                    epochs=20, 
                    batch_size=128, 
                    validation_split=0.2, 
                    callbacks=[early_stop, checkpoint], 
                    verbose=1)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n최종 테스트 정확도: {test_acc * 100:.2f}%")

# 시각화 (Loss & Accuracy)
plt.figure(figsize=(12, 5))

# Loss 그래프
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

# Accuracy 그래프
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print('\n\n저장된 모델 읽어 분류 예측')
best_model = load_model(modelpath)

new_data = x_test[:5]
new_label = y_test[:5]
pred_prob = best_model.predict(new_data, verbose = 0)
pred_class = (pred_prob >= 0.5).astype(int).ravel()

print("\n--- 첫 5개 리뷰 예측 결과 확인 ---")
print("실제 정답 (Label):", new_label.astype(int))
print("모델 예측 (Class):", pred_class)
print("-" * 40)

# 결과를 보기 좋게 한 줄씩 출력
for i in range(5):
    real = "긍정(1)" if new_label[i] == 1 else "부정(0)"
    result = "긍정(1)" if pred_class[i] == 1 else "부정(0)"
    print(f'{i+1}번 리뷰 예측:{result}, 실제:{real}, 긍정확률:{pred_prob[i][0]}')