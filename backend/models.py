from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for patient authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to patient records
    patient_records = db.relationship('PatientRecord', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class PatientRecord(db.Model):
    """Patient record model for storing analysis history"""
    __tablename__ = 'patient_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Image and analysis data
    image_filename = db.Column(db.String(255), nullable=True)
    image_base64 = db.Column(db.Text, nullable=True)  # Store base64 encoded image
    
    # Prediction results
    top_prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    all_predictions = db.Column(db.Text, nullable=True)  # JSON string of all predictions
    heatmap_base64 = db.Column(db.Text, nullable=True)
    
    # Clinical notes
    body_parts = db.Column(db.String(255), nullable=True)  # e.g., 'arm', 'face', 'leg'
    notes = db.Column(db.Text, nullable=True)
    
    # Follow-up status
    follow_up_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, reviewed, archived
    doctor_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PatientRecord {self.id} - {self.top_prediction}>'
