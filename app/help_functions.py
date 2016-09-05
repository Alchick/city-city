#coding: utf-8
import re
from sqlalchemy import exc, desc
import os
from flask import request
from models import *
from app import db
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from app import mail
from flask.ext.mail import Message
from threading import Thread

OK_STATUS = 0
PROBLEM_STATUS = 1

def send_email(subject, sender, recipients, text_body, html_body=None):
    try:
        msg = Message(subject, sender=sender, recipients = recipients)
        msg.body = text_body
        msg.html = html_body
        assync_send = Thread(target = mail.send, args = [msg])
        assync_send.setDaemon(True)
        assync_send.start()
    except Exception as ex:
        print 'Unable to send mail, watch logs', ex
        return PROBLEM_STATUS
    
#DATABASE OPERATIONS
#SAVE,INSERT,UPDATE OPERATIONS
def save_data_to_db(data):
    try:
        db.session.add(data)
        db.session.commit()
        return ('green','Данные успешно добавлены')
    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        #check duplicate value error for postgres(pgcode) or for mysql (ex.orig)
        if ex.orig.pgcode == '23505' or ex.orig[0] == 1062:
            if 'article_file' in ex.message:
                return ('red','Файл с таким названием уже есть в базе данных')
            if 'email' in ex.message:
                return ('red','Такой электронный адрес уже есть в базе данных')
            if 'article_name' in ex.message:
                return ('red','Статья с таким называние уже есть в базе данных')
            if 'unique_rating' in ex.message:
                return ('GoldenRod','Ваша оценка данной статьи уже учтена')
            print ex
            return ('red','Ошибка обработки, повторите познее или напишите нам')
        print ex
        return ('red','Ошибка обработки, повторите познее или напишите нам')

def save_article(article, file, filename):
    message = save_data_to_db(article)
    if 'green' in message:
        try:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return ('green','Ваша статья успешно добавлена')
        except Exception as ex:
            db.session.delete(article)
            db.session.commit()
            print 'File-save exception', ex
            return ('red','Ошибка обработки, повторите познее или напишите нам')
    else: return message

def insert_comment(article_id, user_name, email, comment_body):
    comment = users_comment(article_id, user_name, email, comment_body)
    return save_data_to_db(comment)

def add_admin(name, login, email, phone, password):
    admin = culture_admins(name, login, password, email, phone)
    return save_data_to_db(admin)

def set_rating(rating, article_id, admin_id, comment):
    rating = article_rating(article_id, admin_id, comment, rating)
    return save_data_to_db(rating)

def update_article_status(article_id, new_status):
    try:
        update = db.session.query(articles).filter(articles.id == article_id).update({'status':int(new_status)})
        db.session.commit()
    except Exception as ex:
        print ex
        db.session.rollback()

#SELECT OPERATIONS
#ARTICLES SELECT OPERATIONS
def get_articles(): #something wrong with this select
    try:
        result =  db.session.query(articles.id, articles.author_name, articles.article_name,articles.date,articles.status).\
        filter(articles.article_file.like('%jp%g')).\
        order_by('date desc').limit(10);
    except Exception as ex:
        result = ('red', 'Произошла ошибка при запросе статей. Попробуйте позднее')
    return result

def get_article(id):
    try:
        result = db.session.query(articles.id, articles.author_name, articles.article_name,articles.date,articles.status,\
        articles.article_file).\
        filter(articles.id == id).first()
    except Exception as ex:
        result = ('red', 'Произошла ошибка при запросе статьи. Попробуйте позднее')
    return result
def find_article_by_name(article_name):
    try:
        result = db.session.query(articles.id, articles.author_name, articles.article_name,articles.date,articles.status).\
    filter_by(article_name=article_name).all()
    except Exception as ex:
        result = ('red', 'Произошла ошибка при поиске. Попробуйте позднее')
    return result

def find_article_by_author(author_name):
    try:
        result = db.session.query(articles.id, articles.author_name, articles.article_name,articles.date,articles.status).\
        filter_by(author_name=author_name).all()
    except Exception as ex:
        result = ('red', 'Произошла ошибка при поиске. Попробуйте позднее')
    return result 

    
#COMMENTS SELECT OPERATIONS
def get_user_comments(id):
    try:
        result = db.session.query(users_comment.user_name, users_comment.date, users_comment.comment_body).\
        filter_by(article_id = id).order_by(users_comment.date.desc()).all()
    except Exception as ex:
        result = ('red', 'Произошла ошибка при запрос комментариев. Попробуйте позднее')
    return result

def get_admin_comments(id):
    try: 
        result = db.session.query(article_rating.rating,article_rating.date, article_rating.comment).\
        filter_by(article_id = id).join(culture_admins).add_columns(culture_admins.login).order_by(article_rating.date.desc()).all()
    except Exception as ex:
        result = ('red', 'Произошла ошибка при запросе комментариев. Попробуйте позднее')
    return result
#OTHER OPERATIONS
def registered_user(login):
    return db.session.query(culture_admins).filter(culture_admins.login == login).first()

def get_rating_average(id):
    try:
        summ = 0
        ratings = db.session.query(article_rating.rating).filter(article_rating.article_id == id).all()
        for i in ratings:
            summ = summ + i.rating
        try:
            return summ/len(ratings)
        except Exception as ex:
            return 0
    except Exception as ex:
        return PROBLEM_STATUS

#OTHER FUNCTIONS
def check_file_extension(filename):
    if '.' in filename and \
    filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
        return True
    else: return False
