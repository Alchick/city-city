#coding: utf-8
from flask_wtf import Form, PasswordField, SubmitField
from wtforms import TextField
from wtforms.validators import Length, Email, Regexp, DataRequired, Required, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import re

class CreateForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    author_name = TextField('author_name', validators=[Required(message = u'Введите Имя'),\
                                                                             Regexp(reg, message = u'Неверный символ'),\
                                                                             Length(max=40)])
    article_name = TextField('article_name', validators=[Required(message = u'введите название статьи'),\
                                                                             Regexp(reg, message = u'Неверный символ'),\
                                                                             Length(max=40)])
    email = TextField('email', validators = [Required(message = u'Введит электронный адрес'),\
                                            Email(message = u'Неверный почта')])
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
                                                                Regexp(reg, message = u'Неверный символ'),\
                                                                Length(max=40)])
    article_name = TextField('article_name',validators=[Required(message = u'введите название статьи'),\
                                                                Regexp(reg, message = u'неверный символ'),\
                                                                Length(max=40)])

class CommentForm(Form):
    reg = re.compile(u'^[а-яА-Я ]+$')
    #reg = re.compile(u'^[a-zA-Z]+$')
    author_name = TextField('author_name', validators=[Required(message = u'Введите Имя'),\
                                                       Regexp(reg, message = u'Неверный символ'),\
                                                       Length(max=40)])
    email = TextField('email', validators = [Required(message = u'Введит электронный адрес'),\
                                            Email(message = u'Неверный почта')])

    comment = TextField('comment', validators=[Required(message = u'Введите комментарий'),\
                                               Regexp(reg, message = u'Неверный символ'),\
                                               Length(max=400)])
