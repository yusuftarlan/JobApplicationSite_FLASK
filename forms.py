from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField,PasswordField,EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email
 
class LoginForm(FlaskForm):
    username = StringField(
        'Kullanıcı Adı',
        validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Şifre',validators=[DataRequired(), Length(min=4)])
    submit_login = SubmitField('Giriş Yap')


class RegisterForm(FlaskForm):
    name = StringField(
        'Ad',
        validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField(
        'Soyadı',
        validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField(
        'Kullanıcı Adı',
        validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField(
        'E-mail Adresi',
        validators=[DataRequired(),  Email(message="Geçerli bir e-posta adresi giriniz."), Length(min=3, max=25)])
    password = PasswordField('Şifre',validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Şifre Tekrar',validators=[DataRequired(), Length(min=4)])
    submit_register = SubmitField('Kayıt Ol')