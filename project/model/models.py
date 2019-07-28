from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine
from project.config import SQLALCHEMY_DATABASE_URI
import logging

# Create a DBAPI connection

# Setting up Base to automap
Base = automap_base()
# Creating engine using connection string 
engine = create_engine(SQLALCHEMY_DATABASE_URI, isolation_level="READ UNCOMMITTED")
Base.prepare(engine, reflect=True)
# Creating session using engine
session = Session(engine)


Customer = Base.classes.customer
BranchOffice = Base.classes.branch_office
HeadOffice = Base.classes.head_office
Transaction = Base.classes.transaction



# setting up logging
logger = logging.getLogger(__name__)
format = '[%(asctime)s] [%(levelname)s] [%(message)s] [--> %(pathname)s [%(process)d]:]'
logging.basicConfig(format=format, level=logging.INFO)