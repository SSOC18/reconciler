# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import io
import requests
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask, session


SESSION_TYPE = 'filesystem'

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Upload Folder')
ALLOWED_EXTENSIONS = (['csv'])


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def Recon():
    if request.method == 'GET':
        return render_template("DF.html")
        
    # check if the post request has the file part
    print("start post")
    print(request.files)
    if 'F1' not in request.files:
        flash('No file part 1')
        return redirect(request.url)

    print("getting file 1")
    file1 = request.files['F1']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file1.filename == '':
        flash('No selected file 1')
        return redirect(request.url)

    if not (file1 and allowed_file(file1.filename)):
        flash("something wrong with file 1")
        return redirect(request.url)
    
    print("got file 1")
    filename1 = secure_filename(file1.filename)
    filename1b = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    file1.save(filename1b)

    dfrc1 = pd.read_csv(filename1b)

    if 'F2' not in request.files:
        flash('No file part 2')
        return redirect(request.url)

    print("got file 2")
    file2 = request.files['F2']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file2.filename == '':
        flash('No selected file 2')
        return redirect(request.url)

    if not(file2 and allowed_file(file2.filename)):
        flash('No selected file 2')
        return redirect(request.url)

    filename2 = secure_filename(file2.filename)
    filename2b = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    file2.save(filename2b)
    dfrc2=pd.read_csv(filename2b)
    DF=dfrc1.merge(dfrc2, left_on='symbol', right_on='symbol', how='outer')
    DF['diff']=DF['position_x']-DF['position_y']
    x = pd.DataFrame(DF)
    return render_template("DF.html", name='diff', data=x.to_html())







if __name__ == '__main__':
    app.debug = True
    app.run()


