#coding: utf-8
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint



class articles(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    article_name = db.Column('article_name', db.VARCHAR(50), unique = True, nullable=False)
    author_name = db.Column('author_name', db.VARCHAR(70), nullable=False)
    article_file = db.Column('article_file', db.VARCHAR(50), unique = True, nullable=False)
    date = db.Column('date', db.DateTime) #is it trur type?
    author_email = db.Column('email', db.VARCHAR(30), unique = True, nullable=False)
    status = db.Column('status', db.SmallInteger)
    article_rating = db.relationship('article_rating', backref='articles', lazy='dynamic')
    users_comment = db.relationship('users_comment', backref='articles', lazy='dynamic')    #how does fucking lazy works?
    
    def __init__(self, article_name, author_name, article_file,email):
        self.article_name = article_name
        self.author_name = author_name
        self.article_file = article_file
        self.date = datetime.utcnow()
        self.author_email = email
        self.status = 2


    def __repr__(self):
        return 'ID-{0}\nAUTHOR-{1}\nARTICLE-{2}\nDATE-{3}\nARTICLE_FILE-{4}\nEMAIL-{5}\nSTATUS-{6}\n'.format(self.id,\
                                                                                   self.author_name,\
                                                                                   self.article_name,\
                                                                                   self.date,\
                                                                                   self.article_file,\
                                                                                   self.email,\
                                                                                   self.status)
                                                                                   


class culture_admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(70))
    login = db.Column('login', db.VARCHAR(20), unique = True, nullable=False)
    password = db.Column('password', db.VARCHAR(100), nullable=False)
    email = db.Column('email', db.VARCHAR(50), unique=True, nullable=False)
    phone = db.Column('phone', db.VARCHAR(30), unique=True)
    article_rating = db.relationship('article_rating', backref='culture_admins', lazy='dynamic')
    registered_on = db.Column('registered_on' , db.DateTime)
    def __init__(self, name, login, password, email, phone):
        self.name = name
        self.login = login
        self.password = generate_password_hash(password)
        self.email = email
        self.phone = phone
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return 'ID-{0}\nNAME-{1}\nLOGIN-{2}\nPASSWORD-{3}\nEMAIL-{4}\nPHONE-{5}\n,ADMIN_STATUS-{6},REGISTERED-{7}'.format(self.id,\
                                                                                   self.name,\
                                                                                   self.login,\
                                                                                   self.password,\
                                                                                   self.email,\
                                                                                   self.phone,\
                                                                                   self.admin_status,\
                                                                                   self.registered_on)
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

    def check_password(self,password):
        return check_password_hash(self.password, password)





#in article_rating table admins write comments about article
class article_rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id')) #foreign key
    admin_id = db.Column(db.Integer, db.ForeignKey('culture_admins.id')) #foreign key
    rating = db.Column('rating', db.Integer)
    comment = db.Column('comment', db.VARCHAR(500))
    date = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('article_id', 'admin_id', name='unique_rating'),)
    def __init__(self, article_id, admin_id, comment, rating):
        self.article_id = article_id
        self.admin_id = admin_id
        self.comment = comment
        self.date = datetime.utcnow()
        self.rating = rating

    def __repr__(self):
        return 'ARTICLE_ID-{0}\nADMIN_ID-{1}\nCOMMENT-{2}\nRATING-{3}'.format(self.article_id,\
                                                                    self.admin_id,\
                                                                    self.comment,\
                                                                    self.rating)
class users_comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_name = db.Column(db.VARCHAR(70))
    email = db.Column(db.VARCHAR(30))
    comment_body = db.Column(db.VARCHAR(500))
    date = db.Column(db.DateTime)
    def __init__(self, article_id, user_name, email, comment_body):
        self.article_id = article_id
        self.user_name = user_name
        self.email = email
        self.comment_body = comment_body
        self.date = datetime.utcnow()

    def __repr__(self):
        return 'ARTICLE_ID-{0}\nUSER_NAME-{1}\nEMAIL-{2}\nCOMMENT_BODY-{3}\nDATE-{4}\n'.format(self.article_id,\
                                                                   self.user_name,\
                                                                   self.email,\
                                                                   self.comment_body,\
                                                                   self.date)

