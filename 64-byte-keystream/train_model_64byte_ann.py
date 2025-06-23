import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv("all_ciphers_64byte.csv")

# Step 2: Encode the labels (RC4=0, TRIVIUM=1, ESPRESSO=2)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["label"])
y_cat = to_categorical(y)

# Step 3: Normalize the inputs (0–255 → 0–1)
X = df.drop("label", axis=1) / 255.0

# Step 4: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, random_state=42
)

# Step 5: Build a simple ANN model
model = Sequential()
model.add(Dense(128, input_shape=(64,), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))  # 3 cipher classes

# Step 6: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 7: Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=128,
    validation_split=0.1
)

# Step 8: Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {accuracy:.4f}")

# Step 9: Save the model
model.save("ann_model_64byte.h5")
print("Model saved as ann_model_64byte.h5")

# Step 10: Save training accuracy plot
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.title("ANN Training Accuracy (64-byte keystreams)")
plt.savefig("ann_training_plot_64byte.png")
print("Training plot saved as ann_training_plot_64byte.png")