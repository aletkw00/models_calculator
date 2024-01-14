from flask_wtf import FlaskForm
from flask_wtf.file import FileField, MultipleFileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, InputRequired
from flaskr.models import User
from flask_login import current_user
import re

class AccountForm(FlaskForm):
    email = StringField(label='Email',
                        id='field_email',
                        description='Type new email',
                        validators=[DataRequired(), Email()])
    password = PasswordField(label='Password',
                             id='field_password',
                             description='New password must contain a special character, an uppercase letter, an lowercase letter, a number and 8 charaters',
                             validators=[Optional()])
    update = SubmitField(label='Update',
                         id='button_update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
        
    def validate_password(self, password):
        if password.data != "":
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
        


class ModelForm(FlaskForm):
    model_dir = StringField(label='Model Directory:',
                            id="field_model_dir",
                            description='Type a new folder name or select an existing folder',
                            validators=[DataRequired(), Length(max=20)])
    file_input = FileField(label='Model input:',
                           id="field_file_input",
                           description='Choose a input file',
                           validators=[FileRequired(), FileAllowed(['csv'], 'Only one CVS file')])
    files_output = MultipleFileField(label='Model expected outputs:',
                                     id="field_files_output",
                                     description='Choose multiple expected output',
                                     validators=[FileRequired(), FileAllowed(['csv'], 'Only CVS files')])
    window = IntegerField(label='Window:',
                          id="field_window",
                          description='Enter a integer value from 0',
                          validators=[Optional()])
    modelname = StringField(label='Model Name:',
                            id="field_model_name",
                            description='Before the name there is always current year_month_day_hour_min_sec',
                            validators=[InputRequired(), Length(max=20)])
    test = BooleanField(label='Test:',
                        id="field_test",
                        validators=[Optional()])
    submit = SubmitField(label='Run Script',
                         id="submit_button")

    def validate_window(self, window):
        if window.data < 0:
            raise ValidationError('Must be greater or equal than 0')