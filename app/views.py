#coding: utf-8
import os
from flask import render_template, request, flash, url_for, redirect, g
from app import app
from forms import CreateForm, FindForm, CommentForm
from help_functions import *
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from models import culture_admins

STATUS = {1:[u'На печать', '#008000'], 2:[u'В рассмотрении', ' #FF8C00'], 3:[u'В архив', '#FF0000']}

@app.route('/test.html', methods = ['GET', 'POST'])
def test():
    testform = CreateForm()
    if request.method == 'POST' and testform.validate_on_submit():
        print 'bla'
        print request.form.get('author_name')
        return redirect(url_for('test'))
    return render_template('test.html', form=testform)

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
        flash(('red',u'Пользователь с таким именем не найден'))
        return redirect(url_for('login'))
    if not registered_user(login).check_password(password):
        flash(('red', u'Неверный пароль'))
        return redirect(url_for('login'))
    login_user(registered_user(login), remember = remember_me)
    #flash('Logged is successfully')
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
            flash(('red','Доступ закрыт'))
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
    return redirect(url_for('test'))

@app.route('/index.html')
def index():
    print url_for('static', filename='css/stylemain.css')
    return render_template("index.html")

@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/read.html', methods = ['GET', 'POST'])
def read():
    form = FindForm()
    if request.method == 'POST':
        if request.form.get('article_name'):
            articles =  find_article_by_name(request.form.get('article_name'))
        if request.form.get('author_name'):
            articles = find_article_by_author(request.form.get('author_name'))
        return redirect(url_for('read.html', articles = articles)) #it seems that this is not true way
                                                                 #true way - make render_template with parameters
    articles = get_articles()
    return render_template("read.html",
                           articles = articles,\
                           form = form)

@app.route('/get_file.html', methods = ['GET', 'POST'])
def get_file():
    form = CommentForm()
    admin_comments = None
    if request.args:
        filename = request.args.get('filename') #could it be empty?
        article_name = request.args.get('article_name') #could it be empty?
        author_name = request.args.get('author_name') #could it be empty?
        date = request.args.get('date') #could it be empty?
        id = request.args.get('id')
        status = request.args.get('status') #could it be empty?
        user_comments = get_user_comments()
        if current_user.is_authenticated:
            admin_comments = get_admin_comments(id) #understand how to get admin_name
        rating_average = get_rating_average(id)
        return render_template("get_file.html",\
                               filename = filename,\
                               article_name = article_name,\
                               author_name = author_name,\
                               date = date,\
                               status = int(status),\
                               user_comments = user_comments,\
                               id = id,\
                               enumerate = enumerate,\
                               form = form,\
                               rating_average = rating_average,\
                               admin_comments = admin_comments)
    else: return redirect('read.html')

@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")

@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    form = CreateForm()
    if request.method == 'POST': #and form.validate_on_submit():
        file = request.files['userfile']
        print file
        if file:
            filename = secure_filename(file.filename)
            if not(check_file_extension(file.filename)):
                #flash("u'Неподдерживаемый формат файла'")
                flash(('red','Неподдерживаемый формат файла'))
                return redirect(url_for('create'))
            article = articles(article_name = request.form['article_name'],\
                               author_name = request.form['author_name'],\
                               article_file = filename,\
                               email = request.form['email']) 
            flash(save_article(article, file, filename))
            return render_template('create.html',\
                                    form=form)
        else: 
            flash(('red','Прикрепите файл'))
            return redirect(url_for('create'))

    return render_template("create.html",\
                           form=form)

@app.route('/admin.html', methods = ['GET', 'POST'])
@login_required
def admin():
    records = get_article_from_db()
    return render_template('admin.html',\
                            records = records)

@app.route('/set_comment.html', methods = ['POST'])
def set_comment():
    art_id = request.form.get('art_id')
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    #set_comment_message = insert_comment(art_id,name,email,comment))
    #set_rating_message = set_rating(rating, art_id, current_user.id)
    print current_user.__dict__
    result_message = 'set_rating_message'
    return result_message


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
