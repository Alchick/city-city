import os
from app import app
#Options for forms, csfr protection
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
#configuration for saving data
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'doc', 'docx', 'tiff', 'png'])
#change path to more universal
UPLOAD_FOLDER = '/home/e.sergeev/private_repos/city-city/app/static/filestorage/'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
'''
database configuration
SQL-LITE database_URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.file_name')

POSTGRESQL database_URI
SQLALCHEMY_DATABASE_URI = 'postgresql://'+ 'username:password@host:port/database.name')

MYSQL database_URI
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/database.name')
'''
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/city_city'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')





