#coding: utf-8
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Length, Email, Regexp, DataRequired, Required
import re


class ArticleForms(Form):
    author_name = TextField('author_name', description = 'name', validators=[Required(message = u'Пустое поле'),\
                                                                             Regexp(r'^[a-zA-Z]+$', message = u'Неверный символ'),\
                                                                             Length(max=50)])
    article_name = TextField('article_name', validators=[Required(message = u'Пустое поле'),\
                                                         Regexp(r'^[a-zA-Z0-9]+$', message = u'Неверный символ'),\
                                                         Length(max=50)])
    email = TextField('email', validators = [DataRequired(message = u'Пустое поле')])
                                             #Email(message = u'Неверный почта')])

