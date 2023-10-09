from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Pet:
    DB="groovyninja"
    def __init__(self, data):
        self.id=data["id"]
        self.name=data["name"]
        self.age=data["age"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user_id = data["user_id"]
        self.user=None
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO pets (name, age, user_id, created_at, updated_at) VALUES (%(name)s, %(age)s, %(user_id)s, Now(), Now());"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    @classmethod
    def get_all_pets(cls, data):
        query = "SELECT * FROM pets LEFT JOIN users on pets.user_id=users.id"
        results = connectToMySQL(cls.DB).query_db(query, data)

        if not results:
            return []
        
        pets=[]
        
        for row in results:
            this_pet=cls(row)
            
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
            this_pet.user=user_model.User(user_data)
            pets.append(this_pet)
        return pets
    
    @classmethod
    def get_pet_by_id(cls,data):
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    @classmethod
    def update(cls, data):
        query = "UPDATE pets SET name=%(name)s, age=%(age)s, updated_at=NOW()WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM pets WHERE id = %(id)s;"
        data={
            'id': id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_one_pet(cls, data):
        query = '''
            SELECT *, (SELECT COUNT(user_id) FROM likes WHERE likes.item_id=items.id AND user_id=%(user_id)s) AS liked,
            (SELECT COUNT(user_id) FROM likes WHERE likes.item_id=items.id) AS number_of_likes FROM items 
            LEFT JOIN users ON items.user_id=users.id
            WHERE items.id=%(item_id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)

        this_pet = cls(results[0]) # Instantiate the item using the data from the db

        user_data={
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'address' : results[0]['address'],
                'city' : results[0]['city'],
                'state' : results[0]['state'],
                'zipcode' : results[0]['zipcode'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at'],
            }
        
        this_pet.user = user_model.User(user_data) # Instantiate the user and associate them with the item

        return this_pet # Return the instance of the item (along with the user)
    