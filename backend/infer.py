import numpy as np
import json
import os

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    print("WARNING: TensorFlow not available. Using mock predictions.")
    TF_AVAILABLE = False

class SkinModel:
    def __init__(self, model_path="saved_model/model.keras", labels_path="labels.json"):
        # Load labels
        with open(labels_path, "r") as f:
            self.labels = json.load(f)
        self.target_size = (224, 224)
        
        # Load the actual model
        self.model = None
        if TF_AVAILABLE:
            try:
                self.model = tf.keras.models.load_model(model_path)
                print(f"Model loaded successfully from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Falling back to mock predictions")
        else:
            print("TensorFlow not available - using mock predictions")
        
        print(f"Model initialized with labels: {self.labels}")

    def predict_probs(self, img_batch):
        # Use the real model if available
        if self.model is not None:
            try:
                predictions = self.model.predict(img_batch)
                # If predictions is a batch, take the first one
                if len(predictions.shape) > 1:
                    predictions = predictions[0]
                return predictions
            except Exception as e:
                print(f"Error during prediction: {e}")
                print("Falling back to mock predictions")
        
        # Fall back to mock predictions if model is not available or prediction fails
        mock_probs = np.random.rand(len(self.labels))
        # Normalize to sum to 1
        mock_probs = mock_probs / np.sum(mock_probs)
        return mock_probs

    def decode(self, probs):
        results = []
        for idx, p in enumerate(probs):
            results.append({"rank": idx+1, "label": self.labels[idx], "prob": float(p)})
        results.sort(key=lambda x: x["prob"], reverse=True)
        return results

    def gradcam(self, img_tensor):
        # If model is not available, return mock heatmap
        if self.model is None:
            # Mock GradCAM - generate a random heatmap
            heatmap = np.random.rand(28, 28)  # Smaller size for efficiency
            heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-8)
            # Resize using simple interpolation
            from PIL import Image
            heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
            heatmap_img = heatmap_img.resize(self.target_size, Image.Resampling.LANCZOS)
            return np.array(heatmap_img) / 255.0
            
        try:
            # Get the last convolutional layer
            last_conv_layer = None
            for layer in reversed(self.model.layers):
                if isinstance(layer, tf.keras.layers.Conv2D):
                    last_conv_layer = layer
                    break
                    
            if last_conv_layer is None:
                # If no conv layer found, fall back to mock
                print("No convolutional layer found for GradCAM, using mock heatmap")
                heatmap = np.random.rand(28, 28)
                heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-8)
                from PIL import Image
                heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
                heatmap_img = heatmap_img.resize(self.target_size, Image.Resampling.LANCZOS)
                return np.array(heatmap_img) / 255.0
                
            # Create a model that outputs both the predictions and the activations of the last conv layer
            grad_model = tf.keras.models.Model(
                inputs=[self.model.inputs],
                outputs=[self.model.output, last_conv_layer.output]
            )
            
            # Compute the gradient of the top predicted class for our input image
            # with respect to the activations of the last conv layer
            with tf.GradientTape() as tape:
                preds, conv_outputs = grad_model(img_tensor)
                top_pred_index = tf.argmax(preds[0])
                top_class_channel = preds[:, top_pred_index]
                
            # This is the gradient of the top predicted class with respect
            # to the output feature map of the last conv layer
            grads = tape.gradient(top_class_channel, conv_outputs)
            
            # Vector of mean intensity of the gradient over a specific feature map channel
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight the channels of the conv layer output by the gradient values
            conv_outputs = conv_outputs[0]
            heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
            heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + tf.keras.backend.epsilon())
            heatmap = heatmap.numpy()
            
            # Resize using PIL
            from PIL import Image
            heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
            heatmap_img = heatmap_img.resize(self.target_size, Image.Resampling.LANCZOS)
            return np.array(heatmap_img) / 255.0
            
        except Exception as e:
            print(f"Error generating GradCAM: {e}")
            print("Falling back to mock heatmap")
            # Fall back to mock heatmap
            heatmap = np.random.rand(28, 28)
            heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-8)
            from PIL import Image
            heatmap_img = Image.fromarray(np.uint8(255 * heatmap))
            heatmap_img = heatmap_img.resize(self.target_size, Image.Resampling.LANCZOS)
            return np.array(heatmap_img) / 255.0
