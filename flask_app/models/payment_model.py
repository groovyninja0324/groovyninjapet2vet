from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Payment:
    DB="groovyninja"
    def __init__(self, data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.card_number=data["card_number"]
        self.month=data["month"]
        self.year=data["year"]
        self.cvv=data["cvv"]
        self.user_id = data["user_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.payment_name=data["payment_name"]
        self.user=None
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO payments (first_name, last_name, card_number, month, year, cvv, payment_name, user_id, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(card_number)s, %(month)s, %(year)s, %(cvv)s, %(payment_name)s, %(user_id)s, Now(), Now());"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    
    @classmethod
    def update(cls, data):
        query = """UPDATE payments 
                SET first_name=%(first_name)s, last_name=%(last_name)s, card_number=%(cars_number)s, month=%(month)s, year=%(year)s, cvv=%(cvv)s, user_id=%(user_id)s, payment_name=%(payment_name)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM payments WHERE id = %(id)s;"
        data={
            'id': id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_payment_by_id(cls,data):
        query = "SELECT * FROM payments WHERE id = %(id)s;"
        results = connectToMySQL('groovyninja').query_db(query,data)
        return results
    
    @classmethod
    def get_all_payments(cls, data):
        query = "SELECT * FROM payments LEFT JOIN users on payments.user_id=users.id"
        results = connectToMySQL(cls.DB).query_db(query, data)

        if not results:
            return []
        
        payments=[]
        
        for row in results:
            this_payment=cls(row)
            
            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'address' : row['address'],
                'city' : row['city'],
                'state' : row['state'],
                'zipcode' : row['zipcode'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            this_payment.user=user_model.User(user_data)
            payments.append(this_payment)
        return payments