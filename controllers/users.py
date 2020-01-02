# -*- coding: utf-8 -*-

"""Web handler for user account related pages."""

from flask import Blueprint, redirect, render_template, request, session

from models.user.error import UserError
from models.user.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Attempts to register a new user account."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return email
        except UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Attempts to log a user in."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.validate_login(email, password):
                session['email'] = email
                return email
        except UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route('/logout')
def logout():
    """Logs the user out."""
    session['email'] = None
    return redirect('login')
