from flask import Blueprint, render_template, flash, redirect, url_for, request
admin=Blueprint("admin", __name__)
from ..models import AdminModel, UserRole
from werkzeug.security import generate_password_hash
from .. import db
from ..forms import ServiceForm, UpdateRequestForm
from ..models import ServiceModel, CustomerRequestModel, ProfessionalModel
from ..decorators import admin_only
from flask_login import current_user
from matplotlib import pyplot as plt
import io
import base64

@admin.route("create-admin")
def create_admin():
    exist_admin=AdminModel.query.filter_by(email="admin@iitm.com").first()
    if(exist_admin):
        return "Admin already exist admin@iitm.com"
    else:
        admin = AdminModel(
        first_name="Admin",
        last_name="User",
        email="admin@iitm.com",
        password=generate_password_hash("12345678"),
        role=UserRole.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        return ("Admin user created successfully!")

@admin.route("dashboard")
@admin_only
def dashboard():
    all_professionals = ProfessionalModel.query.all()
    total_rating = sum(prof.rating for prof in all_professionals if prof.rating)
    total_professionals = len([prof for prof in all_professionals if prof.rating])
    average_rating = total_rating / total_professionals if total_professionals > 0 else 0
    statuses = ['Completed', 'Canceled', 'Pending', 'Accepted']
    request_counts = {
        status: CustomerRequestModel.query.filter_by(status=status).count() for status in statuses
    }
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].bar(request_counts.keys(), request_counts.values(), color=['#4CAF50', '#F44336', '#FFEB3B', '#2196F3'])
    axs[0].set_title('Requests by Status')
    axs[0].set_xlabel('Status')
    axs[0].set_ylabel('Count')

    rating_data = [average_rating, 5 - average_rating]
    axs[1].pie(
        rating_data,
        labels=[f'Avg Rating: {average_rating:.1f}', 'Remaining'],
        autopct=lambda p: '' if p > 0 else '',
        colors=['#4CAF50', '#ddd'],
        startangle=90
    )
    axs[1].axis('equal') 
    axs[1].set_title('Overall Rating')

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
    img.close()
    return render_template("admin/dashboard.html", graph_url=graph_url)

@admin.route("services",  methods=['GET', 'POST'])
@admin_only
def services():
    form = ServiceForm()
    all_services = ServiceModel.query.all()
    if(form.validate_on_submit()):
        new_service=ServiceModel(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            time_required=form.time_required.data,
            category=form.category.data
        )
        db.session.add(new_service)
        db.session.commit()
        flash("Service added successfully", "success")
        return redirect(url_for('admin.services'))
    return render_template("admin/services.html", form=form, services=all_services)

@admin.route("services/delete/<int:service_id>", methods=["POST", "DELETE"])
@admin_only
def delete_service(service_id):
    service = ServiceModel.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully", "danger")
    return redirect(url_for('admin.services'))

@admin.route("/services/update/<int:service_id>", methods=["GET", "POST"])
@admin_only
def update_service(service_id):
    service = ServiceModel.query.get_or_404(service_id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.price = form.price.data
        service.description = form.description.data
        service.time_required = form.time_required.data
        service.category=form.category.data
        db.session.commit()
        flash("Service updated successfully", "success")
        return redirect(url_for('admin.services'))
    return render_template("admin/update-service.html", form=form, service=service)

@admin.route("/services/<int:service_id>", methods=["GET"])
@admin_only
def view_service(service_id):
    service = ServiceModel.query.get_or_404(service_id)
    return render_template("admin/view-service.html", service=service)

@admin.route("orders", methods=["GET"])
@admin_only
def orders():
    requests = CustomerRequestModel.query.all()
    return render_template("admin/orders.html", requests=requests)

@admin.route('orders/<request_id>/update', methods=['GET', 'POST'])
@admin_only
def update_request(request_id):
    current_request = CustomerRequestModel.query.get_or_404(request_id)
    service_category = current_request.service.category
    form = UpdateRequestForm()
    form.professional_id.choices = [
        (str(pro.id), f"{pro.first_name} {pro.last_name} - {pro.service_name}")
        for pro in ProfessionalModel.query.filter_by(service_name=service_category).all()
    ]
    if form.validate_on_submit():
        professional_id = form.professional_id.data
        status = form.status.data
        current_request.professional_id = professional_id
        current_request.status = status
        db.session.commit()
        flash("Request updated successfully!", "success")
        return redirect(url_for("admin.orders"))
    return render_template('admin/update_request.html', current_request=current_request, form=form)

@admin.route('orders/<request_id>/delete', methods=['POST'])
@admin_only
def delete_request(request_id):
    exit_request = CustomerRequestModel.query.get_or_404(request_id)
    db.session.delete(exit_request)
    db.session.commit()
    flash("Request deleted successfully", "success")
    return redirect(url_for('admin.orders'))


@admin.route('professionals')
@admin_only
def professionals():
    professionals = ProfessionalModel.query.all()
    return render_template('admin/professionals.html',professionals=professionals)


@admin.route('/verify_professional/<string:professional_id>', methods=['POST'])
@admin_only
def verify_professional(professional_id):
    professional = ProfessionalModel.query.get(professional_id)
    if not professional:
        flash("Professional not found", "danger")
        return redirect(url_for('admin.professionals'))

    professional.verified = True 
    db.session.commit()
    flash(f"{professional.first_name} {professional.last_name} has been verified.", "success")
    return redirect(url_for('admin.professionals'))