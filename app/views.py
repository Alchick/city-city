from werkzeug.utils import secure_filename
import os
from flask import render_template, request, redirect, url_for
from app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['pdf', 'jpeg', 'png', 'py']



@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")




@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/contacts.html')
def contacts():
    return render_template("contacts.html")

@app.route('/read.html')
def contacts():
    return render_template("read.html")

@app.route('/create.html', methods = ['GET', 'POST', 'PUT'])
def create():
    if request.method=='POST':
        file = request.files['userfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/tmp/', filename))
        return render_template("create.html")
    return render_template("create.html")


