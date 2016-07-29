from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



class articles(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    article_name = db.Column('article_name', db.VARCHAR, unique = True, nullable=False)
    author_name = db.Column('author_name', db.VARCHAR, nullable=False)
    article_file = db.Column('article_file', db.VARCHAR, unique = True, nullable=False)
    date = db.Column('date', db.DateTime, nullable=False) #is it trur type?
    email = db.Column('email', db.VARCHAR, unique = True, nullable=False)
    status = db.Column('status', db.SmallInteger)
    article_rating = db.relationship('article_rating', backref='articles', lazy='dynamic')
    users_comment = db.relationship('users_comment', backref='articles', lazy='dynamic')    #how does fucking lazy works?
    
    def __init__(self, article_name, author_name, article_file, date, email):
        self.article_name = article_name
        self.author_name = author_name
        self.article_file = article_file
        self.date = date
        self.email = email
        self.status = 2


    def __repr__(self):
        return 'ID-{0}\nAUTHOR-{1}\nARTICLE-{2}\nDATE-{3}\nARTICLE_FILE-{4}\nEMAIL-{5}\nSTATUS-{6}\n'.format(self.id,\
                                                                                   self.author_name,\
                                                                                   self.article_name,\
                                                                                   self.date,\
                                                                                   self.article_file,\
                                                                                   self.email,\
                                                                                   self.status,\
                                                                                   self.article_rating)


class culture_admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR)
    login = db.Column('login', db.VARCHAR, unique = True, nullable=False)
    password = db.Column('password', db.VARCHAR, nullable=False)
    email = db.Column('email', db.VARCHAR, unique=True, nullable=False)
    phone = db.Column('phone', db.VARCHAR, unique=True)
    admin_status = db.Column('admin_status', db.SmallInteger) #depends on desc\asc in query
    article_rating = db.relationship('article_rating', backref='culture_admins', lazy='dynamic')
    registered_on = db.Column('registered_on' , db.DateTime)
    def __init__(self, name, login, email, phone, password):
        self.name = name
        self.login = login
        self.email = email
        self.phone = phone
        self.set_password(password)
        self.registered_on = datetime.utcnow()
        self.status = 2

    def __repr__(self):
        return 'ID-{0}\nNAME-{1}\nLOGIN-{2}\nEMAIL-{3}\nPHONE-{4}\n,ADMIN_STATUS-{5}'.format(self.id,\
                                                                                   self.name,\
                                                                                   self.login,\
                                                                                   self.email,\
                                                                                   self.phone,\
                                                                                   self.admin_status)
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class article_rating(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    article_id = db.Column('article_id', db.Integer, db.ForeignKey('articles.id')) #foreign key
    admin_id = db.Column('admin_id', db.Integer, db.ForeignKey('culture_admins.id')) #foreign key
    rating = db.Column('rating', db.Integer, default=0)
    comment = db.Column('comment', db.VARCHAR)
    def __init__(self, article_id, admin_id, rating, comment, date):
        self.article_id = article_id
        self.admin_id = admin_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return 'id-{0}\nARTICLE_ID-{1}\nADMIN_ID-{2}\nRATING-{3}\nCOMMENT-{4}\n'.format(self.article_id,\
                                                                          self.admin_id,\
                                                                          self.rating,\
                                                                          self.comment)
class users_comment(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    article_id = db.Column('article_id', db.Integer, db.ForeignKey('articles.id'))
    user_name = db.Column('user_name', db.VARCHAR)
    email = db.Column('email', db.VARCHAR)
    comment_body = db.Column('comment_body', db.VARCHAR)
    date = db.Column('date', db.DateTime) #is it needet type? is is true type?, maybe timezone or something
    def __init__(self,article_id, user_name, email, comment_body):
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




