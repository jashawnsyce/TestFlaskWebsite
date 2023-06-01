from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category = 'error')
        else:
            flash('No user found', category = 'error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password01 = request.form.get('password01')
        password02 = request.form.get('password02')
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email taken', category='error')
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username taken', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 4 characters', category = 'error')
            elif len(username) < 3:
                flash('Name must be longer than 2 character', category = 'error')
            elif password01 != password02:
                flash('Passwords did not match', category = 'error')
            elif len(password01) < 8:
                flash('Password must be at least 8 characters', category = 'error')
            else:
                new_user = User(email=email, username=username, password = generate_password_hash(password01, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
                flash('Account Created!', category = 'success')

    return render_template("signup.html", user=current_user)