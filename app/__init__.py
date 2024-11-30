from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_login import current_user



db=SQLAlchemy()
DB_NAME="database.db"
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app=Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    app.config["SECRET_KEY"]="secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"]=f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SESSION_PROTECTION"] = "strong"
    app.config["REMEMBER_COOKIE_SECURE"] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads/documents')
    db.init_app(app)

    
    from .views.auth import auth
    from .views.public import public
    from .views.admin import admin
    from .views.customer import customer
    from .views.professional import professional
    app.register_blueprint(public, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(admin, url_prefix="/admin/")
    app.register_blueprint(customer, url_prefix="/customer/")
    app.register_blueprint(professional, url_prefix="/professional/")

    from .models import ProfessionalModel, CustomerModel, AdminModel
    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = AdminModel.query.get((user_id)) or ProfessionalModel.query.get((user_id)) or CustomerModel.query.get((user_id))
        return user
    
    @app.context_processor
    def inject_helpers():
        return dict(get_profile_url=get_profile_url)

    return app

def create_database(app):
    with app.app_context():
        if not os.path.exists(f'app/{DB_NAME}'):
            db.create_all()
            print("Created Database!")

def get_profile_url():
    from .models import UserRole 
    if current_user.is_authenticated:
        if current_user.role == UserRole.CUSTOMER:
            return url_for('customer.profile')
        elif current_user.role == UserRole.PROFESSIONAL:
            return url_for('professional.profile')
        elif current_user.role == UserRole.ADMIN:
            return url_for('admin.dashboard') 
    return url_for('auth.login')