from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///clean_slate.db')

Base = declarative_base()

# class Cleaner(Base)
    # pass
    # migrations && upgrade
    
# class Client(Base)
    # pass
    # migrations && upgrade
    
# class CleaningTask(Base)
    # pass  
    # migrations && upgrade  

# AssociationTable  ClientTaskAssignment(Base)
    # pass
    # migrations && upgrade
    
# debug.py
# seed.py

# Click/Fire
# User authentication