from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import google.generativeai as genai
from config import config

# Load environment variables
load_dotenv()

# Configure Google's Generative AI
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables")

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Initialize CSRF protection
csrf = CSRFProtect()

# Configure CSRF to work with file uploads
def init_csrf(app):
    csrf.init_app(app)
    # Disable CSRF for development
    app.config['WTF_CSRF_ENABLED'] = False

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    # Create and configure the app
    app = Flask(__name__)
    
    # Apply configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure CSRF
    init_csrf(app)
    
    # Initialize database migrations
    Migrate(app, db)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from .views import views as main_blueprint
    from .auth import auth as auth_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize Celery
    from .tasks import init_celery
    app.celery = init_celery(app)
    
    # Import tasks to register them with Celery
    from . import tasks  # noqa
    
    return app
