from Flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session
from Flask_app import bcrypt
# from .recipe import Recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
    
    @staticmethod
    def add_user(data:dict):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);'
        id = connectToMySQL('recipes').query_db(query, data)
        return id

    @classmethod
    def val_new_user(cls, data:dict):
        is_val = True
        if len(data['first_name']) < 2 or str.isalpha(data['first_name']) == False:
            is_val = False
            flash('Must have valid first name')
        if len(data['last_name']) < 2 or str.isalpha(data['last_name']) == False:
            is_val = False
            flash('Must have valid last name')
        if not EMAIL_REGEX.match(data['email']):
            is_val = False
            flash('Must have valid email')
        emails = cls.get_all_emails()
        for email in emails:
            if email['email'] == data['email']:
                is_val = False
                flash('Must have unique email')
        if len(data['password']) < 8:
            is_val = False
            flash('Password must be at least 8 characters')
        if not str.isalnum(data['password']):
            is_val = False
            flash('Must have 1 letter and 1 number')
        else:
            if str.isalpha(data['password']) or str.isnumeric(data['password']):
                is_val = False
                flash('Must have 1 letter and 1 number')
        if data['password'] != data['conf_password']:
            is_val = False
            flash('Passwords must match')
        return is_val

    @staticmethod
    def get_all_emails():
        query = 'SELECT email FROM users'
        emails = connectToMySQL('recipes').query_db(query)
        return emails

    @staticmethod
    def login(data:dict):
        if data['email'] == '' or data['password'] == '':
            session['is_reg'] = False
            flash('Invalid username/ password')
            return True
        query = 'SELECT id, password FROM users WHERE email = %(email)s'
        user = connectToMySQL('recipes').query_db(query, data)
        if bcrypt.check_password_hash(user[0]['password'], data['password']):
            session['user_id'] = user[0]['id']
            return user
        else:
            session['is_reg'] = False
            flash('Invalid username/ password')
            return True

    @classmethod
    def get_user_from_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        data = {'id': id}
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])