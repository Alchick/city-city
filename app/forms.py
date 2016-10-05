#coding: utf-8
from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import Length, Email, Regexp, DataRequired, Required, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import re

class CreateForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    author_name = TextField('author_name', validators=[Required(message = u'Введите Имя'),\
                                                                             Length(max=50)])
    article_name = TextField('article_name', validators=[Required(message = u'Введите название статьи'),\
                                                                             Length(max=50)])
    email = TextField('email', validators = [Required(message = u'Введит электронный адрес'),\
                                            Email(message = u'Неверный формат электронной почты')])
    submit = SubmitField('submit')

class LoginForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    login = TextField('login', validators=[Required(message=u'Пустое поле')])
    password = PasswordField('password', validators=[Required(message=u'Пустое поле')])

class FindForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    author_name = TextField('author_name', validators=[Required(message = u'Введите Имя'),\
                                                                Length(max=40)])
    article_name = TextField('article_name',validators=[Required(message = u'Введите название статьи'),\
                                                                Length(max=40)])

class CommentForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    author_name = TextField('author_name', validators=[Required(message = u'Введите Имя'),\
                                                       Length(max=40)])
    email = TextField('email', validators = [Required(message = u'Введит электронный адрес'),\
                                            Email(message = u'Неверный формат электронной почты')])

    comment = TextField('comment', validators=[Required(message = u'Введите комментарий'),\
                                               Length(max=400)])

