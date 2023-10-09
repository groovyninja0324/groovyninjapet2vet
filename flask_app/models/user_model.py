from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import payment_model, pet_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

pattern = r'^\d{5}(?:-\d{4})?$'

class User:
    DB="groovyninja"
    def __init__(self, data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.address=data["address"]
        self.city=data["city"]
        self.state=data["state"]
        self.zipcode=data["zipcode"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.pets =[]
        self.payments=[]
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, address, city, state, zipcode, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(address)s, %(city)s, %(state)s, %(zipcode)s, Now(), Now());"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_pet(cls, data):
        query = "SELECT * from users LEFT JOIN pets on users.id = pets.user_id where users.id= %(id)s"
        results =connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        print(results)
        user_data=results[0]
        user=cls(user_data)
        pets=[]
        for pet in results:
                pet_data={
                    "id" : pet['pets.id'],
                    "name" : pet['name'],
                    "age" : pet['age'],
                    "created_at" : pet["pets.created_at"],
                    "updated_at" : pet["pets.updated_at"],
                    "user_id" : pet['user_id']                
        }
        pet = pet_model.Pet(pet_data)
        pets.append(pet)
        return user

    
    @classmethod
    def get_user_by_payment(cls, data):
        query = "SELECT * from users LEFT JOIN payments on users.id = payments.user_id where users.id= %(id)s;"
        results =connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        user=cls(results[0])
        payments=[]
        for payment in results:
            payment_data={
                "id" : payment['payments.id'],
                "first_name" : payment['payments.first_name'],
                "last_name" : payment['payments.last_name'],
                "card_number" : payment['card_number'],
                "date" : payment['date'],
                "cvv" : payment['cvv'],
                "created_at" : payment["payments.created_at"],
                "updated_at" : payment["payments.updated_at"],
                "user_id" : payment['user_id']              
        }
        this_payment = payment_model.Payment(payment_data)
        payments.append(this_payment)
        return user
    
    @classmethod
    def get_user_by_email(cls,data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users Where first_name=%(first_name)s AND last_name=%(last_name)s;"
        results = connectToMySQL('groovyninja').query_db(query,user)
        
        if len(results) >= 1:
            flash("Name already taken.")
            is_valid=False
            
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid= False
            
        else:
            if user['first_name'].isnumeric(): 
                flash("First name cannot have numbers")
                is_valid= False
                
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_valid= False
            
        else:
            if user['last_name'].isnumeric(): 
                flash("Last name cannot have numbers")
                is_valid= False
                
        if re.match(pattern, user['zipcode']):
            flash("Invalid zipcode!")
            is_valid=True
        
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
            
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid= False
            
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match")
            is_valid= False
            
        return is_valid