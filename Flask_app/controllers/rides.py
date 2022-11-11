from Flask_app import app
from flask import render_template, redirect, session, request, flash
from Flask_app.models.user import User
from Flask_app.models.ride import Ride

@app.route('/dashboard')
def dashboard():
    if session.get('user_id') == None:
        return redirect('/logout')
    user = User.get_user_from_id(session.get('user_id'))
    rides = Ride.get_all_rides()
    return render_template('/dashboard.html', user = user, rides = rides)

# Ride Requests
@app.route('/request_ride')
def f_request_ride():
    if session.get('user_id') == None:
        return redirect('/logout')
    print(session.get('destination'))
    if session.get('destination') == None:
        data = {
            'destination': '',
            'pick_up': '',
            'date': '',
            'details': ''
        }
    else:
        data = {
            'destination': session['destination'],
            'pick_up': session['pick_up'],
            'date': session['date'],
            'details': session['details']
        }
    return render_template('ride_request.html', data = data, rider_id = session['user_id'])

@app.route('/request-ride', methods = ['POST'])
def r_request_ride():
    if Ride.val_ride(request.form):
        Ride.add_ride(request.form)
        return redirect('/dashboard')
    else:
        return redirect('/request_ride')

#Edit ride
@app.route('/edit_ride/<int:id>')
def f_edit_ride(id):
    if session.get('user_id') == None:
        return redirect('/logout')
    ride = Ride.get_ride_from_id(id)
    if session.get('user_id') == ride.rider_id:
        return render_template('edit_ride.html', ride = ride)
    return redirect('/dashboard')


@app.route('/edit-ride/<int:id>', methods = ['POST'])
def r_edit_ride(id):
    if Ride.val_ride(request.form):
        Ride.edit_ride(request.form)
        return redirect('/dashboard')
    else:
        return redirect('/edit_ride/' + str(id))


#Change drivers
@app.route('/accept-ride/<int:id>')
def r_accept_ride(id):
    data = {
        'driver_id': session.get('user_id'),
        'id': id
    }
    Ride.add_driver(data)
    return redirect('/dashboard')

@app.route('/cancel-ride/<int:id>')
def r_remove_driver(id):
    data = {
        'id': id
    }
    Ride.remove_driver(data)
    return redirect('/dashboard')

#Delete
@app.route('/delete-ride/<int:id>')
def r_delete_ride(id):
    ride = Ride.get_ride_from_id(id)
    if session.get('user_id') == None:
        return redirect('/logout')
    elif session['user_id'] == ride.rider_id:
        Ride.delete_ride(id)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

#Details
@app.route('/details/<int:id>')
def f_ride_details(id):
    ride = Ride.get_ride_from_id(id)
    if session.get('user_id') == ride.driver_id or session.get('user_id') == ride. rider_id:
        user = User.get_user_from_id(session['user_id'])
        return render_template('details.html', ride = ride, user = user)
    else:
        return redirect('/dashboard')
