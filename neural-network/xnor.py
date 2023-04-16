import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Training data (inputs)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)

# Training labels (outputs)
y = np.array([[1], [0], [0], [1]], dtype=float)

# Create the neural network model
model = keras.Sequential(
    [
        layers.Dense(2, activation="sigmoid", input_shape=(2,)),
        layers.Dense(1, activation="sigmoid"),
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(X, y, epochs=10000, verbose=0)

# Evaluate the model on the training data
loss, accuracy = model.evaluate(X, y)
print(f"Loss: {loss}, Accuracy: {accuracy}")

# Test the model
predictions = model.predict(X)
print("Predictions:")
for i, pred in enumerate(predictions):
    print(f"Input: {X[i]}, Expected: {y[i]}, Prediction: {pred}")
