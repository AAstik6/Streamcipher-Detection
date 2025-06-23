import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

df = pd.read_csv("all_ciphers_24byte.csv")

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["label"])
y_cat = to_categorical(y) # onehot encoding

X = df.drop("label",axis=1) / 255.0

X_train, X_test, y_train, y_test = train_test_split(
  X, y_cat, test_size=0.2, random_state=42
)

from tensorflow.keras.layers import Dropout

model = Sequential()
model.add(Dense(256, input_shape=(24,), activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=64,
    validation_split=0.1
)

## tells how well the model works with unseen data
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nTest accuracy: {accuracy:.4f}") 

model.save("model_24byte.h5")
print("Saved as model_24byte.h5")

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')

plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.title("Model Accuracy (24-Byte)")

plt.savefig("training_plot_24byte.png")
print("Plot saved as training_plot_24byte.png")



