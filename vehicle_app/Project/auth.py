from flask import Blueprint, render_template, request,redirect,url_for,flash,session
from flask_login import login_user,logout_user,login_required,current_user
from .models import User
from . import db
import os
import re

auth = Blueprint('auth',__name__)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")

        username_exists = User.query.filter_by(username=username).first()

        if len(password)<4:
            flash('Password must be greater than 4 characters',category='error')
            return render_template('signup.html')


        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        patterns = './?@#$%^&*()'
        has_patterns = any(c in patterns for c in password)



        if has_upper and has_lower and has_digit and has_patterns and len(password) >= 8:
            if username_exists:
                print("Username already exists")
                flash('username already exists',category='error')
                return render_template('signup.html')
            else:
                newUser = User(name=name,username=username,password=password,   role=1)
                db.session.add(newUser)
                db.session.commit()

                flash('account created',category='success')

                return render_template('login.html',user=current_user)
        else:
            flash('passowrd should be of 8 length',category='error')
            return render_template('signup.html')
    else:
        return render_template('signup.html')


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                if user.role == 0:
                    print('admin logged in')
                    login_user(user)
                    return redirect('/admin_dashboard')
                else:
                    login_user(user)
                    return redirect('/customer_dashboard')
            else:
                flash('Incorrect password',category='error')
                return render_template('login.html')
        else:
            flash('Username does not exist',category='error')
            return render_template('login.html')
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

