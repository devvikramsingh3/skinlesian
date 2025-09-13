# Skin Lesion Classifier

An AI-powered web application for classifying skin lesions into different categories using computer vision and machine learning. This project uses the HAM10000 dataset from the International Skin Imaging Collaboration (ISIC) to train a deep learning model for skin lesion classification.

## Features

- Upload and analyze dermatoscopic images
- Classify skin lesions into 7 different categories
- Visualize model attention with Grad-CAM heatmaps
- Modern, responsive UI for desktop and mobile devices
- Interactive chatbot for additional information
- Find nearby specialists based on diagnosis

## Application Preview

![Application Interface](docs/images/app_mockup.svg)

*This mockup shows the main interface of the application with upload area, classification results, heatmap visualization, and AI assistant.*

## Categories of Skin Lesions

The classifier can identify the following types of skin lesions:

- **akiec**: Actinic Keratoses and Intraepithelial Carcinoma
- **bcc**: Basal Cell Carcinoma
- **bkl**: Benign Keratosis-like Lesions
- **df**: Dermatofibroma
- **mel**: Melanoma
- **nv**: Melanocytic Nevi
- **vasc**: Vascular Lesions

## Dataset

This project uses the HAM10000 dataset ("Human Against Machine with 10000 training images") from the ISIC Archive. The dataset consists of dermatoscopic images from different populations, acquired and stored by different modalities. The dataset includes the following information:

- Dermatoscopic images of common pigmented skin lesions
- Metadata including diagnosis, age, sex, and localization
- 7 diagnostic categories with both malignant and benign lesions

For more information about the dataset, visit the [ISIC Archive](https://www.isic-archive.com/).

## Model Architecture

The classification model uses a transfer learning approach with EfficientNetB0 as the backbone:

- Pre-trained EfficientNetB0 base (trained on ImageNet)
- Global Average Pooling layer
- Dense output layer with softmax activation
- Input image size: 224x224 pixels

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- HAM10000 dataset (or similar dermatoscopic image dataset)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/skin-lesion-classifier.git
   cd skin-lesion-classifier
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Download the HAM10000 dataset from the [ISIC Archive](https://www.isic-archive.com/) or use your own dataset of dermatoscopic images.

## Usage

### Preparing the Dataset

1. Place your dataset in the appropriate directory structure or use the provided script to prepare it:
   ```
   cd backend
   python prepare_datasets.py
   ```

### Training the Model

1. Train the model using the prepared dataset:
   ```
   cd backend
   python train.py
   ```

### Running the Application

1. Start the Flask application:
   ```
   cd backend
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Upload a dermatoscopic image and get the classification results.

### Using the Application

1. Upload an image using the file selector on the home page
2. View the classification results and probability distribution
3. Examine the Grad-CAM heatmap showing regions of interest
4. Use the chatbot for additional information about the diagnosis
5. Find specialists near your location based on the diagnosis

## Project Structure

```
skin-lesion-classifier/
├── backend/
│   ├── app.py                 # Flask web application
│   ├── infer.py               # Model inference code
│   ├── utils.py               # Utility functions
│   ├── requirements.txt       # Python dependencies
│   ├── labels.json            # Class labels
│   ├── saved_model/           # Directory for model files
│   └── static/                # Static assets
│       ├── styles.css         # CSS styles
│       └── templates/         # HTML templates
│           ├── index.html     # Upload page
│           └── result.html    # Results page
```

## Disclaimer

This tool is for educational purposes only and should not be used for medical diagnosis. Always consult with a qualified healthcare provider for proper diagnosis and treatment of skin conditions.

## Contributing

Contributions are welcome! Here's how you can contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a Pull Request

### Areas for Improvement

- Add more sophisticated models or ensemble methods
- Improve the UI/UX design
- Add user authentication and result history
- Implement more advanced visualization techniques
- Add support for more image formats and sources

## Acknowledgements

- [ISIC Archive](https://www.isic-archive.com/) for providing the HAM10000 dataset
- [TensorFlow](https://www.tensorflow.org/) for the deep learning framework
- [Flask](https://flask.palletsprojects.com/) for the web framework

## License

MIT