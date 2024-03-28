# for registration
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from retrievedata import dataframe_to_import


class registrationform(FlaskForm):
    def validate_email_address(self, email_address_to_check):
        user = dataframe_to_import.man_register[dataframe_to_import.man_register['email'] == email_address_to_check]
        if not user.empty:
            raise ValidationError('This user already exists! Please try a different email')

    name = StringField(label='Full Name', validators=[Length(min=4, max=50), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    usertype = SelectField(label='Type Of User',choices=["Type of user", "Customer"], validators=[DataRequired()])
    submit = SubmitField(label='Create Account')


class loginform(FlaskForm):
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Sign in')


class marketform(FlaskForm):
    machine = SelectField(label='Machine', choices=["","Cream Separator"], validators=[DataRequired()])
    capacity = StringField(label='Capacity in litres per hour', validators=[DataRequired()])
    automation = SelectField(label='Automation Grade', choices=["", "Automatic", "Semi-Automatic", "Manual"], validators=[DataRequired()])
    showdata = SubmitField(label='Show Machines')

class fodderform(FlaskForm):
    state = SelectField(label='State', choices=["", "Delhi", "Tamil Nadu", "Gujarat", "Haryana", "Uttar Pradesh", "Punjab", "Rajasthan", "Karnataka", "Maharashtra", "Uttarakhand"], validators=[DataRequired()])
    showdata = SubmitField(label='Show Fodder')
    

class vetsform(FlaskForm):
    state = SelectField(label='State', choices=["", "Delhi", "Tamil Nadu", "Gujarat", "Haryana", "Maharashtra"], validators=[DataRequired()])
    showdata = SubmitField(label='Show Vets')

class trainingform(FlaskForm):
    showdata = SubmitField(label='Show Trainings') 

class workshopform(FlaskForm):
    institute = SelectField(label='Institute', choices=["", "NDDB, Anand", "ERDTC, Siliguri", "NRDTC, Jalandhar", "SRDTC, Erode", "MIT, Mehsana"], validators=[DataRequired()])
    showdata = SubmitField(label='Show Workshops')

class instituteform(FlaskForm):
    institute = SelectField(label='Institute', choices=["","NDRI", "Sheth MC College of Dairy Science_Anand", "Dairy Science college_Bangalore"], validators=[DataRequired()])
    type = SelectField(label='Course Type', choices=["", "UG", "PG", "PHD"], validators=[DataRequired()])
    showdata = SubmitField(label='Show Courses')
    
class ethnoform(FlaskForm):
    disease = SelectField(label='Disease', choices=["", "Expelling retained placenta", "gastroinstestinal issues", "Better digestion", "Diarrhea", "To improve the milk quality" ], validators=[DataRequired()])
    showdata = SubmitField(label='Treatment')
  
class cartform(FlaskForm):
    submit = SubmitField(label='Add to Cart')