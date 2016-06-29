from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class ArticleForms(Form):
    author_name = TextField('author_name', validators=[Required()])
    article_name = TextField('article_name', validators=[Required()])
    email = TextField('email', validators = [Required()])

