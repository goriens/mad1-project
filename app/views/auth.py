from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..forms import ProfessionalForm, LoginFrom, CustomerForm
from ..models import ProfessionalModel, UserRole, CustomerModel, AdminModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .. import db
import os
from werkzeug.utils import secure_filename
from flask import current_app

auth=Blueprint("auth", __name__)

@auth.route("choose-register")
def choose_register():
    return render_template("registration_choose.html")

@auth.route("professional/register", methods=["GET", "POST"])
def professional_register():
    form=ProfessionalForm()
    if(form.validate_on_submit()):
        exist_email=ProfessionalModel.query.filter_by(email=form.email.data).first()
        if(exist_email):
            flash("Email Already Exist", "danger")
            return render_template("professional/register.html", form=form)
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/documents')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        document_path = None
        filename = None
        if(form.document.data):
            filename = secure_filename(form.document.data.filename)
            document_path = os.path.join(upload_folder, filename)
            form.document.data.save(document_path)

        new_professional=ProfessionalModel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            email=form.email.data,
            phone_no=form.phone_no.data,
            password=generate_password_hash(form.password.data),
            service_name=form.service_name.data,
            experience=form.experience.data,
            document=filename,
            address=form.address.data,
            pin_code=form.pin_code.data,
            is_active=form.is_active.data,
            role=UserRole.PROFESSIONAL
        )
        db.session.add(new_professional)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("auth.login"))
    return render_template("professional/register.html", form=form)

@auth.route("customer/register", methods=["GET", "POST"])
def customer_register():
    form=CustomerForm()
    if(form.validate_on_submit()):
        exist_email=CustomerModel.query.filter_by(email=form.email.data).first()
        if(exist_email):
            flash("Email Already Exist", "danger")
            return render_template("customer/register.html", form=form)
        new_customer= CustomerModel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            address=form.address.data,
            pin_code=form.pin_code.data,
            role=UserRole.CUSTOMER
        )
        db.session.add(new_customer)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("public.home"))
    return render_template("customer/register.html", form=form) 

@auth.route("login", methods=["GET", "POST"])
def login():
    form=LoginFrom()
    if(form.validate_on_submit()):
        email=form.email.data
        password=form.password.data
        user=AdminModel.query.filter_by(email=email).first() or ProfessionalModel.query.filter_by(email=email).first() or CustomerModel.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            print("us", user.role, user.email)
            login_user(user)
            flash("Logged in Successfully", "success")
            if(user.role==UserRole.ADMIN):
                return redirect(url_for("admin.dashboard"))
            elif(user.role==UserRole.PROFESSIONAL):
                return redirect(url_for("professional.assign_work"))
            elif user.role==UserRole.CUSTOMER:
                return redirect(url_for("public.home"))
        else:
            flash("Invalid Email or Password", "danger")
    return render_template("login.html", form=form)

@auth.route("logout")
def logout():
    logout_user()
    flash("Logout out successfully!", "success")
    return redirect(url_for("auth.login"))