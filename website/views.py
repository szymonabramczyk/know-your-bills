import json
from datetime import datetime

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from . import db
from .models import Expense
from .utils import serialize_expense

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    expenses = [serialize_expense(expense)
                for expense in current_user.expenses]
    return render_template("home.html", user=current_user, expenses=expenses)


@views.route('/', methods=['POST'])
@login_required
def add_expense():
    expense_id = request.form.get('expense_id')

    # no expense_id given - add new expense
    if not expense_id:
        try:
            amount = float(request.form.get('add-amount'))
        except ValueError:
            flash('Incorrect amount!', category='error')
        else:
            date_str = request.form.get('add-date')
            category = request.form.get('add-category')
            payment_method = request.form.get('add-method')
            vendor = request.form.get('add-vendor')
            description = request.form.get('add-description')
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                new_expense = Expense(date=date, amount=amount, category=category, payment_method=payment_method,
                                      vendor=vendor, description=description, user_id=current_user.id)
            else:
                new_expense = Expense(amount=amount, category=category, payment_method=payment_method,
                                      vendor=vendor, description=description, user_id=current_user.id)

            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', category='success')

    # expense_id given - edit the expense with the given id
    if expense_id:
        expense = Expense.query.get(expense_id)
        if expense:
            try:
                amount = float(request.form.get('edit-amount'))
            except ValueError:
                flash('Incorrect amount!', category='error')
            else:
                date_str = request.form.get('edit-date')
                category = request.form.get('edit-category')
                payment_method = request.form.get('edit-method')
                vendor = request.form.get('edit-vendor')
                description = request.form.get('edit-description')
                date = datetime.strptime(date_str, '%Y-%m-%d')

                expense.amount = amount
                expense.category = category
                expense.date = date
                expense.payment_method = payment_method
                expense.vendor = vendor
                expense.description = description

                db.session.commit()
                flash('Expense edited!', category='success')

    expenses = [serialize_expense(expense)
                for expense in current_user.expenses]
    return render_template("home.html", user=current_user, expenses=expenses)


@views.route('/delete-expense', methods=['POST'])
def delete_method():
    data = json.loads(request.data)
    expense_id = data['expenseId']
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error', 'message': 'Expense record not found'}), 404
