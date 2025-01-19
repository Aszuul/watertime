from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    city = StringField("City")
    state = StringField("State")
    country_code = IntegerField("Country Code")
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class PlantSearchForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")
    