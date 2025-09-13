import tensorflow as tf
from tensorflow.keras import layers, models
import json
import os
import numpy as np

# Create a simple model for testing
def create_test_model():
    # Define model architecture (simple CNN)
    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Conv2D(16, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(7, activation='softmax')  # 7 classes from labels.json
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Create a directory for the model if it doesn't exist
    os.makedirs('saved_model', exist_ok=True)
    
    # Save the model
    model.save('saved_model/model.keras')
    
    print("Test model created and saved to saved_model/model.keras")
    return model

if __name__ == "__main__":
    create_test_model()