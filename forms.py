from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    username = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    first_name = TextField(
        'First Name', validators=[DataRequired(), Length(min=2, max=40)]
    )
    last_name = TextField(
        'Last Name', validators=[DataRequired(), Length(min=2, max=40)]
    )
    profession = SelectField(
        'Profession',
        choices=[('Doctor', 'Doctor'), ('InsuranceProfessional', 'Insurance Professional')],
        default='Doctor'
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class SearchRecordsForm(FlaskForm):
    first_name = TextField(
        'First Name', validators=[DataRequired(), Length(min=3, max=40)]
    )
    last_name = TextField(
        'Last Name', validators=[DataRequired(), Length(min=3, max=40)]
    )
