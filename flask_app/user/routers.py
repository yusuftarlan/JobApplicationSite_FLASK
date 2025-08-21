from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from forms import *
from db import get_all_position_info, get_user_info_viaID, get_position_info, create_new_application
from db import get_all_user_application_info, get_position_id, get_cover_letter, get_cvdata

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/user/<int:user_id>', methods=["GET", "POST"])
def user(user_id):
    positions = get_all_position_info()
    user_info = get_user_info_viaID(user_id)
    applications = get_all_user_application_info(user_id)
    applied_positions = []
    for app in applications:
        applied_positions.append(app['position_id'])

    return render_template('user.html', positions=positions, user_id=user_id, user_info=user_info, 
                           applications=applications, applied_positions=applied_positions)


@user_bp.route('/user/<int:user_id>/newapplication/<int:position_id>', methods=["GET", "POST"])
def new_application(user_id, position_id):
    user_info = get_user_info_viaID(user_id)
    position_info = get_position_info(position_id)

    if request.method == "POST":
        cover_letter = request.form.get("cover_letter")
        cv_file = request.files.get("cv_file")
        if cv_file:
            cv_name = cv_file.filename
            cv_data = cv_file.read()
            try:
                create_new_application(
                    user_id, position_id, cv_name, cv_data, cover_letter)
                flash("Başvurunuz başarıyla alındı.", "success")
                return redirect(url_for('user.user', user_id=user_id))
            except Exception as e:
                print("hata: ", e)
    return render_template('new_application.html', user_info=user_info, position=position_info)


@user_bp.route('/user/<int:user_id>/review_application/<int:app_id>', methods=["GET"])
def review_application(user_id, app_id):
    user_info = get_user_info_viaID(user_id)
    position_id = get_position_id(app_id)
    position_info = get_position_info(position_id['position_id'])
    cover_letter = get_cover_letter(app_id)
    return render_template('review_application.html', user_info=user_info, position_info=position_info, cover_letter=cover_letter[0])


@user_bp.route('/user/get_cv/<int:app_id>', methods=["GET"])
def get_cv(app_id):
    data = get_cvdata(app_id)
    return Response(data['cv_data'], mimetype="application/pdf", headers={"Content-Disposition": "inline; filename=cv.pdf"})
