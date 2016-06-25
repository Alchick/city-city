from werkzeug.utils import secure_filename
import os
from flask import render_template, request, redirect, url_for, flash, session
from app import app,db,models
from werkzeug.exceptions import RequestEntityTooLarge
from datetime import datetime

UPLOAD_FOLDER = '/tmp/file_storage/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'txc'])
MAX_CONTENT_LENGTH = 16 * 1024
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'



#@app.route('/')
#@app.route('/index.html')
#def index():
#    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST', 'PUT'])
@app.route('/index.html', methods = ['GET', 'POST', 'PUT'])
@app.route('/create.html', methods = ['GET', 'POST', 'PUT'])
@app.route('/create', methods = ['GET', 'POST', 'PUT'])
def create():
    if request.method=='POST':
        try:
            file = request.files['file_name']
            record = models.Articles(autor=request.form['Author_name'],\
                                    data=datetime.today(),\
                                    article_name = request.form['Article_Name'],\
                                    file_name = file.filename,\
                                    path_to_file=os.path.join(UPLOAD_FOLDER, file.filename))
            db.session.add(record)
            db.session.commit()
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('succes')
                return render_template("create.html")
            else:
                flash('problem')
                return render_template("create.html")
        except RequestEntityTooLarge as ex:
            flash(ex)
            return render_template("create.html")
        #print request.form, '\n' 
        #print 'this is added file in post request', request.files, '\n'
        #print 'Author name', request.form['Author_name']
        #print 'file name', request.files['file_name'].filename
    return render_template("create.html")

@app.route('/read.html')
@app.route('/read')
def read():
    user = models.Articles.query.get(2)
    return render_template("read.html", user=user)

@app.route('/article.html')
@app.route('/article')
def bla_bla():
    return render_template("Article.html")

