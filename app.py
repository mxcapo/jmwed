#!/usr/bin/env python

from flask import Flask, render_template, request
from os import environ
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from model import Party, Guest

@app.route('/')
def coming_soon():
    return render_template('templates/index.html')


if __name__ == '__main__':
    
    app.debug = True
    app.run()