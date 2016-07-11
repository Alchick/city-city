from app import db

class Articles(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key = True)
    article_name = db.Column(db.String)
    author_name = db.Column(db.String)
    file_name = db.Column(db.String)
    date = db.Column(db.DateTime)
    email = db.Column(db.String)
    def __init__(self, article_name, author_name, file_name, date, email):
        self.article_name = article_name
        self.author_name = author_name
        self.file_name = file_name
        self.date = date
        self.email = email


    def __repr__(self):
        return 'ID-{0}\nAUTHOR-{1}\nARTICLE-{2}\nDATE-{3}\nFILE_NAME-{4}\nEMAIL-{5}'.format(self.id,\
                                                                                   self.author_name,\
                                                                                   self.article_name,\
                                                                                   self.date,\
                                                                                   self.file_name,\
                                                                                   self.email)

class Admins(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('admins.id'), primary_key = True)
    Admin_name = db.Column(db.String)
    Admin_login = db.Column(db.String)
    Admin_password = db.Column(db.String)
    Admin_phone = db.Column(db.String)
    Admin_email = db.Column(db.String)
    Admin_status = db.Column(db.Integer)
    def __init__(self, Admin_name, Admin_login, Admin_password, Admin_phone, Admin_email, Admin_status):
        self.Admin_name = Admin_name
        self.Admin_login = Admin_login
        self.Admin_password = Admin_password
        self.Admin_phone = Admin_phone
        self.Admin_email = Admin_email
        self.Admin_status = Admin_status
    def __repr__(self):
        return 'ID-{0}\nADMIN_NAME{1}\nADMIN_LOGIN{1}\nADMIN_PASSWORD{2}\nADMIN_PHONE{3}\nADMIN_EMAIL{4}\nADMIN_STATUS{5}'.format(self.id,\
                                                                                                                                  self.Admin_name,\
                                                                                                                                  self.Admin_login,\
                                                                                                                                  self.Admin_password,\
                                                                                                                                  self.Admin_phone,\
                                                                                                                                  self.Admin_email,\
                                                                                                                                  self.Admin_status)


class Article_comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    User__name = db.Column(db.String)
    Article_id = db.relationship('Articles', backref='articles', cascade='all, delete-orphan', lazy='dynamic')
    Comment_id = db.Column(db.Integer)
    Comment_body = db.Column(db.String)
    def __init__(self, User_name, Article_id, Comment_id, Comment_body):
        self.User_name = User_name
        self.Article_id = Article_id
        self.Comment_id = Comment_id
        self.Comment_body = Comment_body
    def __repr__(self):
        return 'ID-{0}\nUSER_NAME{1}\nARTICLE_ID{2}\nCOMMENT_ID{3}\nCOMMENT_BODY{4}\n'.format(self.id,\
                                                                                              self.User_name,\
                                                                                              self.Article_id,\
                                                                                              self.Comment_id,\
                                                                                              self.Comment_body)

class Article_status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Article_id = db.relationship('Articles', backref='articles', cascade='all, delete-orphan', lazy='dynamic')
    Admin_id = db.relationship('Admins', backref='admins', cascade='all, delete-orphan', lazy='dynamic')
    Article_status = db.Column(db.Integer)
    Comment = db.Column(db.String)
    def __init__(self, Article_id, Admin_id, Article_status, Comment):
        self.Article_id = Article_id
        self.Admin_id = Admin_id
        self.Article_status = Article_status
        self.Comment = Comment
    def __repr__(self):
        return 'ID-{0}\nARTICLE_ID{1}\nADMIN_ID{2}\nARTICLE_STATUS{3}\nCOMMENT{4}\n'.format(self.id,\
                                                                                            self.Article_id,\
                                                                                            self.Admin_id,\
                                                                                            self.Article_status,\
                                                                                            self.Comment)




