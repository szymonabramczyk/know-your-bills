def serialize_expense(expense):
    return {
        "id": expense.id,
        "date": expense.date.strftime('%Y-%m-%d'),
        "amount": expense.amount,
        "category": expense.category,
        "payment_method": expense.payment_method,
        "vendor": expense.vendor,
        "description": expense.description
    }
