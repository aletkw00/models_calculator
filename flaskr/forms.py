from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from flaskr.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ModelForm(FlaskForm):
    model_dir = StringField('Model_dir', validators=[DataRequired(), Length(max=20)])
    window = IntegerField('window', validators=[Optional()])
    test = BooleanField('test')
    modelname = StringField('modelname', validators=[Length(max=20)])
    submit = SubmitField('Run Script')

    def validate_window(self, window):
        if window.data < 0:
            raise ValidationError('Must be greater or equal than 0')