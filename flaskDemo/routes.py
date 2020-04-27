import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeptForm,DeptUpdateForm, AssignForm, BudgetForm, PaymentForm
from flaskDemo.models import User, Post, Department, Dependent, Dept_Locations, Employee, Project, Works_On
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


#Test display for payments
payments = list()
payment = dict()
payment['name'] = "payment1"
payment['amount'] = 50
payment['date'] = "2020-01-01"
payment['expense'] = "ExpenseID1"
payments.append(payment) 

payment = dict()
payment['name'] = "payment2"
payment['amount'] = 20
payment['date'] = "2020-01-02"
payment['expense'] = "ExpenseID2"
payments.append(payment) 

payment = dict()
payment['name'] = "payment3"
payment['amount'] = 40
payment['date'] = "2020-01-03"
payment['expense'] = "ExpenseID3"
payments.append(payment) 

payment = dict()
payment['name'] = "payment4"
payment['amount'] = 85
payment['date'] = "2020-01-04"
payment['expense'] = "ExpenseID4"
payments.append(payment) 

payment = dict()
payment['name'] = "payment5"
payment['amount'] = 23
payment['date'] = "2020-01-05"
payment['expense'] = "ExpenseID5"
payments.append(payment) 

#test display for budgets
tbudgets = list()
budget = dict()
budget['name'] = "Budget0"
budget['amount'] = 2000
budget['sdate'] = "2020-01-01"
budget['edate'] = "2020-02-01"
budget['expense'] = "ExpenseID1"
tbudgets.append(budget) 

budget = dict()
budget['name'] = "budget1"
budget['amount'] = 3282
budget['sdate'] = "2020-01-02"
budget['edate'] = "2020-02-01"
budget['expense'] = "ExpenseID1"
tbudgets.append(budget) 

budget = dict()
budget['name'] = "budget2"
budget['amount'] = 450
budget['sdate'] = "2020-01-03"
budget['edate'] = "2020-03-01"
budget['expense'] = "ExpenseID1"
tbudgets.append(budget) 

budget = dict()
budget['name'] = "budget3"
budget['amount'] = 20000
budget['sdate'] = "2020-01-04"
budget['edate'] = "2020-02-01"
budget['expense'] = "ExpenseID1"
tbudgets.append(budget) 

budget = dict()
budget['name'] = "budget4"
budget['amount'] = 4500
budget['sdate'] = "2020-01-05"
budget['edate'] = "2020-02-01"
budget['expense'] = "ExpenseID1"
tbudgets.append(budget) 

@app.route("/")
@app.route("/home")
def home():
    #results = Employee.query.all()
    #return render_template('dept_home.html', outString = results)
    #posts = Post.query.all()
    #return render_template('home.html', posts=posts)
    results2 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
               .add_columns(Employee.fname, Employee.lname, Employee.ssn, Works_On.essn, Works_On.pno) \
               .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname, Project.pnumber)
    results = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
                .add_columns(Employee.fname, Employee.lname)
    ##return render_template('join.html', title='Join', joined_m_n=results2)
    #TODO use query to either display all payments and do a join with expense and payments and maybe budgets too 
    return render_template('home.html', title = 'Home', payments = payments)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
        assign = Works_On(essn=form.ssn.data, pno=form.pno.data,hours=0)
        db.session.add(assign)
        db.session.commit()
        flash('You have assigned an employee to a project!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='Assign Employee',
                           form=form, legend='Assign Employee')



@app.route("/assign/<pno>/<essn>")
@login_required
def assign(pno, essn):
    assign = Works_On.query.get_or_404([essn,pno])
    return render_template('assign.html', title = str(assign.essn) + "_" + str(assign.pno), assign = assign, now = datetime.utcnow)


@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())


@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
@login_required
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.dnumber.data = dept.dnumber
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('create_dept.html', title='Update Department',
                           form=form, legend='Update Department')




@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home'))
    
    
@app.route("/assign/<pno>/<essn>/delete", methods=['POST'])
@login_required
def delete_assignment(essn,pno):
    assign = Works_On.query.get_or_404([essn,pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The assignment has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/budgets")
@login_required
def budgets():
	#TODO For this you need to calculate total amount spent. Will require a join with payments and budget. 
	#...will need to match expense IDs and make sure date is within the budget time range. 
	return render_template('budgets.html', title = 'Budgets', tbudgets = tbudgets)

@app.route("/budget/new")
@login_required 
def new_budget():
	form = BudgetForm()
	##TODO
	if form.validate_on_submit(): 
		return redirect(url_for('home'))
	return render_template('create_budget.html', title='New Budget',
						form=form, legend='New Budget')

@app.route("/payment/new")
@login_required 
def new_payment():
	form = PaymentForm()
	##TODO 
	if form.validate_on_submit(): 
		return redirect(url_for('home'))
	return render_template('create_payment.html', title='New Payment',
						form=form, legend='New Payment')
