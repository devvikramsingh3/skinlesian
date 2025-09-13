import os
import json
import requests
import re
from flask import Flask, request, render_template, jsonify
from utils import read_image_from_bytes, preprocess, to_base64_png, overlay_heatmap_on_image
from infer import SkinModel

MODEL_PATH = os.environ.get("MODEL_PATH", "saved_model/model.keras")
LABELS_PATH = os.environ.get("LABELS_PATH", "labels.json")

app = Flask(__name__, 
           template_folder=os.path.join('static', 'templates'),
           static_folder='static')

model = SkinModel(MODEL_PATH, LABELS_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    file_bytes = file.read()
    orig = read_image_from_bytes(file_bytes)
    img_batch = preprocess(orig)

    probs = model.predict_probs(img_batch)
    decoded = model.decode(probs)

    heatmap = model.gradcam(img_batch)
    overlay_bgr = overlay_heatmap_on_image(orig, heatmap)
    heatmap_b64 = to_base64_png(overlay_bgr)

    return render_template(
        "result.html",
        predictions=decoded,
        top_label=decoded[0]["label"],
        heatmap_png_base64=heatmap_b64
    )

# Disease information database
DISEASE_INFO = {
    "akiec": {
        "name": "Actinic Keratoses and Intraepithelial Carcinoma",
        "description": "Actinic Keratoses are pre-cancerous lesions caused by sun damage. Intraepithelial Carcinoma (Bowen's disease) is an early form of skin cancer that hasn't spread beyond the epidermis.",
        "treatment": "Treatment options include cryotherapy, topical medications, photodynamic therapy, curettage, or surgical excision.",
        "specialist": "Dermatologist, Dermatologic Surgeon, Oncologist"
    },
    "bcc": {
        "name": "Basal Cell Carcinoma",
        "description": "The most common type of skin cancer. It rarely spreads but can be locally destructive if not treated.",
        "treatment": "Treatment options include surgical excision, Mohs surgery, radiation therapy, or topical medications for superficial cases.",
        "specialist": "Dermatologist, Mohs Surgeon, Surgical Oncologist"
    },
    "bkl": {
        "name": "Benign Keratosis-like Lesions",
        "description": "This category includes seborrheic keratoses, solar lentigo, and lichen-planus like keratoses. These are benign (non-cancerous) skin growths.",
        "treatment": "Treatment is usually not necessary unless for cosmetic reasons. Options include cryotherapy, curettage, or laser therapy.",
        "specialist": "Dermatologist"
    },
    "df": {
        "name": "Dermatofibroma",
        "description": "A common benign skin nodule that often appears as a firm bump on the skin, usually on the legs.",
        "treatment": "Treatment is usually not necessary. If desired for cosmetic reasons, surgical excision can be performed.",
        "specialist": "Dermatologist"
    },
    "mel": {
        "name": "Melanoma",
        "description": "The most serious type of skin cancer. Melanoma can spread to other parts of the body if not caught early.",
        "treatment": "Treatment depends on the stage and may include surgical excision, lymph node biopsy, immunotherapy, targeted therapy, or radiation therapy.",
        "specialist": "Dermatologist, Surgical Oncologist, Medical Oncologist"
    },
    "nv": {
        "name": "Melanocytic Nevi (Moles)",
        "description": "Common benign skin growths that develop from melanocytes. Most moles are harmless, but changes in appearance can be a sign of melanoma.",
        "treatment": "Regular monitoring is recommended. Removal is typically only necessary if the mole shows suspicious changes or for cosmetic reasons.",
        "specialist": "Dermatologist"
    },
    "vasc": {
        "name": "Vascular Lesions",
        "description": "This category includes hemangiomas, angiomas, and pyogenic granulomas. These are benign growths made up of blood vessels.",
        "treatment": "Treatment options include laser therapy, sclerotherapy, surgical excision, or observation depending on the specific type and symptoms.",
        "specialist": "Dermatologist, Vascular Surgeon"
    }
}

# Helper function for finding doctors (used by both endpoints)
def find_doctors_internal(location, lesion_type):
    # Mock data for demonstration with coordinates
    # In a real application, these would come from a geocoding API or database
    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "Dermatologist",
            "address": f"{location.title()}, Medical Center",
            "phone": "(555) 123-4567",
            "rating": "4.8",
            "latitude": 40.7228,  # Mock coordinates based on NYC
            "longitude": -74.0260
        },
        {
            "name": "Dr. Michael Chen",
            "specialty": "Dermatologic Surgeon",
            "address": f"{location.title()}, Skin Care Clinic",
            "phone": "(555) 987-6543",
            "rating": "4.9",
            "latitude": 40.6978,
            "longitude": -73.9960
        },
        {
            "name": "Dr. Emily Rodriguez",
            "specialty": "Dermatopathologist",
            "address": f"{location.title()}, University Hospital",
            "phone": "(555) 456-7890",
            "rating": "4.7",
            "latitude": 40.7328,
            "longitude": -73.9810
        },
        {
            "name": "Dr. James Wilson",
            "specialty": "Oncologist",
            "address": f"{location.title()}, Cancer Treatment Center",
            "phone": "(555) 789-0123",
            "rating": "4.9",
            "latitude": 40.6878,
            "longitude": -74.0210
        },
        {
            "name": "Dr. Lisa Park",
            "specialty": "Dermatologist",
            "address": f"{location.title()}, Downtown Clinic",
            "phone": "(555) 234-5678",
            "rating": "4.6",
            "latitude": 40.7428,
            "longitude": -74.0360
        }
    ]
    
    response_text = f"I found these specialists in {location.title()} who can help with your condition:"
    return jsonify({"response": response_text, "doctors": doctors})

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    message = data.get("message", "").lower()
    lesion_type = data.get("lesion_type", "")
    context = data.get("context", "")
    
    # If context is provided from the result page, use it as the lesion type
    if context and not lesion_type:
        for key in DISEASE_INFO.keys():
            if key in context.lower() or DISEASE_INFO[key]["name"].lower() in context.lower():
                lesion_type = key
                break
    
    # If no specific lesion type is provided, try to identify it from the message
    if not lesion_type:
        for key in DISEASE_INFO.keys():
            if key in message or DISEASE_INFO[key]["name"].lower() in message:
                lesion_type = key
                break
    
    # If we have a lesion type, provide specific information
    if lesion_type and lesion_type in DISEASE_INFO:
        info = DISEASE_INFO[lesion_type]
        
        if "what is" in message or "tell me about" in message or "information" in message:
            response = f"**{info['name']}**: {info['description']}"
        elif "treatment" in message or "how to treat" in message or "cure" in message:
            response = f"**Treatment for {info['name']}**: {info['treatment']}"
        elif "doctor" in message or "specialist" in message or "who should" in message:
            response = f"**Recommended specialists for {info['name']}**: {info['specialist']}"
        elif "find" in message or "near me" in message or "nearby" in message or "location" in message:
            # Check if we have a location in the message
            import re
            location_match = re.search(r'in ([a-zA-Z\s]+)', message)
            if location_match:
                location = location_match.group(1).strip()
                return find_doctors_internal(location, lesion_type)
            else:
                response = f"I can help you find specialists for {info['name']}. Please share your location or enter a city name to find doctors nearby."
        else:
            response = f"I can provide information about {info['name']}. You can ask about what it is, treatment options, or specialists to consult."
    else:
        response = "I'm here to help with information about skin lesions. Please specify which type of lesion you'd like to know about, or ask about your diagnosis results."
    
    return jsonify({"response": response})

@app.route("/api/find-doctors", methods=["POST"])
def find_doctors():
    data = request.json
    location = data.get("location", "")
    lesion_type = data.get("lesion_type", "")
    
    if not location or not lesion_type:
        return jsonify({"error": "Location and lesion type are required"}), 400
    
    # Use the internal function to maintain consistency
    return find_doctors_internal(location, lesion_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
