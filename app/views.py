import os
from flask import render_template, request, flash
from app import app
from forms import ArticleForms
from functions import save_request_data



@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")




@app.route('/about.html')
def about():
    return render_template("about.html")



@app.route('/read.html')
def contacts():
    return render_template("read.html")

@app.route('/contacts.html')
def contact():
    return render_template("contacts.html")


@app.route('/create.html', methods = ['GET', 'POST'])
def create():
    form = ArticleForms()
    if request.method=='POST':
        print request
        if request.files['userfile']:
            flash(save_request_data(request))
            return render_template("create.html",
                                   form = form)
        else: flash("You send no file")
    return render_template("create.html",
                          form = form)



