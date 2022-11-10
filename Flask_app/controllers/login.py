from Flask_app import app
from flask import render_template, redirect, session, request, flash
from Flask_app.models.user import User
from Flask_app import bcrypt

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def r_login():
    if session.get('first_name'):
        data = {
        'first_name': session['first_name'],
        'last_name': session['last_name'],
        'email': session['email']
        }
    else:
        data = {
            'first_name': '',
            'last_name': '',
            'email': ''
        }
    return render_template('login.html', info = data)

@app.route('/add-user', methods = ['POST'])
def f_register():
    if User.val_new_user(request.form):
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        session['user_id'] = User.add_user(data)
        return redirect('/home')
    else:
        session['is_reg'] = True
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/login')

@app.route('/login-user', methods = ['POST'])
def f_login():
    user = User.login(request.form)
    if user == True:
        return redirect('/login')
    else:
        return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')