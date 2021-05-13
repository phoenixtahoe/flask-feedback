from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Optional

class registerForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )
    email = StringField(
        "Email",
        validators=[InputRequired()],
    )
    first_name = StringField(
        "First name",
        validators=[InputRequired()],
    )
    last_name = StringField(
        "Last name"
    )

class loginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )

class feedbackForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired()],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )