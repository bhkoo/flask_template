from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

# Routing for login page
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email = email).first()
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again.', category = 'error')
        else:
            flash(list(form.errors.values())[0][0], category = 'error')
    return render_template('login.html', user = current_user, form = form)

# Routing for logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Routing for signup page
@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data

            new_user = User(email = email, name = name, password = generate_password_hash(password, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account created', category = 'success')
            return redirect(url_for('views.home'))
        else:
            flash(list(form.errors.values())[0][0], category = 'error')

    return render_template('signup.html', user = current_user, form = form)
