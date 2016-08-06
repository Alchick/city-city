#coding: utf-8
import re
from datetime import datetime
from sqlalchemy import exc
import os
from flask import request
from models import *
from app import db
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/home/e.sergeev/private_repos/city-city/app/static/filestorage/'
UPLOAD_FOLDER = os.getcwd()+'/app/static/filestorage/' #find more comfortable way!!!!
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'txt', 'jpg', 'png'])
MAX_FILE_SIZE = 200 * 1024 * 1024

#DATABASE OPERATIONS
def save_data_to_db(data):
    try:
        db.session.add(data)
        db.session.commit()
        return ('green',u'Данные успешно добавлены')
    except exc.SQLAlchemyError as ex:
        #check duplicate value error for postgres(pgcode) or for mysql (ex.orig)
        if ex.orig.pgcode == '23505' or ex.orig[0] == 1062:
            print 'Duplicate values', ex
            return ('red', u'Такие данные уже есть')
        print ex
        return ('red','Ошибка обработки')

def save_article(article, file, filename):
    message = save_data_to_db(article)
    if u'Данные успешно добавлены' in message:
        try:
            file.save(os.path.join(UPLOAD_FOLDER, filename))#wery cunfused moment
            return ('green',u'Ваша статья успешно добавлена')
        except Exception as ex:
            db.session.delete(article)
            db.session.commit()
            print 'File-save exception', ex
            return ('red',u'Ошибка обработки')
    else: return message

def check_file_extension(filename):
    if '.' in filename and \
    filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
        return True
    else: return False

def get_articles(): #something wrong with this select
    return db.session.query(articles).filter(articles.article_file.like('%jp%g')).\
    order_by('date desc').limit(10);

def registered_user(login):
    return db.session.query(culture_admins).filter(culture_admins.login == login).first()

def insert_comment(article_id, user_name, email, comment_body):
    comment = users_comment(article_id, user_name, email, comment_body)
    return save_data_to_db(comment)

def add_admin(name, login, email, phone, password):
    admin = culture_admins(name, login, email, phone, password)
    return save_data_to_db(admin)

#database selects
#what exceptions could be when select make
def get_user_comments():
    return db.session.query(users_comment).all()
def get_admin_comments(id): 
    return db.session.query(article_rating).filter_by(article_id = id).all()

def find_article_by_name(article_name):
    return db.session.query(articles).filter_by(article_name=article_name).all()
    
def find_article_by_author(author_name):
    return db.session.query(articles).filter_by(author_name=author_name).all()
    
def get_data_from_db(): #something wrong with this select
    return db.session.query(articles).\
    filter(articles.article_file.like('%jp%g')).\
    order_by('date desc').limit(10);

def registered_user(login):
    return db.session.query(culture_admins).filter(culture_admins.login == login).all()

def get_rating_average(id):
    summ = 0
    ratings = db.session.query(article_rating.rating).filter(article_rating.article_id == id).all()
    for i in ratings:
        summ = summ + i.rating
    try:
        return summ/len(ratings)
    except Exception as ex:
        return 0

def set_rating(rating, article_id, admin_id):
    try:
        rating = db.session.query(article_rating.rating).\
             filter(article_rating.article_id == article_id,\
                    article_rating.admin_id == admin_id).update({'rating':rating})
        db.session.commit()
        return ('green','Рейтинг успешно обновлен')
    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        print ex
        return ('red',u'Произошла ошибка при обновлении рейтинга, попробуйте еще раз')
