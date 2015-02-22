from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, relationship 
from sqlalchemy.orm import backref, scoped_session