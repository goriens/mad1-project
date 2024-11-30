from flask import Blueprint, render_template, flash, redirect, url_for, request
professional=Blueprint("professional", __name__)
from flask_login import current_user, login_required
from ..forms import UpdateProfessionalForm
from ..models import ProfessionalModel, CustomerRequestModel
from .. import db
import matplotlib.pyplot as plt
import io
import base64

@professional.route("profile", methods=["GET", "POST"])
@login_required
def profile():
    user = ProfessionalModel.query.get_or_404(current_user.id)
    form = UpdateProfessionalForm(obj=user)
    if request.method == "POST" and form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.phone_no = form.phone_no.data
        user.service_name = form.service_name.data
        user.experience = form.experience.data
        user.address = form.address.data
        user.pin_code = form.pin_code.data
        user.is_active = form.is_active.data

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("professional.profile"))
    return render_template("professional/profile.html",form=form, user=user)

@professional.route("work", methods=["GET", "POST"])
@login_required
def assign_work():
    assigned_requests = CustomerRequestModel.query.filter_by(professional_id=current_user.id).all()
    if request.method == "POST":
        request_id = request.form.get("request_id")
        action = request.form.get("action")
        service_request = CustomerRequestModel.query.get_or_404(request_id)
        
        if service_request.professional_id != current_user.id:
            flash("Unauthorized action!", "danger")
            return redirect(url_for("professional.assign_work"))
        if action == "complete":
            service_request.status = "Completed"
            flash("Work marked as completed!", "success")
        elif action == "cancel":
            service_request.status = "Canceled"
            flash("Work marked as canceled!", "danger")
        db.session.commit()
        return redirect(url_for("professional.assign_work"))
    return render_template("professional/assign_work.html", assigned_requests=assigned_requests)

@professional.route('/summary', methods=['GET'])
@login_required
def summary():
    professional = ProfessionalModel.query.get(current_user.id)
    rating_percentage = (professional.rating / 5) * 100 if professional.rating else 0
    statuses = ['Completed', 'Cancelled', 'Pending']
    work_counts = {
        'Completed': CustomerRequestModel.query.filter_by(professional_id=professional.id, status='Completed').count(),
        'Cancelled': CustomerRequestModel.query.filter_by(professional_id=professional.id, status='Canceled').count(),
        'Pending': CustomerRequestModel.query.filter_by(professional_id=professional.id, status='Pending').count(),
    }
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].bar(work_counts.keys(), work_counts.values(), color=['#4CAF50', '#F44336', '#FFEB3B'])
    ax[0].set_title('Work Status for Professional')
    ax[0].set_xlabel('Status')
    ax[0].set_ylabel('Count')

    rating_data = [rating_percentage, 100 - rating_percentage]
    rating_labels = [f'{rating_percentage:.1f}% Rated', 'Remaining']
    ax[1].pie(rating_data, labels=rating_labels, autopct='%1.1f%%', colors=['#4CAF50', '#ddd'], startangle=90)
    ax[1].axis('equal')
    ax[1].set_title('Professional Rating')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template("professional/summary.html", img_data=img_base64)