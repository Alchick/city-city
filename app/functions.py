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
from ServerExceptions import WrongExtensionException, WrongFieldNameException
import re
OK_STATUS = 0
PROBLEM_STATUS = 1
SIZE = 200 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'tiff', 'png', 'txt', 'jpg'])
UPLOAD_FOLDER = '/home/e.sergeev/culture-city/app/static/filestorage/'
#UPLOAD_FOLDER = '/home/e.sergeev/private_repos/city-city/app/static/filestorage/'

def allowed_file(filename):
    if '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
        return filename
    else: raise WrongExtensionException
        


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
        print 'wrong request atributes'
        return "Wrong request atributes"
    except WrongExtensionException:
        return 'Wrong file extension'
    except WrongFieldNameException:
        return 'Wrong field name'
    except Exception as ex:   #what type of exception?
        print 'other exception', ex, type(ex)
        return "Server Error, please write system administrator"

def save_file(file):
    try:
        filename = secure_filename(allowed_file(file.filename)) #what happend if wrong filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return OK_STATUS
    except RuntimeError:
        print 'RuntimeError'
        raise RuntimeError #Wrong file extension
    except RequestEntityTooLarge:
        raise RequestEntityTooLarge #big file size
    except WrongExtensionException:
        raise WrongExtensionException
    except Exception as ex:
        print 'Exception while save file', ex #wrong raise exseption
        raise Exception #another reasons for error while save file

def save_data_to_db(request):#field can be empty?
    try:        
        if regexp(request.form['article_name']) and \
           regexp(request.form['author_name']):
                   
            record = models.Articles(article_name = request.form['article_name'],\
                                author_name = request.form['author_name'],\
                                file_name = request.files['userfile'].filename,\
                                date = datetime.today(),\
                                email = request.form['email'])
            db.session.add(record)
            db.session.commit()
        else: raise WrongFieldNameException
#when table is lock, happened nothing. operations wait their turn. So when it is, operation make
        return OK_STATUS
    except DataError as ex:
        db.session.rollback()
        os.remove(UPLOAD_FOLDER + request.files['userfile'].filename)
        print type(ex)
        print ex.args
        print ex
        print 'Wrong data type'
        
        raise DataError 
        #wrong metadata
    #except ProgrammingError as ex: #do it realy need?
    #    print "wrong field"
    #    raise ProgrammingError
    except Exception as ex:
        db.session.rollback()
        os.remove(UPLOAD_FOLDER + request.files['userfile'].filename)
        print 'Exception while save data to ex', ex
        #raise Exception, 'Execuption while save data'
        #database is lock
        #another transaction
        #tables does not exists
        

def check_file_size(file):
    file_bytes = len(file.read())
    if file_bytes > SIZE:
       return False
    else: return True

def get_data_from_db():
    return db.session.query(models.Articles).filter(models.Articles.file_name.like('%jpg')).order_by('date desc').limit(10);
    
def regexp(text):
    pattern = re.compile('[^a-zA-Z\s]')
    rezult = re.search(pattern, text)
    if rezult:
        return False
    else: return True

