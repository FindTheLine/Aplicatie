from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from wtforms.widgets import TextArea
from flask_wtf.file import FileField

# Create A Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create Login Form
class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create Project Form
class ProjectForm(FlaskForm):
	class Meta:
		csrf = False
		
	project = SelectField("Adauga in: ", choices=[])
	submit = SubmitField("Modifica")
 
class CommentForm(FlaskForm):
	title = StringField("Titlu")
	text = TextAreaField("Comentariu", validators=[DataRequired()])
	submit = SubmitField("Modifica")

class ProfileForm(FlaskForm):
	name = StringField("Nume", validators=[DataRequired()])
	surname = StringField("Prenume", validators=[DataRequired()])
	old_password = PasswordField("Parola veche", validators=[DataRequired()])
	new_password = PasswordField("Parola noua", validators=[DataRequired()])
	resub_new_password = PasswordField("Repeta parola noua", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Form Class
class UserForm(FlaskForm):
	name = StringField("Nume", validators=[DataRequired()])
	surname = StringField("Prenume", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	department = SelectField("Departament", choices=[],validators=[DataRequired()])
	project = SelectField("Proiect", choices=[])

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Trimite link-ul de resetare")

	def validate_email(self,email):
		from .models import Usr
		user = Usr.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account associated with this email')

class ResetPasswordForm(FlaskForm):
	new_password = PasswordField("Parola noua", validators=[DataRequired()])
	resub_new_password = PasswordField("Repeta parola noua", validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Reseteaza parola")