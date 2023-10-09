from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.pet_model import Pet
from flask_app.models import pet_model

@app.route("/pets")
def pet():
    return render_template('add_pet.html')

@app.route("/pets/add", methods=['GET', 'POST'])
def add_pet():
    
    data = {
        'name': request.form['name'],
        'age': request.form['age'],
        'user_id': request.form['user_id']
    }
    Pet.save(data) 
    return redirect('/dashboard')

@app.route("/pets/<int:id>/delete")
def delete(id):
    Pet.delete(id)
    return redirect("/dashboard")

@app.route("/pets/<int:id>/update", methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        pet = Pet.get_all_pets(id)
        return render_template("update_pet.html", pet=pet)
    
    if request.method == 'POST':
        data = {
            
            'name': request.form['name'],
            'age': request.form['age'],
            'id' : id,
        }
        pet=Pet.get_pet_by_id(id)
        Pet.update(data)
        return redirect("/dashboard")