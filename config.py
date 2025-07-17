import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cv_analyzer.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Data Science API
    DATA_SCIENCE_API_URL = os.getenv('DATA_SCIENCE_API_URL', 'http://localhost:5001/api')
    
    # Celery (for background tasks) - Using SQLite for development
    CELERY_BROKER_URL = 'sqla+sqlite:///celery.db'
    CELERY_RESULT_BACKEND = 'db+sqlite:///celery_results.db'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
