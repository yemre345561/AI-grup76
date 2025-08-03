import re
import os
from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from .models import CV, User
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import requests
from sqlalchemy.exc import SQLAlchemyError
from app.model_logic import analyze_cv  


# Configuration
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Helper Functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if not file or not allowed_file(file.filename):
        return None
    
    # Create uploads directory if not exists
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_folder, filename)
    
    # Save file
    file.save(filepath)
    return filename

views = Blueprint('views', __name__)

# Web Routes
@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('home.html')

@views.route('/my_cvs')
@login_required
def my_cvs():
    cvs = CV.query.filter_by(user_id=current_user.id).order_by(CV.upload_date.desc()).all()
    return render_template('my_cvs.html', cvs=cvs)

@views.route('/cv/<int:cv_id>')
@login_required
def cv_results(cv_id):
    cv = CV.query.filter_by(id=cv_id, user_id=current_user.id).first_or_404()

    analysis_data = cv.get_analysis()  

    return render_template('cv_results.html', cv=cv, analysis=analysis_data)



@views.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    from flask import jsonify
    try:
        user = current_user
        user_id = user.id
        
        # 1. Delete user's CV files
        try:
            user_cvs = CV.query.filter_by(user_id=user_id).all()
            for cv in user_cvs:
                if cv.stored_filename:
                    file_path = os.path.join(current_app.root_path, 'static/uploads', cv.stored_filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
        except Exception as e:
            print(f"CV dosyaları silinirken hata: {e}")
        
        # 2. Delete user's CV records
        CV.query.filter_by(user_id=user_id).delete()
        
        # 3. Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # 4. Log out the user
        logout_user()
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Hesabınız başarıyla silindi.'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Hesap silme hatası: {e}")
        return jsonify({
            'success': False,
            'message': 'Hesap silinirken bir hata oluştu: ' + str(e)
        }), 500

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        new_email = request.form.get('email', '').strip().lower()
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Update first name if changed
        if first_name and first_name != user.first_name:
            user.first_name = first_name
            flash('Ad bilgileriniz güncellendi.', 'success')
        
        # Update last name if changed
        if last_name != user.last_name:
            user.last_name = last_name if last_name else None
            if last_name:
                flash('Soyad bilgileriniz güncellendi.', 'success')
        
        # Update email if changed
        if new_email and new_email != user.email:
            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_email):
                flash('Geçersiz e-posta adresi formatı!', 'danger')
            else:
                # Check if email already exists
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user.id:
                    flash('Bu e-posta adresi zaten kullanılıyor!', 'danger')
                else:
                    user.email = new_email
                    flash('E-posta adresiniz güncellendi.', 'success')
        
        # Update password if all fields are provided
        password_updated = False
        if current_password or new_password or confirm_password:
            if not all([current_password, new_password, confirm_password]):
                flash('Şifre güncellemek için tüm alanları doldurmalısınız!', 'danger')
            elif not check_password_hash(user.password, current_password):
                flash('Mevcut şifreniz yanlış!', 'danger')
            elif new_password != confirm_password:
                flash('Yeni şifreler eşleşmiyor!', 'danger')
            elif len(new_password) < 6:
                flash('Şifre en az 6 karakter olmalıdır!', 'danger')
            else:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                password_updated = True
                flash('Şifreniz başarıyla güncellendi.', 'success')
        
        try:
            # Save changes to database
            db.session.commit()
            
            # If password was updated, log the user out for security
            if password_updated:
                logout_user()
                flash('Güvenlik nedeniyle lütfen yeni şifrenizle tekrar giriş yapın.', 'info')
                return redirect(url_for('auth.login'))
                
            return redirect(url_for('views.profile'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error updating profile: {str(e)}')
            flash('Profil güncellenirken bir hata oluştu. Lütfen tekrar deneyiniz.', 'danger')
    
    # For GET requests or if there was an error in POST
    return render_template('profile.html', user=user)

# Simple test upload route
@views.route('/test_upload', methods=['GET', 'POST'])
def test_upload():
    if request.method == 'POST':
        print("Test upload endpoint hit")  # Debug
        print("Files:", request.files)  # Debug
        
        if 'file' not in request.files:
            print("No file part")  # Debug
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            print("No selected file")  # Debug
            return jsonify({'error': 'No selected file'}), 400
            
        try:
            # Create uploads directory if it doesn't exist
            upload_folder = os.path.join(current_app.static_folder, 'test_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            print(f"File saved to: {filepath}")  # Debug
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully!',
                'filename': filename
            })
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return jsonify({'error': str(e)}), 500
    
    return """
    <!doctype html>
    <title>Test File Upload</title>
    <h1>Test File Upload</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <div id="result"></div>
    <script>
    document.querySelector('form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/test_upload', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            document.getElementById('result').textContent = JSON.stringify(result, null, 2);
        } catch (error) {
            document.getElementById('result').textContent = 'Error: ' + error.message;
        }
    });
    </script>
    """

from flask import current_app, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import CV, db
from werkzeug.utils import secure_filename
import os

@views.route('/upload_cv', methods=['GET', 'POST'])
@login_required
def upload_cv():
    if request.method == 'POST':
        print("Dosya yükleme isteği alındı")  # Debug
        
        if 'file' not in request.files:
            print("Dosya bulunamadı")  # Debug
            flash('Lütfen bir dosya seçin', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            print("Dosya adı boş")  # Debug
            flash('Lütfen geçerli bir dosya seçin', 'danger')
            return redirect(request.url)
        
        ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if '.' not in file.filename or file_ext not in ALLOWED_EXTENSIONS:
            print(f"Geçersiz dosya uzantısı: {file.filename}")  # Debug
            flash('Sadece PDF, DOC veya DOCX dosyaları yükleyebilirsiniz.', 'danger')
            return redirect(request.url)
        
        try:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            print(f"Upload klasörü: {upload_folder}")  # Debug

            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(upload_folder, filename)):
                filename = f"{base}_{counter}{ext}"
                counter += 1
                
            filepath = os.path.join(upload_folder, filename)
            print(f"Dosya kaydediliyor: {filepath}")  # Debug
            
            file.save(filepath)
            print("Dosya başarıyla kaydedildi")  # Debug

            # CV kaydını oluştur
            cv = CV(
                original_filename=file.filename,
                stored_filename=filename,
                user_id=current_user.id,
                status='pending',
                created_at=datetime.utcnow()
            )
            db.session.add(cv)
            db.session.commit()
            print(f"CV kaydı oluşturuldu: {cv.id}")  # Debug

            # AI analizini yap
            try:
                from .model_logic import analyze_cv, extract_text_from_pdf
                import json

                # PDF'ten metni oku
                cv_text = extract_text_from_pdf(filepath)

                if cv_text.strip():
                    result = analyze_cv(cv_text)

                    score = result.get("score")
                    if score is None:
                        raise ValueError("Analiz sonucu geçersiz: score değeri yok")

                    print(" Analiz sonucu:", result)
                    print(" Toplam skor:", score)

                    cv.analysis_data = json.dumps(result)
                    cv.overall_score = score  
                    cv.status = 'completed'
                    cv.analysis_date = datetime.utcnow()
                    db.session.commit()
                    print("Analiz tamamlandı ve veritabanına kaydedildi.")
                else:
                    raise ValueError("CV metni boş")

            except Exception as e:
                print(f"Analiz hatası: {str(e)}")
                cv.status = 'error'
                cv.error_message = str(e)
                db.session.commit()

            flash('CV başarıyla yüklendi!', 'success')
            return redirect(url_for('views.my_cvs'))
        
        except Exception as e:
            print(f"Beklenmeyen hata: {str(e)}")  # Debug
            db.session.rollback()
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
            return redirect(request.url)

    
    return render_template('upload_cv.html')




# Helper function to read CV file content
def read_cv_file(file_path):
    """
    Read content from CV file (PDF or DOCX)
    """
    import PyPDF2
    import docx
    
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
                
        elif ext in ['.docx', '.doc']:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
        else:
            return ""
            
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return ""



# analyze_cv_with_ai fonksiyonu
def analyze_cv_with_ai(cv_text):
    if not cv_text.strip():
        return {}

    analysis = analyze_cv(cv_text)

    
    analysis["full_text"] = "\n".join(analysis.get("strengths", [])) + "\n" + "\n".join(analysis.get("weaknesses", []))

    return analysis




@views.route('/api/analyze/<int:cv_id>', methods=['POST'])
def analyze_cv_api(cv_id):
    cv = CV.query.get_or_404(cv_id)

    if cv.status == 'completed':
        feedback = generate_feedback(cv)
        print("FEEDBACK (already completed):", feedback)  
        return jsonify({
            'status': 'already_completed',
            'analysis': feedback
        })

    try:
        # CV işleniyor...
        file_path = os.path.join(current_app.static_folder, 'uploads', cv.stored_filename)
        cv_text = read_cv_file(file_path)
        analysis = analyze_cv_with_ai(cv_text)

        # Veritabanına kaydet
        cv.analysis_data = analysis
        cv.overall_score = analysis.get("score", 0)
        cv.status = 'completed'
        cv.updated_at = datetime.utcnow()
        db.session.commit()

        # Feedback üretimi ve loglanması
        feedback = generate_feedback(cv)
        print("FEEDBACK (fresh):", feedback)  

        return jsonify({
            'status': 'completed',
            'analysis': feedback
        })

    except Exception as e:
        cv.status = 'error'
        db.session.commit()
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500



def generate_feedback(cv):
    import json
    from flask import current_app
    import os

    print(" generate_feedback çağrıldı")
    print("cv.analysis_data:", cv.analysis_data)

    if not cv.analysis_data:
        print(" cv.analysis_data None veya boş!")
        return {
            'score': 0,
            'status': cv.status,
            'sections': {},
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }

    try:
        analysis = json.loads(cv.analysis_data) if isinstance(cv.analysis_data, str) else cv.analysis_data
        if analysis is None:
            raise ValueError("analysis None geldi!")
    except Exception as e:
        print(" JSON parse hatası:", e)
        return {
            'score': 0,
            'status': cv.status,
            'sections': {},
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }

    # CV dosyasını oku
    file_path = os.path.join(current_app.static_folder, 'uploads', cv.stored_filename)
    cv_text = read_cv_file(file_path)

    # Artık analysis üzerinden öneri üret
    recommendations_raw = []  
    print(" Raw Öneriler:", recommendations_raw)

    feedback = {
        'score': analysis.get('score', 0),
        'status': cv.status,
        'sections': {},
        'strengths': analysis.get('strengths', []),
        'weaknesses': analysis.get('weaknesses', []),
        'recommendations': recommendations_raw
    }

    print(" FEEDBACK üretildi:", feedback)
    return feedback





def get_section_feedback(section, score, analysis):
    """Generate feedback for a specific section"""
    # This is a simplified example - you'd want to expand this
    if score >= 80:
        return f"Great work on your {section} section!"
    elif score >= 50:
        return f"Your {section} section is good but could be improved."
    else:
        return f"Consider improving your {section} section."

def generate_recommendations(analysis):
    """Generate actionable recommendations"""
    recommendations = []
    
    # Example recommendations
    if analysis.get('skills', {}).get('Python', 0) < 3:
        recommendations.append({
            'priority': 'high',
            'message': 'Improve your Python skills',
            'resources': ['Python for Data Science course', 'Practice on LeetCode']
        })
    
    if not analysis.get('has_projects', False):
        recommendations.append({
            'priority': 'medium',
            'message': 'Add personal projects to showcase your skills',
            'resources': ['GitHub repository', 'Personal portfolio website']
        })
    
    return recommendations

    return jsonify({
        'status': 'error',
        'message': str(e)
    }), 500

# CV silme endpoint'i
@views.route('/delete-cv/<int:cv_id>', methods=['POST'])
@login_required
def delete_cv(cv_id):
    cv = CV.query.get_or_404(cv_id)
    
    # Sadece CV sahibi silebilir
    if cv.user_id != current_user.id:
        flash('Bu işlemi yapmaya yetkiniz yok!', 'error')
        return redirect(url_for('views.my_cvs'))
    
    try:
        # Dosyayı sil
        file_path = os.path.join('app', 'static', 'uploads', cv.stored_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Veritabanından sil
        db.session.delete(cv)
        db.session.commit()
        
        flash('CV başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('CV silinirken bir hata oluştu.', 'error')
    
    return redirect(url_for('views.my_cvs'))
