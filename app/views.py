#coding: utf-8
import os
from flask import render_template, request, flash, url_for, redirect
from app import app
from forms import *
from check_functions import *
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from models import culture_admins

#LOGIN VIEWS
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    remember_me = False
    if request.form.get('remember_me'):
        remember_me = True
    if registered_user(login) is None:
        flash('Username is invalid')
        return redirect(url_for('login'))
    if not registered_user(login).check_password(password):
        flash('Invalid password')
        return redirect(url_for('login'))
    login_user(registered_user(login), remember = remember_me)
    flash('Logged is successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        if current_user.login == 'root':
            return render_template('register.html', form=form)
        else:
            flash('permission denied')
            return redirect(url_for('login'))
    if request.method == 'POST' and form.validate_on_submit:
        name = request.form.get('name')
        login = request.form.get('login')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        flash(add_admin(name, login, email, phone, password))
        return render_template(url_for('index'))
#PAGES VIEWS
@app.route('/')
def main():
    return redirect(url_for('index'))

@app.route('/index.html')
def index():
    print url_for('static', filename='css/stylemain.css')
    return render_template("index.html")

@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/read.html', methods = ['GET', 'POST'])
def read():
    if request.method == 'POST':
        a = request.form.get('article_find')
        print a
        records = get_data_from_db()
        return render_template("read.html",
                           records = records)
    records = get_data_from_db()
    return render_template("read.html",
                           records = records)

@app.route('/get_file.html', methods = ['GET', 'POST'])
def get_file():
    comments = None
    if request.args:
        filename = request.args.get('filename') #could it be empty?
        article_name = request.args.get('article_name') #could it be empty?
        author_name = request.args.get('author_name') #could it be empty?
        date = request.args.get('date') #could it be empty?
        id = request.args.get('id')
        passi = request.args.get('passi') #could it be empty?
        if current_user.is_authenticated:
            comments = get_comments() 
        return render_template("get_file.html",\
                               filename = filename,\
                               article_name = article_name,\
                               author_name = author_name,\
                               date = date,\
                               passi = passi,\
                               comments = comments,\
                               id = id,
                               enumerate = enumerate)
    else: return redirect('read.html')

@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")

@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    form = ArticleForms()
    if request.method == 'POST' and form.validate_on_submit():
        flash(save_request_data(request))
        return render_template('create.html',\
                                form=form)
    return render_template("create.html",\
                           form=form)

@app.route('/admin.html', methods = ['GET', 'POST'])
@login_required
def admin():
    records = get_data_from_db()
    return render_template('admin.html',\
                            records = records)

@app.route('/set_comment.html', methods = ['POST'])
def set_comment():
    print request.form.get('comment')
    return 'Normik'



#ERRORS
@app.errorhandler(413)
def EntityTooLarge(error):
    return render_template("error.html", error = 413), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error = 404), 404


