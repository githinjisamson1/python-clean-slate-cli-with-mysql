from sqlalchemy import create_engine, desc
from sqlalchemy import (CheckConstraint, UniqueConstraint,
                        Column, DateTime, Integer, BigInteger, String, ForeignKey)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import mysql.connector

Base = declarative_base()


# TODO: Cleaner Model

class Cleaner(Base):
    # name
    __tablename__ = "cleaners"

    # columns
    cleaner_id = Column(Integer(), primary_key=True)
    full_name = Column(String(50))
    contact_number = Column(BigInteger)
    experience_level = Column(String(50))

    # !relationship with CleaningTask on cleaner
    cleaning_tasks = relationship("CleaningTask", backref="cleaner")

    # string 50representation
    def __repr__(self):
        return f"Cleaner {self.cleaner_id}: " \
            + f"{self.full_name}, " \
            + f"Experience Level {self.experience_level}"


# TODO: Client Model

class Client(Base):
    # name
    __tablename__ = "clients"

    # args/classes of constraints/PK/UC/
    __table_args__ = (UniqueConstraint('email',
                                       name='unique_email'),)

    # columns
    client_id = Column(Integer(), primary_key=True)
    client_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    contact_number = Column(BigInteger)

    # !relationship with ClientTask on client
    # ClientTask must have client
    cleaning_tasks = relationship("ClientTask", back_populates="client")

    # string 50representation
    def __repr__(self):
        return f"Client {self.client_id}: " \
            + f"{self.client_name}, " \


# TODO: CleaningTask Model


class CleaningTask(Base):
    # name
    __tablename__ = "cleaning_tasks"

    # columns
    task_id = Column(Integer(), primary_key=True)
    task_description = Column(String(50))
    price = Column(String(50))

    # ForeignKey cleaner_id
    cleaner_id = Column(Integer(), ForeignKey("cleaners.cleaner_id"))

    # !relationship with ClientTask on task
    # ClientTask must have task
    clients = relationship("ClientTask", back_populates="task")

    # string 50representation
    def __repr__(self):
        return f"Cleaning Task {self.task_id}: " \
            + f"{self.task_description}, " \
            + f"Price  {self.price}: " \


# TODO: ClientTask Model
# intermediary/Association Object


class ClientTask(Base):
    # name
    __tablename__ = "client_tasks"

    # columns
    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey("clients.client_id"))
    task_id = Column(Integer(), ForeignKey("cleaning_tasks.task_id"))

    # !relationship with Client on cleaning_tasks
    client = relationship('Client', back_populates='cleaning_tasks')

    # !relationship with CleaningTask on clients
    task = relationship('CleaningTask', back_populates='clients')

    # string 50representation
    def __repr__(self):
        return f'ClientTask(game_id={self.client_id}, ' + \
            f'task_id={self.task_id})'


# avoid Base.metadata/tables are already created using seed.py
engine = create_engine(
    'mysql+mysqlconnector://root:27511112086/2019@localhost:3306/clean_slate_db')
Session = sessionmaker(bind=engine)
session = Session()

# !work with clean_slate outside lib/
