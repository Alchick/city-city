#coding: utf-8
from flask_wtf import Form
from wtforms import TextField
#from wtforms.validators import Length, Email, Regexp, DataRequired, Required, ValidationError
from wtforms.validators import *
from werkzeug.security import generate_password_hash, check_password_hash
import re


class ArticleForms(Form):
    author_name = TextField('author_name', description = 'name', validators=[Required(message = u'Пустое поле'),\
                                                                             Regexp(r'^[a-zA-Z]+$', message = u'Неверный символ'),\
                                                                             Length(max=40)])
    article_name = TextField('article_name', validators=[Required(message = u'Пустое поле'),\
                                                         Regexp(r'^[a-zA-Z0-9]+$', message = u'Неверный символ'),\
                                                         Length(max=40)])
    email = TextField('email', validators = [Required(message = u'Пустое поле')])
                                             #Email(message = u'Неверный почта')])


class LoginForm(Form):
    login = TextField('login', validators=[Required(message=u'Пустое поле')])
    password = TextField('password', validators=[Required(message=u'Пустое поле')])

class Comments(Form):
    login = TextField('login', validators=[Required(message=u'Пустое поле')])
    password = TextField('password', validators=[Required(message=u'Пустое поле')])

class RegistrationForm(Form):
    login = TextField('login', validators=[Required(message=u'Пустое поле')])
    password = TextField('password', validators=[Required(message=u'Пустое поле')])
    email = TextField('email', validators = [Required(message = u'Пустое поле')])
                                             #Email(message = u'Неверный почта')])
    name = TextField('name', validators=[Required(message=u'Пустое поле')])
    phone = TextField('phone', validators=[Required(message=u'Пустое поле')])

