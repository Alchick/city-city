#coding=utf-8
import os
MAX_CONTENT_LENGTH = 100 * 1024 * 1024
USE_X_SENDFILE = True #test how to send cache files to browser
SERVER_NAME = 'culture-city.rf'
SEND_FILE_MAX_AGE_DEFAULT = '43200'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
#check upload folder before start
UPLOAD_FOLDER = BASEDIR + '/static/filestorage/'
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'jpg','doc', 'docx', 'txt'])
CSRF_ENABLED = True
SECRET_KEY = 'Ooshaev6ie8eeRok'

#database configuration
DATABASE_USER = 'postgres'
DATABASE_NAME = 'culture_city'
DATABASE_HOST = 'localhost'
DATABASE_PASSWORD = 'postgres'
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:5432/{3}'.format(\
                                                              DATABASE_USER,\
                                                              DATABASE_PASSWORD,\
                                                              DATABASE_HOST,\
                                                              DATABASE_PASSWORD)
SQLALCHEMY_BINDS = {
    'culture_city-mysql':'mysql://{0}:{1}@{2}:5432/{3}'.format(\
                                                        DATABASE_USER,\
                                                        DATABASE_PASSWORD,\
                                                        DATABASE_HOST,\
                                                        DATABASE_PASSWORD)
    }   
'''
database configuration
SQL-LITE database_URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.file_name')

POSTGRESQL database_URI
SQLALCHEMY_DATABASE_URI = 'postgresql://'+ 'username:password@host:port/database.name')

MYSQL database_URI
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/database.name')
'''
#connection timeout, default 10
#SQLALCHEMY_POOL_TIMEOUT
#remove connection after timeout set in this conf
#SQLALCHEMY_POOL_RECYCLE
#size of connection pool
#SQLALCHEMY_POOL_SIZE
#whe this paramet is true, flask watch database operation
#SQLALCHEMY_RECORD_QUERIES = True 
#send database error messages to STDERR stream (need to check)
#SQLALCHEMY_ECHO = True
#use exceptions as exceptions, not return http 500 error code
#TRAP_HTTP_EXCEPTIONS
#when set to true, flask automatic restart template if it was change. Alrith work when debug mod is disable (in debug mod this option in True by default)
#EXPLAIN_TEMPLATE_LOADING = True

