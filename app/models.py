from app import db

class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String, unique = True)
    author_name = db.Column(db.String)
    article_body_file = db.Column(db.String, unique = True)
    date = db.Column(db.DateTime)
    email = db.Column(db.String, unique = True)
    def __init__(self, article_name, author_name, article_body_file, date, email):
        self.article_name = article_name
        self.author_name = author_name
        self.article_body_file = article_body_file
        self.date = date
        self.email = email

    def __repr__(self):
        return 'ID-{0}\nAUTHOR-{1}\nARTICLE-{2}\nDATE-{3}\nARTICLE_BODY_FILE-{4}\nEMAIL-{5}\n'.format(self.id,\
                                                                                   self.author_name,\
                                                                                   self.article_name,\
                                                                                   self.date,\
                                                                                   self.article_body_file,\
                                                                                   self.email)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    login = db.Column(db.String, unique = True)
    password = db.Column(db.DateTime)
    email = db.Column(db.String)
    user_status = db.Column(db.String, unique = True) #add description
    def __init__(self, name, login, password, email, user_status):
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.user_status = user_status

    def __repr__(self):
        return 'ID-{0}\nNAME-{1}\nLOGIN-{2}\nPASSWORD-{3}\nEMAIL-{4}\nSTATUS-{5}'.format(self.id,\
                                                                                   self.name,\
                                                                                   self.login,\
                                                                                   self.password,\
                                                                                   self.email,\
                                                                                   self.status)
class article_status(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique = True)
    status = db.Column(db.String, unique = True)
#    def __init__(self, iarticle_name, author_name, file_name, date, email):
#        self.article_name = article_name
#        self.author_name = author_name
#        self.file_name = file_name
#        self.date = date
#        self.email = email

    def __repr__(self):
        return 'id-{0}\nARTICLE_ID-{1}\nUSER_ID-{2}\nSTATUS-{3}\n'.format(self.article_id,\
                                                                          self.user_id,\
                                                                          self.status)
class approved_comments(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String, unique = True)
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.String)
#    def __init__(self, article_name, author_name, file_name, date, email):
#        self.article_name = article_name
#        self.author_name = author_name
#        self.file_name = file_name
#        self.date = date
#        self.email = email

    def __repr__(self):
        return 'USER_ID-{0}\nARTICLE_ID-{1}\nCOMMENT-{2}\n'.format(self.user_id,\
                                                                   self.article_id,\
                                                                   self.comment)

#class comments(db.Model):
#    article_id = db.Column(db.String, unique = True)
#    comment_id = db.Column(db.String, unique = True#)
#    comment_body = db.Column(db.String)
#    def __init__(self, article_name, author_name, file_name, date, email):
#        self.article_name = article_name
#        self.author_name = author_name
#        self.file_name = file_name
#        self.date = date
#        self.email = email

#    def __repr__(self):
#        return 'ARTICLE_ID-{0}\nCOMMENT_ID-{1}\nCOMMENT_BODY-{2}\n'.format(self.article_id,\
#                                                                            self.comment_id,\
#                                                                            self.comment_body)
