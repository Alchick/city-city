from app import db

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String, unique = True)
    author_name = db.Column(db.String)
    file_name = db.Column(db.String, unique = True)
    date = db.Column(db.DateTime)
    email = db.Column(db.String)
    def __init__(self, article_name, author_name, file_name, date, email):
        self.article_name = article_name
        self.author_name = author_name
        self.file_name = file_name
        self.date = date
        self.email = email


    def __repr__(self):
        return 'id-{0}\nAuthor-{1}\nArticle-{2}\ndate-{3}\nfile_name-{4}\nemail-{5}'.format(self.id,\
                                                                                   self.author_name,\
                                                                                   self.article_name,\
                                                                                   self.date,\
                                                                                   self.file_name,\
                                                                                   self.email)


'''
NOTES
while change field name, all data have dismised
'''
