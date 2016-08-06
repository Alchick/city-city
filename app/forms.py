#coding: utf-8
from flask_wtf import Form
from wtforms import TextField
#from wtforms.validators import Length, Email, Regexp, DataRequired, Required, ValidationError
from wtforms.validators import *
from werkzeug.security import generate_password_hash, check_password_hash
import re


class MainForm(Form):
    author_name = TextField('author_name', description = 'author_name', validators=[Required(message = u'Введите Имя'),\
                                                                             Regexp(r'^[a-zA-Z]+$', message = u'Неверный символ'),\
                                                                             Length(max=40)])
    article_name = TextField('article_name', description = 'article_name', validators=[required(message = u'введите название статьи'),\
                                                                             regexp(r'^[a-za-z0-9]+$', message = u'неверный символ'),\
                                                                             length(max=40)])
    email = TextField('email', validators = [Required(message = u'Введит электронный адрес')])
                                             #Email(message = u'Неверный почта')])
    comment = TextField('comment', description = 'comment', validators=[required(message = u'Введите комментарий'),\
                                                                             regexp(r'^[a-za-z0-9]+$', message = u'неверный символ'),\
                                                                             length(max=500)])

class LoginForm(Form):
    login = TextField('login', validators=[Required(message=u'Пустое поле')]) #Test Regexp
    password = TextField('password', validators=[Required(message=u'Пустое поле')]) #Test regexp

