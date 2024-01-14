from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flaskr.models import User
import re

class RegistrationForm(FlaskForm):
    email = StringField(label='Email',
                        id='field_email',
                        validators=[DataRequired(), Email()])
    password = PasswordField(label='Password',
                             id='field_password',
                             description='New password must contain a special character, an uppercase letter, an lowercase letter, a number and 8 charaters',
                             validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up',
                         id='button_register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
        
    def validate_password(self, password):
        if(len(password.data) < 8):
            raise ValidationError('Password must have at least 8 characters.')
        char_special = re.compile('[@_!#$%^&*()<>?/\|}{~:]')        
        if(char_special.search(password.data) == None):
            raise ValidationError('Password must contain a special character.')
        if(re.search(r'[A-Z]', password.data) == None):
            raise ValidationError('Password must contain at least 1 uppercase letter.')
        if(re.search(r'[a-z]', password.data) == None):
            raise ValidationError('Password must contain at least 1 lowercase letter.')
        if(re.search(r'\d', password.data) == None):
            raise ValidationError('Password must contain a number.')


class LoginForm(FlaskForm):
    email = StringField(label='Email',
                        id='field_email',
                        validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', 
                             id='field_password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login',
                         id='button_login')