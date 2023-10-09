from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.payment_model import Payment

import stripe

SECRET_KEY = "sk_test_51NywdBA1oLqqmXpmXuORNInYcBKjAF701v2EWbxiPsN4qtfGT9lRqyUxXesMKO4Oc1sTPX8oPQ7Gcn3xcsYRSfXe00cTZCVuIz"

stripe.api_key=SECRET_KEY

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Get token and amount from the request
        token = request.json['token']
        amount = int(request.json['amount']) * 100  # Convert to cents

        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            description='Payment for Transport',
            source=token,
        )

        # If the charge is successful, redirect to the payment confirmation page
        if charge.status == 'succeeded':
            return redirect(url_for('payment_confirmation', amount=amount / 100, transaction_id=charge.id))
        else:
            return "Payment failed."

    except Exception as e:
        # Handle errors and return an appropriate response
        return str(e)
    
@app.route('/payment_confirmation')
def payment_confirmation():
    # You would typically retrieve payment details from a database or session here
    amount = request.args.get('amount')
    transaction_id = request.args.get('transaction_id')
    return render_template('payment_confirmation.html', amount=amount, transaction_id=transaction_id)

@app.route("/payments")
def add_payment_method():
    return render_template('add_payment.html')

@app.route("/payments/add", methods=['GET', 'POST'])
def add_payment():
    
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "card_number" : request.form["card_number"],
        "month" : request.form["month"],
        "year" : request.form ["year"],
        "cvv" : request.form["cvv"],
        "payment_name" : request.form["payment_name"],
        "user_id": request.form['user_id']
    }
    Payment.save(data) 
    return redirect('/dashboard')

@app.route("/payments/<int:id>/view")
def view_payment_info(id):
    data ={
        'id' : id
    }
    payment_data = Payment.get_payment_by_id(data)
    return render_template("payment_info.html", payment=payment_data)

@app.route("/payments/<int:id>/delete")
def delete_payment(id):
    Payment.delete(id)
    return redirect("/dashboard")

@app.route("/payments/<int:id>/update", methods=['GET', 'POST'])
def update_payment(id):
    if request.method == 'GET':
        payment = Payment.get_payment_by_id(id)
        return render_template("update_payment.html", payment=payment)
    
    if request.method == 'POST':
        payment = Payment.get_payment_by_id(id)  # Retrieve the existing payment
        payment.card_number = request.form["card_number"]
        payment.month = request.form["month"]
        payment.year = request.form["year"]
        payment.cvv = request.form["cvv"]
        payment.payment_name = request.form["payment_name"]
        payment.user_id = request.form["user_id"]
    
    # Save the updated payment to the database (assuming you have a save method)
        Payment.save()  # Adjust this based on your actual database interaction
    
    return redirect("/dashboard")
