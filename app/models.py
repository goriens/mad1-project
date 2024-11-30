from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum
import uuid
from sqlalchemy.dialects.sqlite import TEXT 
from datetime import datetime


class UserRole(Enum):
        ADMIN="Admin"
        PROFESSIONAL="Professional"
        CUSTOMER="Customer"

class CategoryEnum(Enum):
    AC_REPAIR = "AC Repair"
    MECHANIC = "Mechanic"
    SALOON = "Saloon"
    PLUMBING = "Plumbing"
    ELECTRICIAN = "Electrician"
    PAINTING = "Painting"
    GARDENING = "Gardening"
    MAKEUP_ARTIST = "Makeup Artist"

class ProfessionalModel(db.Model, UserMixin):
        id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        gender = db.Column(db.String(10), nullable=False)
        email=db.Column(db.String(120), unique=True, nullable=False)
        phone_no = db.Column(db.String(15), nullable=False)
        password = db.Column(db.String(128), nullable=False)
        service_name = db.Column(db.String(100), nullable=False)
        experience = db.Column(db.Integer, nullable=False)
        document = db.Column(db.String(200), nullable=True)
        address = db.Column(db.Text, nullable=False)
        pin_code = db.Column(db.String(10), nullable=False)
        is_active = db.Column(db.Boolean, default=True, nullable=False)
        created_at = db.Column(db.DateTime(timezone=True), default=func.now())
        rating = db.Column(db.Float, default=0.0, nullable=True)
        verified = db.Column(db.Boolean, default=False, nullable=False) 
        role=db.Column(db.Enum(UserRole), default=UserRole.PROFESSIONAL, nullable=False)

class CustomerModel(db.Model, UserMixin):
        id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        gender = db.Column(db.String(10), nullable=False)
        email=db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(128), nullable=False)
        address = db.Column(db.Text, nullable=False)
        pin_code = db.Column(db.String(10), nullable=False)
        created_at = db.Column(db.DateTime(timezone=True), default=func.now())
        role=db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)

class AdminModel(db.Model, UserMixin):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.ADMIN, nullable=False)

class ServiceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_required = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class CustomerRequestModel(db.Model):
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    customer_id = db.Column(db.Text, db.ForeignKey("customer_model.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service_model.id"), nullable=False)
    professional_id = db.Column(db.Text, db.ForeignKey("professional_model.id"), nullable=True) 
    status = db.Column(db.String(20), default="Pending", nullable=False)
    requested_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    preferred_date = db.Column(db.Date, nullable=True)  
    preferred_time = db.Column(db.String(50), nullable=True) 
    additional_notes = db.Column(db.Text, nullable=True)  
    address = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    customer = db.relationship("CustomerModel", backref="requests", lazy=True)
    service = db.relationship("ServiceModel", backref="requests", lazy=True)
    professional = db.relationship("ProfessionalModel", backref="requests", lazy=True) 
