from Flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session
# from Flask_app import bcrypt

class Ride:
    def __init__(self, data:dict):
        self.id = data['id']
        self.pick_up = data['pick_up']
        self.destination = data['destination']
        self.date = data['date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rider_name = data['first_name']
        self.rider_id = data['rider_id']
        if data['driver_id'] != None:
            self.driver_name = data['drivers.first_name']
            self.driver_id = data['drivers.id']
        return

    @staticmethod
    def add_ride(data):
        query = """INSERT INTO rides (pick_up, destination, date, details, rider_id)
        VALUES (%(pick_up)s, %(destination)s, %(date)s, %(details)s, %(rider_id)s)"""
        id = connectToMySQL('ohana').query_db(query, data)
        return id

    @staticmethod
    def val_ride(data):
        is_val = True
        if len(data['destination']) <= 3:
            is_val = False
            flash('Must have valid destination')
        if len(data['pick_up']) <= 3:
            is_val = False
            flash('Must have valid pick-up location')
        if data['date'] == '':
            is_val = False
            flash('Must include Date')
        if len(data['details']) <= 10:
            is_val = False
            flash('Must have valid details')
        if is_val == False:
            session['destination'] = data['destination']
            session['pick_up'] = data['pick_up']
            session['date'] = data['date']
            session['details'] = data['details']
        return is_val

    @staticmethod
    def edit_ride(data:dict):
        query = """UPDATE rides SET pick_up = %(pick_up)s, details = %(description)s WHERE id = %(id)s"""
        connectToMySQL('ohana').query_db(query, data)
        return

    @classmethod
    def get_all_rides(cls):
        query = 'SELECT * FROM rides LEFT JOIN users AS riders ON riders.id = rides.rider_id LEFT JOIN users AS drivers ON drivers.id = rides.driver_id'
        results = connectToMySQL('ohana').query_db(query)
        rides = []
        for ride in results:
            rides.append(cls(ride))
        return rides

    @classmethod
    def get_ride_from_id(cls, id):
        data = {'id': id}
        query = 'SELECT * FROM rides LEFT JOIN users AS riders ON riders.id = rides.rider_id LEFT JOIN users AS drivers ON drivers.id = rides.driver_id WHERE rides.id = %(id)s'
        result = connectToMySQL('ohana').query_db(query, data)
        return cls(result[0])

    @staticmethod
    def add_driver(data):
        query = """UPDATE rides SET driver_id = %(driver_id)s WHERE id = %(id)s;"""
        connectToMySQL('ohana').query_db(query, data)
        return

    @staticmethod
    def remove_driver(data):
        query = """UPDATE rides SET driver_id = null WHERE id = %(id)s;"""
        connectToMySQL('ohana').query_db(query, data)

    @staticmethod
    def delete_ride(id):
        query = 'DELETE FROM rides WHERE id = %(id)s'
        data = {'id': id}
        connectToMySQL('ohana').query_db(query, data)
        return