from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note, User
from . import db
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    all_notes = Note.query.all()
    all_users = User.query.all()

    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user, notelist=all_notes, userlist=all_users)


@views.route('u/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    all_notes = Note.query.all()
    all_users = User.query.all()

    return render_template("user.html", current_user=current_user, user=user, notelist=all_notes, userlist=all_users)
