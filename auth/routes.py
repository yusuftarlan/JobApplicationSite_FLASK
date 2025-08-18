import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, request
from forms import *
from db import get_user_info, generate_hash, new_user_create, login_user

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret = current_app.config.get('RECAPTCHA_SECRET_KEY')

        if not recaptcha_response:
            flash("reCAPTCHA doğrulamasını tamamlayın.", "danger")
            return render_template('login.html', form=form)

        # Google reCAPTCHA doğrulaması
        payload = {
            'secret': secret,
            'response': recaptcha_response
        }

        try:
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=payload)
            result = r.json()
        except Exception as e:
            flash("reCAPTCHA doğrulaması sırasında bir hata oluştu.", "danger")
            return render_template('login.html', form=form)

        if not result.get('success'):
            flash("reCAPTCHA doğrulaması başarısız.", "danger")
            return render_template('login.html', form=form)

        # Kullanıcı giriş doğrulaması
        username = form.username.data
        password = form.password.data
        # varsayalım login_user bu üçlü döndürüyor
        success, role, user_id = login_user(username, password)

        if success:
            if role == 1:
                return redirect(url_for('admin.admin_panel', user_id=user_id))
            else:
                return redirect(url_for('user.user', user_id=user_id))
        else:
            flash("Kullanıcı adı veya şifre yanlış.", "danger")
            return redirect(url_for("auth.login"))

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        is_username_taken = get_user_info(username)
        if is_username_taken != None:
            flash("Kullanıcı adı alınmış!", "danger")
            return render_template("register.html", form=form)

        elif form.password.data != form.confirm_password.data:
            flash("Şifreler uyuşmuyor!", "danger")
            return render_template("register.html", form=form)
           
        else:
            name = form.name.data
            surname = form.surname.data
            email = form.email.data
            sifre = form.password.data
            hash = generate_hash(sifre)
            try:
                new_user_create(name, surname, username, email, hash)
                flash("Kullanıcı oluşturuldu", "success")
                return redirect(url_for("auth.login", form=form))
            except:
                flash("Kullanıcı oluştururken hata !", "danger")
                return redirect(url_for("auth.login", form=form))
    return render_template('register.html', form=form)
