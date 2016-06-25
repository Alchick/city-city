from app import db

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    autor = db.Column(db.String(64), index = True)
    data = db.Column(db.DateTime, index=True)
    article_name = db.Column(db.String(64))
    file_name = db.Column(db.String(120), index = True, unique = True)
    path_to_file = db.Column(db.String(120), index = True, unique = True)
                    
    def __repr__(self):
        return '<Author{0}\ndata{1}\narticle_name{2}\nfile_name{3}\npath_to_file{4}>'.format(self.autor, self.data, self.article_name, self.file_name, self.path_to_file)
