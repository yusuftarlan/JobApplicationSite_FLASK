from flask import Flask, render_template, flash, redirect, url_for
from flasgger import Swagger
from auth.routes import auth_bp 
from admin.routes import admin_bp
from user.routers import user_bp

app = Flask(__name__)
swagger = Swagger(app)

app.secret_key = 'kf6E_q.346'
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

app.config['RECAPTCHA_SITE_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

@app.route("/")
def root():
    return redirect("/login")

if __name__ == "__main__":
    app.run(host ='0.0.0.0', debug=True)



