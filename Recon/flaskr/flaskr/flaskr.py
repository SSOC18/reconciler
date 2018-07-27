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
import urllib.parse as urlparse
from urllib.parse import urlencode
import psycopg2 as pg
import pandas.io.sql as psql
from flask import Flask
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import insert
import logging
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)

SESSION_TYPE = 'filesystem'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'Upload Folder')
ALLOWED_EXTENSIONS = (['csv'])


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class securities(object):
    pass
 

# def loadSession():
#     """"""    
    
#     engine = create_engine('postgresql:/fatme:upBH2UtS@localhost/mf_dummy', echo=True)
 
#     metadata = MetaData(engine)
#     sec = Table('securities', metadata, 
#                       Column("symbol", Integer, primary_key=True), Column("position", Integer, primary_key=True))
#     mapper(Securities, sec)
 
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session
 


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    return st

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# from https://stackoverflow.com/a/3207973/4126114
from os import listdir
from os.path import isfile, join
  
    
@app.route('/', methods=['GET', 'POST'])
def Recon():

    if request.method == 'GET':
        
        return render_template("Recon.html",H2="View Previous Reconciliations", H3="Upload from Database" )
        
        
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
    fileT2= Time + '-f2.csv'
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

    fn_sel = Time
    return redirect("http://ssoc18.teamshadi.net:5000/ReconView?fn_sel=" + fn_sel)
  

@app.route('/ReconView', methods=['GET', 'POST'])
def Redux():
    num = request.args.get('fn_sel')
    mypath = UPLOAD_FOLDER
    for file in os.listdir(mypath):
        if file.endswith(num + "-f1.csv"):
            f1=file
            f11 = os.path.join(app.config['UPLOAD_FOLDER'], f1)
            rc1 = pd.read_csv(f11)

        elif file.endswith(num + "-f2.csv"):
            f2=file
            f22 = os.path.join(app.config['UPLOAD_FOLDER'], f2)
            rc2 = pd.read_csv(f22)
    DF=rc1.merge(rc2, left_on='symbol', right_on='symbol', how='outer')
    DF['diff']=DF['position_x']-DF['position_y']
    x = pd.DataFrame(DF)
    mypath = UPLOAD_FOLDER
    
    return render_template("ReconView.html", Title="Current Reconciliation", data=x.to_html(), Uploadnew="Upload new reconciliation", H2="View Previous Reconciliations")

@app.route('/listprev', methods=['GET', 'POST'])
def listfiles():
    mypath = UPLOAD_FOLDER
    fn_all = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    fn_all = [f.replace('.csv','').replace('-f1','').replace('-f2','') for f in fn_all]
    fn_all = list(set(fn_all))
    fn_all.sort()
    return render_template("listprev.html", fn_all=fn_all, fn_sel=request.args.get('fn_sel'))

@app.route ('/uploadfromdb', methods=['GET','POST'])
def dbupload():
    
    if request.method == 'GET':
        
        return render_template("uploadfromdb.html",H2="View Previous Reconciliations", H3="Upload files" )
        
        
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
    FT1= Time + '-f1.csv'
    filename1b = os.path.join(app.config['UPLOAD_FOLDER'], FT1)
    file1.save(filename1b)
    dfrc1 = pd.read_csv(filename1b)

    
#     if 'Table' not in request.headers:
#         flash('No Selected Table')
#         return redirect(request.url)
    Tablename = request.form['Table']

    # if user does not select file, browser also
    # submit a empty part without filename

    
    
#     if 'Table' not in database
#         flash("Table not in database")
#         return redirect(request.url)

    tablename=Tablename
#     engine = create_engine('postgresql:/fatme:upBH2UtS@localhost/mf_dummy', echo=True)
    engine = create_engine("postgres:http://ssoc18.teamshadi.net:8000/mf_dummy", echo=True)
    metadata = MetaData(engine)
    sec = Table('securities', metadata, 
                      Column("symbol", Integer, primary_key=True), Column("position", Integer, primary_key=True))
    mapper(Securities, sec)
    connection = engine.connect()
    table=pd.read_sql_table(tablename, connection, schema=None, index_col=None, coerce_float=True, parse_dates=None, columns=['symbol','position'], chunksize=None)
    fileT2= Time + '-f2.csv'
    newfile=table.to_csv('newfile.csv')
    filename2b = os.path.join(app.config['UPLOAD_FOLDER'], fileT2)
    newfile.save(filename2b)
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

    fn_sel = Time
    return redirect("http://ssoc18.teamshadi.net:5000/ReconView?fn_sel=" + fn_sel)
    
    
                           
if __name__ == '__main__':
    app.debug = True
    session = loadSession()
    res = session.query(Securities).all()
    res[1].title
    app.run()


