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
import string
import random
import time
from matplotlib import style
import datetime

SESSION_TYPE = 'filesystem'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Upload Folder')
ALLOWED_EXTENSIONS = (['csv'])


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def id_generator(size=8, chars=string.ascii_uppercase + string.digits): #File name Generator
#     return ''.join(random.choice(chars) for _ in range(size))

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    return st

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_clickable(val): #turns the file_name into links, upon clicking sends to recon.html where data is displayed accordingly
    dfrecon = pd.read_csv(val)
    z = pd.DataFrame(dfrecon)
    return render_template("recon.html", name=dfrecon, data=z.to_html())
    #return '<a target="_blank" href="recon.html">{}</a>'.format(val, val)


@app.route('/', methods=['GET', 'POST'])

def Recon():
#     pff = os.path.join(UPLOAD_FOLDER, "FileFrame.csv")
#     with open(pff) as f:
#         FileFrame=pd.read_csv(f)
    #This is the file that would contain the file pairs as well as the reconiciliation file name
#     FileFrame = 'Nothing to display yet'
#     if request.method == 'GET':
       # y = pd.DataFrame(FileFrame)
#         return render_template("DF.html", n=FileFrame, d=y.to_html())
#     #if not 'GET'== NULL
    if request.method == 'GET':
        return render_template("DF.html")


    # check if the post request has the file part
    if 'F1' not in request.files:
        flash('No Selected file 1')
        return redirect(request.url)
    file1 = request.files['F1']

    # if user does not select file, browser also
    # submit a empty part without filename

    if not (file1 and allowed_file(file1.filename)):
        flash("something wrong with file 1")
        return redirect(request.url)
    

    filename1 = secure_filename(file1.filename)
    Time= timestamp()
    stamps = ['']
    stamps.append(Time)
    fileframe = pd.DataFrame(columns=stamps)
    
    FT1= Time + '-f1.csv'
    filename1b = os.path.join(app.config['UPLOAD_FOLDER'], FT1)
    file1.save(filename1b)
    dfrc1 = pd.read_csv(filename1b)




    # check if the post request has the file part
    if 'F2' not in request.files:
        flash('No Selected file 2')
        return redirect(request.url)
    file2 = request.files['F2']

    # if user does not select file, browser also
    # submit a empty part without filename

    if not (file2 and allowed_file(file2.filename)):
        flash("something wrong with file 2")
        return redirect(request.url)

    filename2 = secure_filename(file1.filename)
    fileT2= Time + '-f2.csv';
    filename2b = os.path.join(app.config['UPLOAD_FOLDER'], fileT2)
    file2.save(filename2b)
    dfrc2 = pd.read_csv(filename2b)

    #This section checks if any or both files have the appropriate columns and flashes a messages accordingly
    if not (({'symbol', 'position'}.issubset(dfrc1.columns))or({'symbol', 'position'}.issubset(dfrc2.columns))):
        flash("File 1 and File 2 do not contain the appropriate data. Columns must contain 'symbol' and 'position'.")
        return redirect(request.url)
    else:
        if not {'symbol', 'position'}.issubset(dfrc1.columns):
            flash("File 1 does not contain the appropriate data. Columns must contain 'symbol' and 'position'.")
            return redirect(request.url)
        if not {'symbol', 'position'}.issubset(dfrc2.columns):
            flash("File 2 does not contain the appropriate data. Columns must contain 'symbol' and 'position'.")
            return redirect(request.url)


    DF=dfrc1.merge(dfrc2, left_on='symbol', right_on='symbol', how='outer')
    DF['diff']=DF['position_x']-DF['position_y']
   
    

#     FileFrame.style.format({'url': make_clickable})
    x = pd.DataFrame(DF)
    y = pd.DataFrame(FileFrame)
    return render_template("DF.html",  n=FileFrame, d=y.to_html(), name=DF, data=x.to_html())





if __name__ == '__main__':
    app.debug = True
    app.run()


