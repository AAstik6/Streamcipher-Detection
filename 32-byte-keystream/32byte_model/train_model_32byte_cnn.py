import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv("all_ciphers_32byte.csv")

# Step 2: Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["label"])       # RC4=0, TRIVIUM=1, ESPRESSO=2
y_cat = to_categorical(y)

# Step 3: Normalize input bytes (0–255 → 0–1)
X = df.drop("label", axis=1) / 255.0

# Step 4: Reshape input for CNN: (samples, 32, 1)
X = np.expand_dims(X.values, axis=-1)

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, random_state=42
)

# Step 6: Build CNN model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(32, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))  # 3 classes

# Step 7: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 8: Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.1
)

# Step 9: Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {accuracy:.4f}")

# Step 10: Save the model
model.save("cnn_model_32byte.h5")
print(" Model saved as cnn_model_32byte.h5")

# Step 11: Plot training history
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.title("CNN Model Accuracy (32-byte keystreams)")
plt.savefig("cnn_training_plot_32byte.png")
print("Training plot saved as cnn_training_plot_32byte.png")