#!/usr/bin/env python
from sqlalchemy.engine.url import URL
from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'aasdlkfjwoAfdgknFGJMKdfkweAFFk'
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']