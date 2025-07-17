from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Başarıyla giriş yapıldı!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Hatalı şifre, tekrar deneyin.', category='error')
        else:
            flash('Bu email adresiyle kayıtlı kullanıcı bulunamadı.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Bu email adresi zaten kullanımda.', category='error')
        elif len(email) < 4:
            flash('Email en az 4 karakter olmalıdır.', category='error')
        elif len(first_name) < 2:
            flash('İsim en az 2 karakter olmalıdır.', category='error')
        elif password1 != password2:
            flash('Şifreler eşleşmiyor.', category='error')
        elif len(password1) < 7:
            flash('Şifre en az 7 karakter olmalıdır.', category='error')
        else:
            new_user = User(
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Hesap oluşturuldu!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
