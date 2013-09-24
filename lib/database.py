""" database handler """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')

from inspired_landing_config import SQLALCHEMY_DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from contextlib import contextmanager

#engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
                                         #autoflush=False,
                                         #bind=engine))
engine = None

def init_engine(uri, **kwargs):
    """ create the engine when needed """
    global engine
    engine = create_engine(uri, **kwargs)
    return engine

db_session = scoped_session(lambda: create_session(autocommit=False,
                                             autoflush=False,
                                             bind=engine))


# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """

    @property
    def columns(self):
        """ list of database column names """
        #for column in self._sa_class_manager.mapper.mapped_table.columns:
            #print column
        return [column.name for column in self.__table__.columns ]

    @property
    def fields(self):
        """ list of model field names """
        return [key for key in self.__mapper__.c.keys()]

    @property
    def column_items(self):
        """ get each class attribute value for the column name """
        return dict((column, getattr(self, column, None)) for column in \
            self.columns)

    @property
    def field_items(self):
        """ get each class attribute value for the field name """
        return dict((field, getattr(self, field)) for field in self.fields)

    #def __repr__(self):
        #return '{}({})'.format(self.__class__.__name__, self.field_items)

    @property
    def to_json(self):
        """ return a dictionary for field items """
        return self.field_items

Base.query = db_session.query_property()

def init_models():
    """ import all the models. 
    TODO need a more programatic method to do this
    """
    import lib.users.models
    
def init_db(engine):
    """ initialize the database """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
        
