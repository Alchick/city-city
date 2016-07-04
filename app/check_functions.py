import re
from datetime import datetime
from sqlalchemy import exc
import os
from flask import request
from models import Articles
from app import db
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/e.sergeev/private_repos/city-city/app/static/filestorage/'
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'txt'])
MAX_FILE_SIZE = 200 * 1024 * 1024

def save_request_data(request):
    try:
        file = request.files['userfile']
        if not(file):
            return 'You send no file'
        if not(check_file_size(file)):
            return 'File size is too big'
        elif not(check_file_extension(file.filename)):
            return 'Unsupported file extension'
        elif regexp(request.form['article_name'], r'[^a-zA-Z\s]'):
            return 'Wrong article_name'
        elif regexp(request.form['author_name'], r'[^a-zA-Z\s]'):
            return('wrong author_name')
        elif regexp(request.form['email'], r'@\w+'):#do not check. why?
            return('wrong email')
        else:
            filename = secure_filename(file.filename)
            record = Articles(article_name = request.form['article_name'],\
                                     author_name = request.form['author_name'],\
                                     file_name = filename,\
                                     date = datetime.today(),\
                                     email = request.form['email'])
#when table is lock, happened nothing. operations wait their turn. So when it is, operation make
            file.save(os.path.join(UPLOAD_FOLDER, filename))#wery cunfused moment
            db.session.add(record)
            db.session.commit()
            return 'Succes'
    except exc.SQLAlchemyError as ex:
        print ex
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        db.session.rollback()
        return 'Enternal server Error, write system administrator'
    except Exception as ex:
        print ex
        return 'Enternal server Error, write system administrator'

def check_file_size(file):
#    return ['File size is too big' if len(file.read()) > MAX_FILE_SIZE #this construction?
    file_bytes = len(file.read())
    if file_bytes < MAX_FILE_SIZE: #get +1 byte to for more something, read habra about it Look
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

def get_data_from_db():
    return db.session.query(Articles).\
    filter(Articles.file_name.like('%jpg')).\
    order_by('date desc').limit(10);

