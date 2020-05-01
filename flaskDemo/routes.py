import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, db2, bcrypt, mysql
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, BudgetForm, PaymentForm, BudgetUpdateForm
from flaskDemo.models import User, Expense, Payment, Budget, BudgetsFor
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        results = Payment.query.join(Expense, Payment.expenseID == Expense.expenseID) \
                    .add_columns(Payment.description, Payment.date, Payment.amount, Expense.expenseID, Expense.expenseType) \
                    .join(User, Payment.userID == User.id) \
                    .add_columns(Payment.userID, User.id, User.username) \
                    .filter((Payment.userID == current_user.id) | (User.username == current_user.username)).all()
        cur = mysql.connection.cursor()
        sum = cur.execute("SELECT SUM(amount) FROM Payment")
        if sum > 0:
            total = cur.fetchall()
    else:
        return redirect(url_for('register'))
    return render_template('home.html', title = 'Home', payments = results, total = total)

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