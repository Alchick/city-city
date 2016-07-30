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
UPLOAD_FOLDER = '/home/e.sergeev/culture-city/app/static/filestorage/'
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'txt', 'jpg', 'png'])
MAX_FILE_SIZE = 200 * 1024 * 1024

def save_request_data(request):
    try:
        file = request.files['userfile']
        filename = secure_filename(file.filename)
        print filename
        if not(file):
            return 'You send no file'
        #if not(check_file_size(file)):
        #    return 'File size is too big'
        elif not(check_file_extension(file.filename)):
            return 'Unsupported file extension'
        else:
            record = articles(article_name = request.form['article_name'],\
                              author_name = request.form['author_name'],\
                              article_file = filename,\
                              date = datetime.today().strftime("%d-%m-%Y %H:%M:%S"),\
                              email = request.form['email'])
#when table is lock, happened nothing. operations wait their turn. So when it is, operation make
#Затрет текущий файл статьи, если такой файл уже есть. Т.е. статья по сути пропадет
            file.save(os.path.join(UPLOAD_FOLDER, filename))#wery cunfused moment
            db.session.add(record)
            db.session.commit()
            return 'Succes'
    except exc.SQLAlchemyError as ex:
#        if ex.orig.pgcode == '23505':
        print 'database exception', ex
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        db.session.rollback()
        return ex.orig.message
        #return 'Enternal server Error, write system administrator'
    except Exception as ex:
        print 'Exception', ex, type(ex)
        return 'Enternal server Error, write system administrator'

def check_file_size(file):
#    return ['File size is too big' if len(file.read()) > MAX_FILE_SIZE #this construction?
    if len(file.read()) < MAX_FILE_SIZE: #get +1 byte to for more something, read habra about it Look
        return True
    else: return False

def check_file_extension(filename):
    if '.' in filename and \
    filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
        return True
    else: return False

def regexp(text, pattern):
    result = re.search(pattern, text)
    if result:
        return True
    else: return False

def get_data_from_db(): #something wrong with this select
    return db.session.query(articles).\
    filter(articles.article_file.like('%')).\
    order_by('date desc').limit(10);


def registered_user(login):
    return db.session.query(culture_admins).filter(culture_admins.login == login).first()

def insert_comment(article_id, user_name, email, comment_body):
    comment = users_comment(article_id, user_name, email, comment_body)
    db.session.add(comment)
    db.session.commit()
    return "Success"

def add_admin(name, login, email, phone, password):
    admin = culture_admins(name, login, email, phone, password)
    db.session.add(admin)
    db.session.commit()
    return "success add"

def get_comments():
    return db.session.query(users_comment).all() 

