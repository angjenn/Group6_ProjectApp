import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Dummy data for training
X = np.array([
    [30, 1, 1],  # [duration, type (0=Running, 1=Strength, 2=HIIT), intensity (0=Easy, 1=Moderate, 2=Hard)]
    [45, 0, 2],
    [20, 2, 0],
    [60, 1, 1],
    [15, 0, 0]
])

y = np.array([
    [1, 10, 2, 30],  # Example workout plan representation (e.g., sets, reps, duration)
    [2, 15, 3, 45],
    [1, 5, 1, 20],
    [3, 12, 4, 60],
    [1, 8, 2, 15]
])

model = Sequential([
    Dense(64, input_shape=(3,), activation='relu'),
    Dense(64, activation='relu'),
    Dense(4)  # Output layer with 4 neurons for the workout plan representation
])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=50)

model.save('workout_model.h5')
