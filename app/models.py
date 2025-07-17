from . import db
from flask_login import UserMixin
from datetime import datetime
import json
from sqlalchemy.dialects.postgresql import JSON

class AnalysisMixin:
    def get_analysis(self):
        return json.loads(self.analysis_data) if self.analysis_data else {}
    
    def set_analysis(self, data):
        self.analysis_data = json.dumps(data, ensure_ascii=False) if data else None

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    cvs = db.relationship('CV', backref='owner', lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class CV(db.Model, AnalysisMixin):
    __tablename__ = 'cvs'
    
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Analysis Data
    analysis_data = db.Column(JSON, nullable=True)  # Ham analiz verileri
    
    # Scoring
    overall_score = db.Column(db.Float, nullable=True)  # Genel puan (0-100)
    section_scores = db.Column(JSON, nullable=True)  # Bölümlere göre puanlar
    
    # Status
    status = db.Column(db.String(20), default='pending', 
                      nullable=False)  # pending, processing, completed, failed
    
    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.original_filename,
            'upload_date': self.upload_date.isoformat(),
            'score': self.overall_score,
            'status': self.status,
            'analysis': self.get_analysis()
        }
    
    def get_analysis_dict(self):
        """Parse analysis_result JSON string to dict"""
        if self.analysis_result:
            return json.loads(self.analysis_result)
        return {}
        
    def set_analysis_result(self, data):
        """Convert dict to JSON string for storage"""
        if isinstance(data, dict):
            self.analysis_result = json.dumps(data, ensure_ascii=False)
        else:
            self.analysis_result = data
