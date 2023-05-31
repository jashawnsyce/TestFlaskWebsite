from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully!', category='success')
            else:
                flash('Incorrect password', category = 'error')
        else:
            flash('No user found', category = 'error')
            
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password01 = request.form.get('password01')
        password02 = request.form.get('password02')
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email taken', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(firstname) < 2:
            flash('Name must be longer than 1 character', category = 'error')
        elif password01 != password02:
            flash('Passwords did not match', category = 'error')
        elif len(password01) < 8:
            flash('Password must be at least 8 characters', category = 'error')
        else:
            flash('Account Created!', category = 'success')
            new_user = User(email=email, first_name=firstname, password = generate_password_hash(password01, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("signup.html")