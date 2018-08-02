
Reconciler.app
============


What It Does
---------------

This is a Flask web application designed to allow users to reconcile two .csv files with designated columns. It also allows the usage of tables within the connected database and revisiting of past reconciliations.


How To Install
-----------------

In order to correctly run the project these are the steps for installation:

1. Have a working private server.

2. Have a psql database within the server, use 'psql (databasename)' in your terminal to access the database

3. Create a table and edit it with the following lines:
		CREATE TABLE securities (
		    symbol varchar(255),
		    position int
		);


4. Copy the setting.py.dist file contents into a separate file entitled settings.py after entering the database name and enter your username and password in settings.py 

5. Use terminal to direct to the directory where flaskr.py is located (i.e: ./Recon/flaskr/flaskr)

6. Execute the command: sh -e ./run.txt : this runs flask via your server on port 5000. You may access and run.txt and change the port used at your behest.

7. Access your server at the designated port (port 5000 if unchanged) by typing the url: servername.net:5000


Example Usage
------------------
//to be modified



How to Set Up The Development Environment
------------------------------------------------------

In order to set up the development environment certain frameworks need to be installed:

- Python frameworks
- PSQL
- Flask
- SQLAlchemy



License and author info
----------------------------

Copyright(C) Akiki Engineering Est. 2018









