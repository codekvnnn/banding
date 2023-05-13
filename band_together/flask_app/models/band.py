from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user import User

class Band:
    db = "band_schema"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.city = data['city']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        
        
# create
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO bands(name,genre,city,user_id)
            VALUES (%(name)s,%(genre)s,%(city)s,%(user_id)s)
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
# read
    @classmethod
    def select_one(cls, data):
        query="""SELECT * FROM bands 
            JOIN users ON users.id = bands.user_id 
            WHERE bands.id=%(id)s"""
        results=connectToMySQL(cls.db).query_db(query, data)
        result=results[0]
        print(result)
        temp={
            'id': result['users.id'],
            'first_name': result['first_name'], 
            'last_name': result['last_name'], 
            'email': result['email'], 
            'password': result['password'], 
            'created_at': result['users.created_at'], 
            'updated_at': result['users.updated_at']
        }
        result=cls(result)
        result.user=User(temp)
        return result
    
# update
    @classmethod
    def update(cls,data):
        query="""UPDATE bands SET name=%(name)s, city=%(city)s, genre=%(genre)s, user_id=%(user_id)s 
                WHERE id = %(id)s"""
                
        return connectToMySQL(cls.db).query_db(query, data)
    
# delete
    @classmethod
    def delete(cls,data):
        query="""DELETE FROM bands 
                WHERE id=%(id)s"""
                
        return connectToMySQL(cls.db).query_db(query, data)
    
                                    # retreve
    @classmethod
    def get_all(cls):
        query="""SELECT * FROM bands 
            JOIN users ON users.id = bands.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        print (results)
        bands = []
        for row in results:
            temp={
                'id': row['users.id'],
                'first_name': row['first_name'], 
                'last_name': row['last_name'], 
                'email': row['email'], 
                'password': row['password'], 
                'created_at': row['users.created_at'], 
                'updated_at': row['users.updated_at']
            }
            result=cls(row)
            result.user=User(temp)
            bands.append(result)
        return bands
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Band Name min 2 characters")
            is_valid = False
        if len(data['genre']) < 2:
            flash("Music Genre min 2 characters")
            is_valid = False    
        if len(data['city']) < 2:
            flash("City is missing")
            is_valid = False
        return is_valid
        
    @classmethod
    def my_bands(cls, data):
        query="""SELECT * FROM bands 
            JOIN users ON users.id = bands.user_id
            WHERE bands.user_id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print (results)
        bands = []
        for row in results:
            temp={
                'id': row['users.id'],
                'first_name': row['first_name'], 
                'last_name': row['last_name'], 
                'email': row['email'], 
                'password': row['password'], 
                'created_at': row['users.created_at'], 
                'updated_at': row['users.updated_at']
            }
            result=cls(row)
            result.user=User(temp)
            bands.append(result)
        return bands