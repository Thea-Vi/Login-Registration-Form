import re

from flask import flash
from flask_bcrypt import Bcrypt

from flask_app import app


from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("log_register_schema").query_db(query)
        
        users = []
        for u in users:
            users.append(cls(u))
        
        return users
        
        
        
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("log_register_schema").query_db(query, data)
        
        if len(results) < 1:
            return False
        
        return User(results[0])
        
        
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("log_register_schema").query_db(query, data)
        
        if len(results) < 1:
            return False
        
        return User(results[0])
        
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        # query returns the id of the newly created user
        return connectToMySQL("log_register_schema").query_db(query, data)
     
 
    @staticmethod
    def register_validator(info):
        is_valid = True
        
        if len(info['first_name']) < 2:
            flash('First Name must be at least 2 characters.')
            is_valid = False
            
        if len(info['last_name']) < 2:
            flash('Last Name must be at least 2 characters.')      
            is_valid = False
            
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(info['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        else:
            user = User.get_by_email({'email': info['email']})
            if user:
                flash('Email is already in use')
                is_valid = False
                
        
        if len(info['password']) < 5:
            flash('Password must be at least 5 characters.')
            is_valid = False
            
        # if len(info['password']) != info['confirm_password']:
        #     flash('Password must match!')      
        #     is_valid = False
            
        return is_valid
        
    
    @staticmethod
    def login_validator(info):    
        user = User.get_by_email({'email': info['email']})
        
        if not user:
            flash('Invalid. Try again')
            return False
        
        if not bcrypt.check_password_hash(user.password, info['password']):
            flash('Invalid Credentials')
            return False
        
        return True
            
        
        
    


    