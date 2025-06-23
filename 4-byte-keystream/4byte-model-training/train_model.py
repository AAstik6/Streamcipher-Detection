import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# STEP 1: Load your dataset
df = pd.read_csv("all_ciphers_8byte.csv")  # Your combined RC4/TRIVIUM/ESPRESSO samples

# STEP 2: Encode the 'label' column into numbers
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["label"])       # RC4 → 0, TRIVIUM → 1, ESPRESSO → 2
y_cat = to_categorical(y)                          # One-hot encoding for softmax

# STEP 3: Normalize 8 input byte columns (0–255 → 0–1)
X = df.drop("label", axis=1) / 255.0

# STEP 4: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, random_state=42
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.initializers import HeUniform

model = Sequential()
model.add(Dense(128, input_shape=(8,), activation='relu', kernel_initializer=HeUniform()))
model.add(Dense(64, activation='relu', kernel_initializer=HeUniform()))
model.add(Dense(32, activation='relu', kernel_initializer=HeUniform()))
model.add(Dense(3, activation='softmax'))  # 3 output classes

# STEP 6: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# STEP 7: Train the model
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=64,           # Smaller batches help sometimes
    validation_split=0.1
)

# STEP 8: Evaluate on test data
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\n✅ Test Accuracy: {accuracy:.4f}")

# STEP 9: Save the trained model
model.save("cipher_nn_model.h5")
print("💾 Model saved as 'cipher_nn_model.h5'")

# STEP 10: Save a training graph
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Training Accuracy')
plt.legend()
plt.grid(True)
plt.savefig("training_plot.png")
print("📊 Training plot saved as 'training_plot.png'")

model.save("improved_cipher_model.h5")