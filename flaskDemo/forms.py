from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Expense, Payment, Budget, BudgetsFor
from wtforms.fields.html5 import DateField


expenses = Expense.query.with_entities(Expense.expenseType, Expense.expenseID).distinct()
results = list()
for row in expenses:
    rowDict=row._asdict()
    results.append(rowDict)
expenseChoices = [(row['expenseID'], row['expenseType']) for row in results]

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', 
                           validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class BudgetUpdateForm(FlaskForm):
    bName=StringField('Budget Name:', validators=[DataRequired(),Length(max=15)])
    amount = IntegerField("Amount", validators = [DataRequired()])
    sDate = DateField("Start Date", validators = [DataRequired()])
    eDate = DateField("End Date", validators = [DataRequired()])
    expenseType = SelectField("Expense Type", choices = expenseChoices, coerce=int)
    submit = SubmitField('Update Budget')

class BudgetForm(BudgetUpdateForm):
    submit = SubmitField('Create Budget')
	
class PaymentForm(FlaskForm):
	pName = StringField("Payment Name", validators = [DataRequired()])
	amount = IntegerField("Amount", validators = [DataRequired()]) 
	date = DateField("Date", validators = [DataRequired()])
	expenseType = SelectField("Expense Type", choices = expenseChoices, coerce=int)
	submit = SubmitField('Add Payment')