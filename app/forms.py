#coding: utf-8
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required, Length, Email, Regexp, DataRequired, ValidationError
import re


class ArticleForms(Form):
    author_name = TextField('author_name', description = 'name', validators=[Required()])
    article_name = TextField('article_name', validators=[Required()])
    email = TextField('email', validators = [Required()])

