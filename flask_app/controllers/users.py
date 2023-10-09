from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models import pet_model
from flask_app.models import payment_model

import smtplib
import ssl

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    images = ['images/patches.png', 'images/kiara.png', 'images/rio.png', 'images/spike.png']
    return render_template('index.html', images=images)

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data={
        "id": session['user_id']
    }
    user=User.get_one_user(data)
    pets = pet_model.Pet.get_all_pets(data)
    payments=payment_model.Payment.get_all_payments(data)
    return render_template('dashboard.html',user=user, pets=pets, payments=payments)


@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/user_login')
def user_login():
    return render_template('log.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route("/register",methods=['POST'])
def register():

    if not User.validate_user(request.form): 
        return redirect('/registration')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zipcode" : request.form['zipcode'],
        "password": pw_hash
    }
    
    id = User.save(data) 
    
    print(request.form)
    
    session['user_id'] = id 
    
    return redirect('/dashboard')

@app.route("/login",methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user = User.get_user_by_email(data)
    if not user:
        flash("Invalid Email/Password")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    
    session['user_id'] = user.id
    
    return redirect('/dashboard')

@app.route("/transport")
def transport():
    return render_template('transport.html')

@app.route("/vet_resources")
def resources():
    return render_template('vet_resources.html')

@app.route("/meet_ninjas")
def meet_the_ninjas():
    return render_template('ninjas.html')

@app.route("/privacy")
def privacy_policy():
    return render_template('privacy.html')

@app.route("/terms")
def terms_conditions():
    return render_template('terms.html')

@app.route("/email_successful")
def email_sent():
    return render_template("email.html")

@app.route('/send_email', methods=['POST'])
def send_email():
    
    recipient_email = request.form['recipient_email']
    pet_name = request.form['pet_name']
    transport_date = request.form['transport_date']
    pick_up = request.form['up_location']
    drop_off=request.form['off_location']
    

    smtp_server = "smtp.gmail.com" 
    smtp_port = 587
    smtp_username = "thegroovyninjas@gmail.com"
    smtp_password = "lqzi mcbt jkvg hgma"
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(587)
            server.login(smtp_username, smtp_password)
            
        email_message=(recipient_email, pet_name, transport_date, pick_up, drop_off)

    # Send the email
        server.sendmail(smtp_username, recipient_email, email_message)

        return redirect("/email_successful")
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')
