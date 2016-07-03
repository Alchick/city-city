import os
from flask import render_template, request, flash, url_for
from app import app
from forms import ArticleForms
from functions import save_request_data, get_data_from_db, check_file_size
import pprint

@app.route('/bla-bla-pizda/')
def pizda(): 
    pass
@app.route('/')
@app.route('/index.html')
def index():
    print url_for('pizda')
    print url_for('static', filename='css/stylemain.css')
    return render_template("index.html")


    

@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/read.html')
def contacts():
    records = get_data_from_db()
    return render_template("read.html",
                           records = records)

@app.route('/get_file.html')
def get_file():
    filename = request.args.get('filename') #could it be empty?
    return render_template("get_file.html",
                          filename = filename)


@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")


@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    form = ArticleForms()
    if request.method=='POST' and form.validate_on_submit():
        file = request.files['userfile']
        if file:
            if check_file_size(file):
                flash(save_request_data(request))
                return render_template("create.html",
                                   form = form)
            else: flash('Wrong file size')
        else: flash("You send no file")
    return render_template("create.html",
                          form = form)


@app.errorhandler(413)
def err_413(error):
    return render_template("index.html")
