from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

users = [
'Jay',
'Kilien',
'Link',
'Sheik'
]


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text='test string', users=users)

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

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(firstname) < 2:
            flash('Name must be longer than 1 character', category = 'error')
        elif password01 != password02:
            flash('Passwords did not match', category = 'error')
        elif len(password01) < 8:
            flash('Password must be at least 8 characters', category = 'error')
        else:
            flash('Account Created!', category = 'success')
            #add user to database

    return render_template("signup.html")