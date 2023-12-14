from sqlalchemy import create_engine, desc
from sqlalchemy import (CheckConstraint, UniqueConstraint,
                        Column, DateTime, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///clean_slate.db')

Base = declarative_base()

# !models

class Cleaner(Base):
    # name
    __tablename__ = "cleaners"

    # columns
    cleaner_id = Column(Integer(), primary_key=True)
    full_name = Column(String(25))
    contact_number = Column(Integer())
    experience_level = Column(String())

    # !relationship with CleaningTask on cleaner
    cleaning_tasks = relationship("CleaningTask", backref="cleaner")

    # string representation
    def __repr__(self):
        return f"Cleaner {self.cleaner_id}: " \
            + f"{self.full_name}, " \
            + f"Experience Level {self.experience_level}"


class Client(Base):
    # name
    __tablename__ = "clients"

    # args/classes of constraints/PK/UC/
    __table_args__ = (UniqueConstraint('email',
                                       name='unique_email'),)

    # columns
    client_id = Column(Integer(), primary_key=True)
    client_name = Column(String(25))
    email = Column(String())
    password = Column(String())
    contact_number = Column(Integer())

    # !relationship with ClientTask on client
    # ClientTask must have client
    cleaning_tasks = relationship("ClientTask", back_populates="client")

    # string representation
    def __repr__(self):
        return f"Client {self.client_id}: " \
            + f"{self.client_name}, " \



class CleaningTask(Base):
    # name
    __tablename__ = "cleaning_tasks"

    # columns
    task_id = Column(Integer(), primary_key=True)
    task_description = Column(String())
    price = Column(String())

    # ForeignKey cleaner_id
    cleaner_id = Column(Integer(), ForeignKey("cleaners.cleaner_id"))

    # !relationship with ClientTask on task
    # ClientTask must have task
    clients = relationship("ClientTask", back_populates="task")

    # string representation
    def __repr__(self):
        return f"Cleaning Task {self.task_id}: " \
            + f"{self.task_description}, " \
            + f"Price  {self.price}: " \


# intermediary/Association Object/CLIENTTASKASSIGNMENT

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

    # string representation
    def __repr__(self):
        return f'ClientTask(game_id={self.client_id}, ' + \
            f'task_id={self.task_id})'

# TODO:
# How to use Click/Fire?
# How to implement user authentication?
