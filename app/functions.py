#functions module
import os
from flask import request
from werkzeug.utils import secure_filename
from app import db
import models
from werkzeug.exceptions import RequestEntityTooLarge
#from app import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from datetime import datetime
from sqlalchemy.exc import DataError
OK_STATUS = 0

ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'tiff', 'png', 'txt', 'jpg'])
UPLOAD_FOLDER = '/home/e.sergeev/private_repos/city-city/app/static/filestorage/'

def allowed_file(filename):
    if '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
        return filename
    else: raise RuntimeError #change exception class


def save_request_data(request):
    try:
        if save_file(request.files['userfile']) == OK_STATUS and \
        save_data_to_db(request) == OK_STATUS:
            return "Success"
    except RuntimeError:
        return "Wrong file extension"
    except RequestEntityTooLarge:
        return "File is too big" #flask return 413 page error, not good
    except DataError:
        return "Wrong file atributes"
    except Exception as ex:   #what type of exception?
        print ex
        return "Server Error, please write system administrator"

def save_file(file):
    try:
        filename = secure_filename(allowed_file(file.filename)) #what happend if wrong filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return OK_STATUS
    except RuntimeError:
        raise RuntimeError #Wrong file extension
    except RequestEntityTooLarge:
        raise RequestEntityTooLarge #big file size
    except Exception as ex:
        print 'Exception while save file', ex #wrong raise exseption
        raise Exception #another reasons for error while save file

def save_data_to_db(request):#field can be empty?
    try:        
        
        record = models.Articles(article_name = request.form['article_name'],\
                                author_name = request.form['author_name'],\
                                file_name = request.files['userfile'].filename,\
                                date = datetime.today(),\
                                email = request.form['email'])
        db.session.add(record)
        db.session.commit()
        return OK_STATUS
    except DataError:
        db.session.rollback()       #is it all?
        raise DataError #wrong metadata
    #except ProgrammingError as ex: #do it realy need?
    #    print "wrong field"
    #    raise ProgrammingError
    except Exception as ex:
        print 'Exception while save data to ex', ex
        raise Exception
        #database is lock
        #another transaction
        #tables does not exists
        



def get_data_from_db():
    return models.Articles.query.all()
    

