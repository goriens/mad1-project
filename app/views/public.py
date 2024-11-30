from flask import Blueprint, render_template, flash, redirect, url_for
public=Blueprint("public", __name__)
from ..models import ServiceModel, CustomerRequestModel
from ..forms import ServiceRequestForm
from flask_login import current_user, login_required
from .. import db

@public.route("")
def home():
    categories = [
        {"name": "AC Repair", "icon": "images/icons/air-conditioner.png"},
        {"name": "Mechanic", "icon": "images/icons/mechanic.png"},
        {"name": "Saloon", "icon": "images/icons/beauty-saloon.png"},
        {"name": "Plumbing", "icon": "images/icons/plumbing.png"},
        {"name": "Electrician", "icon": "images/icons/electrician.png"},
        {"name": "Painting", "icon": "images/icons/exhibition.png"},
        {"name": "Gardening", "icon": "images/icons/gardening.png"},
        {"name": "Makeup Artist", "icon": "images/icons/cosmetics.png"},
    ]
    return render_template("index.html", categories=categories)

@public.route("<category>")
def services_by_category(category):
    services = ServiceModel.query.filter_by(category=category).all()
    return render_template("public/services_by_category.html", category=category, services=services)

@public.route("<category>/<service_id>", methods=["GET", "POST"])
@login_required
def service_request(category,service_id):
    service=ServiceModel.query.get_or_404(service_id)
    form=ServiceRequestForm()
    if(form.validate_on_submit()):
        new_request = CustomerRequestModel(
            customer_id=current_user.id,
            service_id=service.id,
            preferred_date=form.preferred_date.data,
            preferred_time=form.preferred_time.data,
            additional_notes=form.additional_notes.data,
            address=form.address.data,
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Your request has been placed successfully!", "success")
        return redirect(url_for("public.home"))
    return render_template("public/service_request.html",form=form, category=category, service_id=service_id)