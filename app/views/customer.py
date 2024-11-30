from flask import Blueprint, render_template, flash, redirect, url_for, request
customer=Blueprint("customer", __name__)
from flask_login import current_user, login_required
from ..forms import UpdateCustomerForm, RatingForm
from .. import db
from ..models import CustomerRequestModel
import matplotlib.pyplot as plt
import io
import base64

@customer.route("profile", methods=["GET", "POST"])
@login_required
def profile():
    user= current_user
    form = UpdateCustomerForm()
    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.gender.data = user.gender
        form.email.data = user.email
        form.address.data = user.address
        form.pin_code.data = user.pin_code

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.address = form.address.data
        user.pin_code = form.pin_code.data
        db.session.commit() 
        flash("Profile updated successfully", "success")
        return redirect(url_for('customer.profile'))
    return render_template("customer/profile.html",form=form, user=user)

@customer.route("orders")
@login_required
def orders():
    requests = CustomerRequestModel.query.filter_by(customer_id=current_user.id).all()
    print(requests)
    return render_template("customer/orders.html", requests=requests)

@customer.route("orders/<request_id>", methods=["GET", "POST"])
@login_required
def view_order(request_id):
    service_request = CustomerRequestModel.query.filter_by(id=request_id, customer_id=current_user.id).first()
    if request.method == "POST":  
        if service_request.status in ["Pending", "Accepted"]: 
            service_request.status = "Cancelled"
            db.session.commit()
            flash("Request cancelled successfully.", "success")
        else:
            flash("Request cannot be cancelled in the current status.", "warning")
        return redirect(url_for("customer.orders"))
    
    return render_template("customer/view_order.html", service_request=service_request)

@customer.route("/rate/<request_id>", methods=["GET", "POST"])
@login_required
def rate_professional(request_id):
    request = CustomerRequestModel.query.get_or_404(request_id)
    if request.status != "Completed":
        flash("You can only rate completed requests.", "warning")
        return redirect(url_for("customer.orders"))
    form = RatingForm()
    if form.validate_on_submit():
        rating = form.rating.data
        request.rating = rating
        professional = request.professional
        if professional:
            all_ratings = [req.rating for req in professional.requests if req.rating is not None]
            new_average = sum(all_ratings) / len(all_ratings)
            professional.rating = round(new_average, 2)
        db.session.commit()
        flash("Rating submitted successfully!", "success")
        return redirect(url_for("customer.orders"))
    return render_template("customer/rate_professional.html", form=form, request=request)

@customer.route("/summary", methods=["GET"])
@login_required
def summary():
    customer_requests = CustomerRequestModel.query.filter_by(customer_id=current_user.id).all()
    statuses = {'Pending': 0, 'Completed': 0, 'Cancelled': 0}
    for req in customer_requests:
        if req.status == "Pending":
            statuses['Pending'] += 1
        elif req.status == "Completed":
            statuses['Completed'] += 1
        elif req.status == "Cancelled":
            statuses['Cancelled'] += 1

    fig, ax = plt.subplots()
    ax.bar(statuses.keys(), statuses.values(), color=['yellow', 'green', 'red'])

    ax.set_xlabel('Status')
    ax.set_ylabel('Count')
    ax.set_title('Request Status Summary')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return render_template("customer/request_summary.html", img_data=img_base64)

