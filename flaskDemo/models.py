from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['User']
    '''
    __table_args__ = {'extend_existing': True}
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    # b.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.image_file}')"
    '''

class Expense(db.Model):
    __table__ = db.Model.metadata.tables['Expense']
    '''
    __table_args__ = {'extend_existing': True}
    expenseId = db.Column(db.Integer, primary_key=True)
    expenseType = db.Column(db.String(20), nullable=False)
    totalAmount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Expense('{self.expenseType}', '{self.totalAmount}')"
    '''

class Payment(db.Model):
    __table__ = db.Model.metadata.tables['Payment']
    
    '''
    __table_args__ = {'extend_existing': True}
    paymentId = db.Column(db.Integer, primary_key=True)
    expenseId = db.Column(db.Integer, db.ForeignKey('expense.expenseId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Payment('{self.amount}', '{self.description}', '{self.date}')"
    '''

class Budget(db.Model):
    __table__ = db.Model.metadata.tables['Budget']
    '''
    __table_args__ = {'extend_existing': True}
    budgetId = db.Column(db.Integer, primary_key=True)
    budgetType = db.Column(db.String(20), nullable=False)
    dateRange = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    budgetName = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Budget('{self.budgetName}', '{self.budgetType}', '{self.amount}', '{self.dateRange}')"
    '''

class BudgetsFor(db.Model):
    __table_args__ = {'extend_existing': True}
    budgetID = db.Column(db.Integer, db.ForeignKey("budget.budgetID"), primary_key=True)
    expenseID = db.Column(db.Integer,db.ForeignKey("expense.expenseID"),primary_key=True)
    