import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://'+ 'postgres:postgres@localhost:5432/city_city'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
