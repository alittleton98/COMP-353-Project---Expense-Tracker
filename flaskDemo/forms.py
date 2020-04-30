from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Expense, Payment, Budget, BudgetsFor
from wtforms.fields.html5 import DateField


'''
ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above
pnos = Project.query.with_entities(Project.pnumber).distinct()
results=list()
for row in pnos:
    rowDict=row._asdict()
    results.append(rowDict)
projChoices = [(row['pnumber'],row['pnumber']) for row in results]

emps = Employee.query.with_entities(Employee.ssn).distinct()
results2 = list()
for row in emps:
    rowDict=row._asdict()
    results2.append(rowDict)
empChoices = [(row['ssn'],row['ssn']) for row in results2]

myChoices2 = [(row[0],row[0]) for row in ssns]  # change
results3=list()
for row in ssns:
    rowDict=row._asdict()
    results3.append(rowDict)
myChoices = [(row['mgr_ssn'],row['mgr_ssn']) for row in results3]
regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2
'''

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
    '''
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    '''

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


'''

class DeptForm(DeptUpdateForm):

    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    submit = SubmitField('Add this department')

    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
        dept = Department.query.filter_by(dnumber=dnumber.data).first()
        if dept:
            raise ValidationError('That department number is taken. Please choose a different one.')
            
class AssignForm(FlaskForm):
    pno=SelectField("Project", choices = projChoices, coerce=int)
    ssn=SelectField("Employee", choices = empChoices)
    submit = SubmitField('Assign')
    
    def validate_ssn(self, ssn):
        combos = Works_On.query.filter_by(pno=self.pno.data)
        if combos:
            for combo in combos:
                if str(combo.essn) == str(self.ssn.data):
                    raise ValidationError('This employee is already assigned to this project.')

'''

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
	
	##needs work 
	'''
		def validate_expense(self, expenses):
			combos = Works_On.query.filter_by(pno=self.pno.data)
			if combos:
				for combo in combos:
					if str(combo.essn) == str(self.ssn.data):
						raise ValidationError('This employee is already assigned to this project.')
	'''


