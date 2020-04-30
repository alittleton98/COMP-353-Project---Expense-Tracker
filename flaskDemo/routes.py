import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, BudgetForm, PaymentForm, BudgetUpdateForm
from flaskDemo.models import User, Expense, Payment, Budget, BudgetsFor
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
    '''
    results2 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
               .add_columns(Employee.fname, Employee.lname, Employee.ssn, Works_On.essn, Works_On.pno) \
               .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname, Project.pnumber)
    results = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
                .add_columns(Employee.fname, Employee.lname)
    '''
    if current_user.is_authenticated:
        results = Payment.query.join(Expense, Payment.expenseID == Expense.expenseID) \
                    .add_columns(Payment.description, Payment.date, Payment.amount, Expense.expenseID, Expense.expenseType) \
                    .join(User, Payment.userID == User.id) \
                    .add_columns(Payment.userID, User.id, User.username) \
                    .filter((Payment.userID == current_user.id) | (User.username == current_user.username)).all()
    else:
        return redirect(url_for('register'))
    ##return render_template('join.html', title='Join', joined_m_n=results2)
    #TODO use query to either display all payments and do a join with expense and payments and maybe budgets too 
    return render_template('home.html', title = 'Home', payments = results, expenseTypes = results)

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
        user = User(username=form.username.data, password=hashed_password, name=form.fullname.data)
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
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
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', title='Account', form=form)

@app.route("/budgets")
@login_required
def budgets():
	#TODO For this you need to calculate total amount spent. Will require a join with payments and budget. 
	#...will need to match expense IDs and make sure date is within the budget time range. 
    
    results = Budget.query.join(Payment, Payment.expenseID == Budget.expenseID) \
                    .add_columns(Budget.budgetID, Budget.budgetName, Budget.amount, Budget.startDate, Budget.endDate, Payment.description, Payment.amount.label("payAmount"), Payment.date) \
                    .filter(Budget.userID == current_user.id).all()
    
    
    return render_template('budgets.html', title = 'Budgets', budgets = results)

@app.route("/budget/new", methods=['GET', 'POST'])
@login_required 
def new_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        assign = Budget(userID = current_user.id, budgetName = form.bName.data, expenseID = form.expenseType.data, startDate = form.sDate.data, endDate = form.eDate.data, amount = form.amount.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have created a new budget!', 'Success')
        return redirect(url_for('home'))
    return render_template('create_budget.html', title='New Budget', form=form, legend='New Budget')


@app.route("/payment/new", methods=['GET', 'POST'])
@login_required 
def new_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        assign = Payment(userID = current_user.id, expenseID = form.expenseType.data, description = form.pName.data, amount = form.amount.data, date = form.date.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new Payment!', 'Success')
        return redirect(url_for('home'))
    return render_template('create_payment.html', title='New Payment', form=form, legend='New Payment')

@app.route("/budgets/<budgetID>")
@login_required
def budget(budgetID):
    budget = Budget.query.get_or_404(budgetID)
    return render_template('budget.html', title=budget.budgetName, budget=budget, now=datetime.utcnow())

@app.route("/budgets/<budgetID>/delete", methods=['POST'])
@login_required
def delete_budget(budgetID):
    budget = Budget.query.get_or_404(budgetID)
    db.session.delete(budget)
    db.session.commit()
    flash('The budget has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/budget/<budgetID>/update", methods=['GET', 'POST'])
@login_required
def update_budget(budgetID):
    budget = Budget.query.get_or_404(budgetID)
    currentBudget = budget.budgetName

    form = BudgetUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentBudget !=form.bName.data:
            budget.budgetName=form.bName.data
        budget.amount=form.amount.data
        budget.startDate=form.sDate.data
        budget.endDate=form.eDate.data
        budget.expenseID=form.expenseType.data
        db.session.commit()
        flash('Your budget has been updated!', 'success')
        return redirect(url_for('budget', budgetID=budgetID))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        form.bName.data = budget.budgetName
        form.amount.data = budget.amount
        form.sDate.data = budget.startDate
        form.eDate.data = budget.endDate
        form.expenseType.data = budget.expenseID
    return render_template('create_budget.html', title='Update Budget',
                           form=form, legend='Update Budget')


'''
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

@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home'))
    

'''

