#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import backref, scoped_session
from os import environ
from json import dumps

def db_connect():
    return create_engine(environ['DATABASE_URL'])

engine = db_connect()
session = scoped_session(sessionmaker(bind=engine,\
                                      autocommit=False,\
                                      autoflush=False))
Base = declarative_base()
Base.query = session.query_property()
metadata = Base.metadata

class Party(Base):
    __tablename__ = 'parties'
    id            = Column(Integer, primary_key =True)
    deleted       = Column(Boolean, default=False)
    side          = Column(String(30), default='None', nullable=False)
    grouping      = Column(String(40), default='None', nullable=False)    
    addr_1        = Column(String(50), nullable=True)
    addr_2        = Column(String(50), nullable=True)
    city          = Column(String(50), nullable=True)
    state         = Column(String(10), nullable=True)
    zipcode       = Column(String(15), nullable=True)
    country       = Column(String(30), nullable=True)

    def hash(self):
        _hashmap = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        _hashmap['guests'] = [{'last_name' : guest.last_name,
                               'first_name' : guest.first_name,
                               'guest_id' : guest.id}
                               for guest in self.guests]
        return _hashmap

    def jsonify(self):
        return dumps(self.hash())

    def __repr__(self):
        return str(self.jsonify())

class Guest(Base):
    __tablename__ = 'guests'
    id          = Column(Integer, primary_key=True)
    party_id    = Column(Integer, ForeignKey('parties.id'))
    deleted     = Column(Boolean, default=False)
    last_name   = Column(String(50), nullable=True)
    first_name  = Column(String(50), nullable=True)
    priority    = Column(String(20), nullable=True)
    probability = Column(String(20), nullable=True)
    gender      = Column(String(10), nullable=True)
    guest_type  = Column(String(30), default="wedding")
    party       = relationship("Party", lazy='joined', backref=backref("guests", order_by=id))

    def __init__(self, party_id=None):
        if party_id:
            self.party_id = party_id
        else:
            p = Party()
            self.party = p
            self.party_id = p.id

    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def jsonify(self):
        return dumps(self.hash())

    def hash(self):
        _hashmap = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        _hashmap['party'] = {'party_id': self.party_id,
                             'side': self.party.side,
                             'grouping': self.party.grouping,
                             'guests': self.party.guests}
        _hashmap['name'] = self.name()
        return _hashmap

    def __repr__(self):
        return str(self.jsonify())


def drop_tables(engine):
    metadata.drop_all(engine)

def create_tables(engine):
    metadata.create_all(engine)

def drop_and_create():
    drop_tables(engine)
    create_tables(engine)
    session.commit()

def main():
    create_tables(engine)
    session.commit()

if __name__ == '__main__':
    main()
    