from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app


bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,
# which is made by invoking the function Bcrypt with our app as an argument

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, username, password, created_at, updated_at ) 
        VALUES (%(fname)s , %(lname)s, %(email)s , %(username)s, %(password)s, NOW(), NOW() );"""
        return connectToMySQL('users').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, data):
        query = " SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('users').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, user_id, data):
        data = {
            "user_id": user_id,
            "email": data["email"],
            "fname": data["fname"],
            "lname": data["lname"],
            "username": data["username"],
            "password": data["password"]
        }
        query = """
        UPDATE users 
        SET first_name = %(fname)s, last_name= %(lname)s, email=%(email)s, username=%(username)s, password=%(password)s
        WHERE id= %(user_id)s;"""
        return connectToMySQL('users').query_db(query, data)

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s"
        result = connectToMySQL('users').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
  
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = " SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('users').query_db(query,user)
        if len(results) >= 1:
            flash("Email is already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email.", "register")
            is_valid = False
        if len(user["fname"]) < 3:
            flash("Invalid first name. First name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["lname"]) < 3:
            flash("Invalid last name. Last name must be at least 3 characters. ", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Invalid password. Password must be at least 8 characters.", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match.", "register")
        return is_valid
    
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('users').query_db(query,user)
        
        return is_valid 