import os
import json
import requests
import re
import base64
from datetime import datetime
from functools import wraps
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from utils import read_image_from_bytes, preprocess, to_base64_png, overlay_heatmap_on_image
from infer import SkinModel
from models import db, User, PatientRecord

# Initialize Flask app
# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# For Vercel deployment, adjust paths if running from root
if os.path.basename(BASE_DIR) == 'backend':
    # Running from backend directory (local development)
    pass
else:
    # Running from root directory (Vercel deployment)
    BASE_DIR = os.path.join(BASE_DIR, 'backend')

MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(BASE_DIR, "saved_model/model.keras"))
LABELS_PATH = os.environ.get("LABELS_PATH", os.path.join(BASE_DIR, "labels.json"))

app = Flask(__name__, 
           template_folder=os.path.join(BASE_DIR, 'static', 'templates'),
           static_folder=os.path.join(BASE_DIR, 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///skin_lesion_classifier.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Load model
try:
    model = SkinModel(MODEL_PATH, LABELS_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Model loading error: {e}")
    model = None

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")
        # Continue anyway - tables might already exist

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

# ==================== Authentication Routes ====================

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        
        # Validation
        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        if request.is_json:
            return jsonify({"success": "Registration successful. Please log in."}), 201
        else:
            return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        username = data.get("username", "").strip()
        password = data.get("password", "")
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401
        
        login_user(user, remember=data.get("remember", False))
        
        if request.is_json:
            return jsonify({"success": "Login successful"}), 200
        else:
            return redirect(url_for("index"))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for("index"))

# ==================== Main Routes ====================

@app.route("/")
def index():
    """Home page"""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    """Predict skin lesion and save to patient history"""
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
    
    # Convert original image to base64
    image_b64 = to_base64_png(orig)
    
    # Get additional form data
    body_parts = request.form.get("body_parts", "").strip()
    notes = request.form.get("notes", "").strip()
    
    # Save to patient history
    top_prediction = decoded[0]["label"]
    confidence = decoded[0]["prob"]
    
    patient_record = PatientRecord(
        user_id=current_user.id,
        image_filename=file.filename,
        image_base64=image_b64,
        top_prediction=top_prediction,
        confidence=confidence,
        all_predictions=json.dumps(decoded),
        heatmap_base64=heatmap_b64,
        body_parts=body_parts,
        notes=notes,
        status='pending'
    )
    
    db.session.add(patient_record)
    db.session.commit()
    
    return render_template(
        "result.html",
        predictions=decoded,
        top_label=top_prediction,
        heatmap_png_base64=heatmap_b64,
        record_id=patient_record.id
    )

@app.route("/patient-history")
@login_required
def patient_history():
    """Display patient's analysis history"""
    page = request.args.get("page", 1, type=int)
    per_page = 10
    
    # Get records for current user, ordered by newest first
    records = PatientRecord.query.filter_by(user_id=current_user.id).order_by(
        PatientRecord.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return render_template(
        "patient_history.html",
        records=records,
        disease_info=DISEASE_INFO
    )

@app.route("/patient-history/<int:record_id>")
@login_required
def record_detail(record_id):
    """View details of a specific patient record"""
    record = PatientRecord.query.get_or_404(record_id)
    
    # Authorization check - ensure user owns this record
    if record.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Parse predictions JSON
    predictions = json.loads(record.all_predictions) if record.all_predictions else []
    
    return render_template(
        "record_detail.html",
        record=record,
        predictions=predictions,
        disease_info=DISEASE_INFO
    )

@app.route("/api/update-record/<int:record_id>", methods=["PUT"])
@login_required
def update_record(record_id):
    """Update patient record notes and follow-up date"""
    record = PatientRecord.query.get_or_404(record_id)
    
    # Authorization check
    if record.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    
    if "notes" in data:
        record.notes = data["notes"].strip()
    
    if "follow_up_date" in data:
        if data["follow_up_date"]:
            record.follow_up_date = datetime.fromisoformat(data["follow_up_date"])
    
    if "status" in data:
        if data["status"] in ['pending', 'reviewed', 'archived']:
            record.status = data["status"]
    
    db.session.commit()
    return jsonify({"success": "Record updated successfully"}), 200

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

# ==================== Doctor Finder Routes ====================

def find_doctors_internal(location, lesion_type):
    """Helper function for finding doctors"""
    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "Dermatologist",
            "address": f"{location.title()}, Medical Center",
            "phone": "(555) 123-4567",
            "rating": "4.8",
            "latitude": 40.7228,
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
    """Chatbot API endpoint"""
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
    """Find doctors endpoint"""
    data = request.json
    location = data.get("location", "")
    lesion_type = data.get("lesion_type", "")
    
    if not location or not lesion_type:
        return jsonify({"error": "Location and lesion type are required"}), 400
    
    return find_doctors_internal(location, lesion_type)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

@app.before_request
def before_request():
    """Make current_user available to all templates"""
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
