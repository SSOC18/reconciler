export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run -h 0.0.0.0 -p 5000

psql mf_dummy

CREATE TABLE securities (
    symbol varchar(255),
    position int
);