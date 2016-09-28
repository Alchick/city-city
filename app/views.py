#coding: utf-8
import os
from flask import render_template, request, flash, url_for, redirect, g, json
from app import app, mail
from flask.ext.mail import Message
from forms import CreateForm, FindForm, CommentForm, LoginForm
from help_functions import *
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import culture_admins
from flask import jsonify
from datetime import datetime
import sys
import logging, logging.config
reload(sys)
sys.setdefaultencoding('utf-8')

view_log = logging.getLogger('view_func')

STATUS = {1:[u'На печать', '#008000'], 2:[u'В рассмотрении', ' #FF8C00'], 3:[u'В архиве', '#FF0000']}

#@app.route('/test.html', methods = ['GET', 'POST'])
#def test():
#    text = '''
#        This is wartime, this is our time
#        We won't be denied
#    '''
#    testform = CreateForm()
#    data = datetime.utcnow()
#    if request.method == 'POST':
#        print request.form
#    return render_template('test.html', form=testform, text=text, data = data)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',\
                               form = form) #return static page login
    login = request.form.get('login')
    password = request.form.get('password')
    remember_me = False
    if request.form.get('remember_me'):
        remember_me = True
    if not(registered_user(login)):
        flash(('red','Неверное имя пользователя'))
        view_log.info('unknown login - ' + login)
        return render_template('login.html',\
                                form=form)
    if not registered_user(login).check_password(password):
        flash(('red', 'Неверный пароль'))
        view_log.info('unknown password  for login - ' + login)
        return render_template('login.html',\
                                form=form)
    login_user(registered_user(login), remember = remember_me)
    view_log.info(login + ' authorized success')
    #flash('Logged is successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    view_log.info(current_user.login + ' logout')
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
            view_log.warning('attempt to get access for register user')
            return redirect(url_for('login'))
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        login = request.form.get('login')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        flash(add_admin(name, login, email, phone, password))
        view_log.info('check registration for user ' + login)
        return render_template(url_for('index'))

#PAGES VIEWS
@app.route('/')
def main():
    return redirect(url_for('index'))

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/about.html')
def about():
    return render_template("about.html")


'''
functions:
    get_articles()
    find_article_by_name()
    find_article_by_author()
    return article in list with elements:
article.id - [0]
article.author_name - [1]
article.article_name - [2]
article.date - [3]
article.status - [4]
'''
@app.route('/read.html', methods = ['GET', 'POST'])
def read():
    form = FindForm()
    articles = None
    if request.method == 'POST':
        if request.form.get('article_name'):
            articles =  find_article_by_name(request.form.get('article_name'))
        if request.form.get('author_name'):
            articles = find_article_by_author(request.form.get('author_name'))
        if not(request.form.get('article_name')) and not(request.form.get('author_name')):
            articles = get_articles()
            view_log.info('get articles in post request')
        return render_template('read.html',\
                                 articles = articles,\
                                 form=form) 
    articles = get_articles()
    return render_template("read.html",\
                           articles = articles,\
                           form = form)

'''
    get_article() function return article in format:
article.id - [0]
article.author_name - [1]
article.article_name - [2]
article.date - [3]
article.status - [4]
article.article_filename - [5]
'''
@app.route('/get_article.html', methods = ['GET', 'POST'])
def get():
    form = CommentForm()
    admin_comments = None
    if request.args:
        id = request.args.get('id')
        article = get_article(id)
        status = request.args.get('status')
        user_comments = get_user_comments(id)
        if current_user.is_authenticated:
            admin_comments = get_admin_comments(id)
        rating_average = get_rating_average(id)
	return render_template("get_article.html",\
                               article = article,
                               form = form,\
                               rating_average = rating_average,\
                               admin_comments = admin_comments)
    else: return redirect('read.html')

@app.route('/contacts.html')
def contact():
    if request.method == 'POST':
        name = request.form.get('name').upper() + '\n'
        mail = request.form.get('email').upper() + '\n'
        opinion = request.form.get('opinion') + '\n'
        try:
            with open('user_opinion.txt', 'a') as f:
                f.write(name+mail+opinion)
            f.close()
            view_log.info('add new opinion')
        except Exception as ex:
            view_log.error('error occured while add new opinion')
            view_log.error(ex)
            view_log.error(name)
            view_log.error(mail)
            view_log.error(opinion)
    return render_template("contacts.html") #static page

@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    form = CreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['userfile']
        if file:
            filename = secure_filename(file.filename)
            if not(check_file_extension(file.filename)):
                flash(('red','Неподдерживаемый формат файла'))
                view_log.error('Неподдерживаемый формат файла')
                view_log.error(filename)
                return redirect(url_for('create'))
            view_log.info('check new article ' + request.form['article_name'] + 'by '+ request.form['author_name'])
            article = articles(article_name = request.form['article_name'],\
                               author_name = request.form['author_name'],\
                               article_file = filename,\
                               email = request.form['email'])
            flash(save_article(article, file, filename))
            #add email notification about add new article
            return render_template('create.html',\
                                    form=form)
        else: 
            flash(('red','Прикрепите файл'))
            return redirect(url_for('create'))

    return render_template("create.html",\
                           form=form)

@app.route('/set_comment.html', methods = ['POST'])
def set_comment():
    art_id = request.form.get('art_id')
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    if current_user.is_authenticated:
        rating = request.form.get('rating')
        message = set_rating(rating, art_id, current_user.id, comment)
        view_log.info(current_user.login + ' set rating for article '+ art_id)
    else:
        message = insert_comment(art_id,name,email,comment)
        view_log.info('add new comment for article '+ art_id)
    return jsonify(color = message[0],\
                   message_words = message[1])



@app.route('/get_comment', methods = ['GET'])
def get_comment():
    id = request.args.get('id')
    i = int(request.args.get('iter'))
    user_comments = get_user_comments(id)[i:]
    admin_comments = get_admin_comments(id)[i:]
    return jsonify(user_comments = user_comments[0:3], user_length = len(user_comments),\
                   admin_comments = admin_comments[0:3], admin_length = len(admin_comments))
    
#ERRORS
#40x errors
@app.errorhandler(413)
def EntityTooLarge(error):
    view_log.warning('too big file size')
    view_log.warning(error)
    return render_template("error.html", error = error) #entetity too large

@app.errorhandler(400)
def page_not_found(error):
    return render_template("error.html", error = error) #wrong request(syntax)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error = error) #not found


@app.errorhandler(408)
def page_not_found(error):
    return render_template("error.html", error = error) #request timeout

@app.errorhandler(410)
def page_not_found(error):
    return render_template("error.html", error = error) #resource was deleted


#50x errors
@app.errorhandler(500)
def page_not_found(error):
    view_log.error('500_error')
    view_log.error(error)
    db.session.rollback()
    return render_template("error.html", error = error) #internal server error

@app.errorhandler(501)
def page_not_found(error):
    view_log.error('501_error')
    view_log.error(error)
    db.session.rollback()
    return render_template("error.html", error = error) #not realized

@app.errorhandler(502)
def page_not_found(error):
    view_log.error('502_error')
    view_log.error(error)
    db.session.rollback()
    return render_template("error.html", error = error) #bad gateway

@app.errorhandler(503)
def page_not_found(error):
    view_log.error('503_error')
    view_log.error(error)
    db.session.rollback()
    return render_template("error.html", error = error) #service unavailable

@app.errorhandler(504)
def page_not_found(error):
    view_log.error('504_error')
    view_log.error(error)
    db.session.rollback()
    return render_template("error.html", error = error) #gateway timeout


####
@app.before_request
def before_request():
    g.status = STATUS
