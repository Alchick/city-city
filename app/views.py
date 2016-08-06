#coding: utf-8
import os
from flask import render_template, request, flash, url_for, redirect, g
from app import app
from forms import *
from help_functions import *
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from models import culture_admins

STATUS = {1:[u'На печать', '#008000'], 2:[u'В рассмотрении', ' #FF8C00'], 3:[u'В архив', '#FF0000']}

@app.route('/test.html')
def test():
    return render_template('test.html')

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
    findForm = MainForm()
    if request.method == 'POST':
        if request.form.get('article_name'):
            records =  find_article_by_name(request.form.get('article_name'))
        if request.form.get('author_name'):
            records = find_article_by_author(request.form.get('author_name'))
        return redirect(url_for('read.html', records = records)) #it seems that this is not true way
                                                                 #true way - make render_template with parameters
#        return render_template("read.html",
#                           records = records,\
#                           findForm = findForm)
    records = get_data_from_db()
    return render_template("read.html",
                           records = records,\
                           findForm = findForm)

@app.route('/get_file.html', methods = ['GET', 'POST'])
def get_file():
    commentForm = MainForm(Form)
    if request.args:
        filename = request.args.get('filename') #could it be empty?
        article_name = request.args.get('article_name') #could it be empty?
        author_name = request.args.get('author_name') #could it be empty?
        date = request.args.get('date') #could it be empty?
        id = request.args.get('id')
        status = request.args.get('status') #could it be empty?
        comments = get_comments() 
        return render_template("get_file.html",\
                               filename = filename,\
                               article_name = article_name,\
                               author_name = author_name,\
                               date = date,\
                               status = int(status),\
                               comments = comments,\
                               id = id,
                               enumerate = enumerate,\
                               commentForm = commentForm)
    else: return redirect('read.html')

@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")

@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    Sendform = MainForm()
    if request.method == 'POST': #and form.validate_on_submit():
        if file in request.files:
            flash(save_request_data(request))
            return render_template('create.html',\
                                    Sendform=Sendform)
        else: 
            flash('You send no file')
            return redirect(url_for('create'))

    return render_template("create.html",\
                           Sendform=Sendform)

@app.route('/admin.html', methods = ['GET', 'POST'])
@login_required
def admin():
    records = get_data_from_db()
    return render_template('admin.html',\
                            records = records)

@app.route('/set_comment.html', methods = ['POST'])
def set_comment():
    flash(insert_comment(request.form.get('art_id'),\
                         request.form.get('name'),\
                         request.form.get('email'),\
                         request.form.get('comment')))
    return "Normik"



#ERRORS
@app.errorhandler(413)
def EntityTooLarge(error):
    return render_template("error.html", error = 413), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error = 404), 404

@app.errorhandler(500)
def page_not_found(error):
    db.session.rollback()
    return render_template("error.html", error = 500), 500

@app.before_request
def before_request():
    g.status = STATUS
