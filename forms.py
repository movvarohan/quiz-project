from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import HiddenField,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class loginform(FlaskForm):
    email=StringField('Enter Email',validators=[DataRequired(),Email()])
    password=PasswordField('Enter Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign In')

class signupform(FlaskForm):
    name=StringField('Enter Name',validators=[DataRequired()])
    email=StringField('Create Email',validators=[DataRequired(),Email()])
    password=PasswordField('Create password',validators=[DataRequired()])
    submit=SubmitField('Create')

