from flask import Blueprint, render_template, request, Response, redirect, url_for, flash
from db import get_all_user_info, new_position_create, set_position_passive
from db import get_all_position_info, get_position_info, get_applications_for_position, get_cvdata, set_app_status


admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/admin_panel/<int:user_id>', methods=["GET", "POST"])
def admin_panel(user_id):
    users = get_all_user_info()
    positions = get_all_position_info()

    if request.method == 'POST':
        if 'btn_sil' in request.form:
            selected_id = request.form.get('btn_sil')
            set_position_passive(selected_id)
            flash("Pozisyon silindi.", "danger")
            return redirect(url_for('admin.admin_panel', user_id=user_id))
        
    return render_template('admin_panel.html', user_id=user_id, users=users, positions=positions)


# Yeni pozisyon ekleme sayfası
@admin_bp.route('/admin_panel/<int:user_id>/new_position', methods=["GET", "POST"])
def new_position(user_id):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        location = request.form.get("location")
        department = request.form.get("department")
        deadline = request.form.get("deadline")
        try:
            new_position_create(user_id, title, description,
                                department, location, deadline)
            flash("Yeni pozisyon açıldı.", "success")
            return redirect(url_for('admin.admin_panel', user_id=user_id))
        except:
            flash("Yeni pozisyon açılamadı.", "danger")
            return redirect(url_for('admin.admin_panel', user_id=user_id))
    return render_template('new_position.html', user_id=user_id)

# İlana gelen başvuruları görme ve karar verme


@admin_bp.route('/admin_panel/<int:user_id>/applications/<int:position_id>', methods=["GET", "POST"])
def applications(user_id, position_id):
    position_info = get_position_info(position_id)
    applications_info = get_applications_for_position(position_id)
    action = request.form.get('action')
    if request.method == 'POST':
        app_id = int(request.form.get('app_id'))

        if action == 'accept':
            # Başvuruyu kabul et
            print("accept çalıştı")
            set_app_status(app_id, 2)

        elif action == 'reject':
            # Başvuruyu reddet
            print("reject çalıştı")
            set_app_status(app_id, 3)
        return redirect(url_for('admin.applications', user_id=user_id, position_id=position_id))
    return render_template('applications.html', user_id=user_id, position=position_info, applications=applications_info)


@admin_bp.route('/admin_panel/get_cv/<int:app_id>', methods=["GET", "POST"])
def get_cv(app_id):
    data = get_cvdata(app_id)
    return Response(data['cv_data'], mimetype="application/pdf", headers={"Content-Disposition": "inline; filename=cv.pdf"})
