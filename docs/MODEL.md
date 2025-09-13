# Model Architecture

## Overview

The skin lesion classifier uses a transfer learning approach with EfficientNetB0 as the backbone. This document provides details about the model architecture, training process, and performance metrics.

## Architecture Details

```
Model: Sequential
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
EfficientNetB0 (Functional)  (None, 7, 7, 1280)        4,049,571 
_________________________________________________________________
GlobalAveragePooling2D      (None, 1280)              0         
_________________________________________________________________
Dense                       (None, 7)                 8,967     
=================================================================
Total params: 4,058,538
Trainable params: 8,967 (Dense layer only)
Non-trainable params: 4,049,571 (Frozen EfficientNetB0)
```

## Transfer Learning Approach

1. **Base Model**: EfficientNetB0 pre-trained on ImageNet
2. **Feature Extraction**: The base model is frozen (weights not updated during training)
3. **Custom Classification Head**: A Global Average Pooling layer followed by a Dense layer with softmax activation

## Input Processing

- Input image size: 224x224 pixels
- RGB color channels
- Pixel values normalized to [0, 1]
- Data augmentation during training:
  - Random horizontal and vertical flips
  - Random rotation (±15 degrees)
  - Random zoom (±10%)

## Training Details

- **Optimizer**: Adam
- **Loss Function**: Sparse Categorical Crossentropy
- **Batch Size**: 32
- **Epochs**: 10
- **Learning Rate**: 0.001

## Performance Metrics

The model achieves the following performance on the validation set:

- **Accuracy**: ~80-85%
- **Precision**: ~78-83%
- **Recall**: ~75-80%
- **F1 Score**: ~76-81%

## Class-wise Performance

Performance varies across different lesion types:

- Best performance on: nv (Melanocytic Nevi), bkl (Benign Keratosis-like Lesions)
- Moderate performance on: bcc (Basal Cell Carcinoma), akiec (Actinic Keratoses)
- Lower performance on: mel (Melanoma), df (Dermatofibroma), vasc (Vascular Lesions)

## Visualization

The model includes Grad-CAM visualization to highlight regions that influenced the prediction, providing interpretability for the classification results.

## Future Improvements

- Fine-tuning the base model instead of just feature extraction
- Ensemble methods combining multiple models
- More sophisticated data augmentation techniques
- Class balancing to address imbalanced distribution in the dataset
- Testing with different backbone architectures (ResNet, DenseNet, etc.)