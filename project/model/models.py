from datetime import datetime
from sqlalchemy import create_engine, Column, LargeBinary, Integer, SmallInteger, Numeric, String, ForeignKey, Boolean, DateTime, Date, Table, or_, and_, Text, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from project.config import *
from passlib import hash


# Create a DBAPI connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# Declare an instance of the Base class for mapping tables
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    fname = Column(String(100))
    lname = Column(String(100))
    password = Column(String(500))
    active = Column(Boolean(), default=True)
    image_url = Column(String(1000))
    mobile_verified = Column(Boolean(), default=False)
    created = Column(DateTime(), default=datetime.now)
    mobile = Column(String(15))
    modified = Column(DateTime())

    def __init__(self, email, fname, lname, password, active, mobile, image_url):
        # print ('Inside __init__')
        self.fname = fname
        self.lname = lname
        self.mobile = mobile
        self.email = email
        self.password = hash.pbkdf2_sha512.encrypt(password)
        self.active = active
        self.image_url = image_url
        self.modified = datetime.now()

