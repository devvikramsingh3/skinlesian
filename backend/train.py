import tensorflow as tf
from tensorflow.keras import layers, models
import json, os

# ⚠️ Adjust this path to where your dataset is stored
DATASET_DIR = os.environ.get("DATASET_DIR", "dataset")  
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
MODEL_DIR = "saved_model"
LABELS_FILE = "labels.json"

def build_model(num_classes):
    base = tf.keras.applications.EfficientNetB0(
        include_top=False, input_shape=(224,224,3), weights="imagenet"
    )
    base.trainable = False  # transfer learning (freeze backbone)

    inputs = layers.Input(shape=(224,224,3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    model = models.Model(inputs, outputs)
    return model

def main():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATASET_DIR, "train"),
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATASET_DIR, "val"),
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names
    print("Classes:", class_names)

    model = build_model(len(class_names))
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save(os.path.join(MODEL_DIR, "model.keras"))
    with open(os.path.join(MODEL_DIR, LABELS_FILE), "w") as f:
        json.dump(class_names, f)

    print("✅ Training complete. Model saved in", MODEL_DIR)

if __name__ == "__main__":
    main()
