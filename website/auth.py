
from flask import Blueprint, flash,render_template,request,redirect,url_for
auth=Blueprint('auth',__name__)
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_required,logout_user,login_user,current_user
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect',category='error')
        else:
            flash('Email is not valid',category='error')

    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist',category='error')
        elif len(email)<4:
            flash('email should be greater than 3 characters',category="error")
        elif len(firstName)<2:
            flash('firstName should be greater than 2 chracters',category='error')
        elif (password1!=password2):
            flash("password doesn't match", category='error')
        elif len(password1)<7:
            flash("password must be of atleast 7 characters",category='error')
        else:

            new_user=User(email=email,first_name=firstName,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("User add sucessfully!",category='success')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html',user=current_user)





