from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FileField, BooleanField, SubmitField, TextAreaField, FloatField,DateField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional, InputRequired, NumberRange

class ProfessionalForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    service_name = SelectField(
        'Service Name', 
        choices=[
            ('Cleaning', 'Cleaning'),
            ('Mechanic', 'Mechanic'),
            ('Saloon', 'Saloon'),
            ('Plumbing', 'Plumbing'),
            ('Electrician', 'Electrician'),
            ('Carpentry', 'Carpentry'),
            ('Painting', 'Painting'),
            ('Gardening', 'Gardening')
        ], 
        validators=[DataRequired()]
    )
    experience = IntegerField('Experience (Years)', validators=[DataRequired()])
    document = FileField('Upload Document (PDF)', validators=[Optional()])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=10)])
    is_active = BooleanField('Is Active', default=True)
    submit = SubmitField('Register')

class UpdateProfessionalForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_no = StringField('Phone Number', validators=[DataRequired(), Length(max=10)])
    service_name = SelectField(
        'Service Name', 
        choices=[
            ('Cleaning', 'Cleaning'),
            ('Mechanic', 'Mechanic'),
            ('Saloon', 'Saloon'),
            ('Plumbing', 'Plumbing'),
            ('Electrician', 'Electrician'),
            ('Carpentry', 'Carpentry'),
            ('Painting', 'Painting'),
            ('Gardening', 'Gardening')
        ], 
        validators=[DataRequired()]
    )
    experience = IntegerField('Experience (Years)', validators=[DataRequired()])
    document = FileField('Upload Document (PDF)', validators=[Optional()])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=10)])
    is_active = BooleanField('Is Active', default=True)
    verified = BooleanField("Verified")
    rating = DecimalField("Rating", places=1, validators=[Optional()])
    submit = SubmitField('Update')

class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Register')

class UpdateCustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Update')

class LoginFrom(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')

class ServiceForm(FlaskForm):
    name = StringField('Service Name',
    validators=[DataRequired(),Length(max=100)])
    price = FloatField('Price (₹)',validators=[DataRequired(),NumberRange(min=0)])
    description = TextAreaField('Description',validators=[DataRequired(),Length(max=500)])
    time_required = StringField('Time Required (Hour)',validators=[DataRequired(),Length(max=50)])
    category = SelectField('Category', 
                           choices=[('AC Repair', 'AC Repair'),
                                    ('Mechanic', 'Mechanic'),
                                    ('Saloon', 'Saloon'),
                                    ('Plumbing', 'Plumbing'),
                                    ('Electrician', 'Electrician'),
                                    ('Painting', 'Painting'),
                                    ('Gardening', 'Gardening'),
                                    ('Makeup Artist', 'Makeup Artist')],
                           validators=[DataRequired()])
    submit = SubmitField('Add')

class ServiceRequestForm(FlaskForm):
    preferred_date = DateField("Preferred Date", format='%Y-%m-%d', validators=[DataRequired()])
    preferred_time = SelectField("Preferred Time 9AM to 6PM", choices=[('Morning', 'Morning'),
                                    ('Afternoon', 'Afternoon'),
                                    ('Evening', 'Evening')], validators=[DataRequired()])
    additional_notes = TextAreaField("Additional Notes", render_kw={"rows": 3})
    address = TextAreaField("Service Address", validators=[DataRequired()], render_kw={"rows": 3})
    submit = SubmitField("Place Request")

class UpdateRequestForm(FlaskForm):
    professional_id = SelectField('Assign Professional', coerce=str, validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Request')

class RatingForm(FlaskForm):
    rating = FloatField("Rate the Professional (1-5)", validators=[
        DataRequired(), 
        NumberRange(min=1.0, max=5.0, message="Rating must be between 1 and 5")
    ])
    submit = SubmitField("Submit Rating")