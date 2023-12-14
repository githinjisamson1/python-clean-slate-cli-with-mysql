#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: use debug.py for testing purposes
# !import models to be tested

from models import Cleaner, Client, CleaningTask, ClientTask

if __name__ == '__main__':

    engine = create_engine('sqlite:///clean_slate.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb
    ipdb.set_trace()
