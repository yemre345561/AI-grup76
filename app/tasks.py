from celery import Celery
from .models import db, CV
import os

# Create celery instance without the app
celery = Celery(__name__)

@celery.task
def analyze_cv_async(cv_id):
    """Background task to analyze CV"""
    from . import create_app
    from .views import analyze_cv_api
    
    # Create app instance for this task
    app = create_app()
    with app.app_context():
        return analyze_cv_api(cv_id)

def init_celery(app):
    """Initialize celery with Flask app context"""
    # Configure celery
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery
