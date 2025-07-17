from app import create_app, db
from app.models import User, CV
import os

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'CV': CV}

if __name__ == '__main__':
    # Gerekli klasörleri oluştur
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    
    # Veritabanını oluştur
    with app.app_context():
        db.create_all()
    
    # Uygulamayı başlat
    app.run(debug=True, host='0.0.0.0', port=5000)
