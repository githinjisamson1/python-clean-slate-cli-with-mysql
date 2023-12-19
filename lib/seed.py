#!/usr/bin/env python3

import mysql.connector
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Cleaner, Client, CleaningTask, ClientTask, Base

# for generating fake values/dummy data
fake = Faker()

experience_levels = ["junior", "intermediate", "senior"]

cleaning_tasks = [
    {
        "task_description": "Dish washing",
        "price": 150
    },
    {
        "task_description": "Laundry",
        "price": 200
    },
    {
        "task_description": "Carpet cleaning",
        "price": 250
    },
    {
        "task_description": "Car wash",
        "price": 300
    },
    {
        "task_description": "Window cleaning",
        "price": 350
    },
    {
        "task_description": "Construction cleaning",
        "price": 400
    },
    {
        "task_description": "Janitorial Services",
        "price": 450
    },
    {
        "task_description": "Pressure Washing",
        "price": 500
    },
    {
        "task_description": "Gym cleaning",
        "price": 550
    },
    {
        "task_description": "Dryer Vent Cleaning",
        "price": 600
    },
]


if __name__ == '__main__':

    engine = create_engine(
        'mysql+mysqlconnector://root:27511112086/2019@localhost:3306/clean_slate_db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # !empty tables then fill upon running seed.py
    session.query(Cleaner).delete()
    session.query(CleaningTask).delete()
    session.query(Client).delete()
    session.query(ClientTask).delete()

    # !insert 5 cleaner instances/objects
    for item in range(5):
        cleaner = Cleaner(
            full_name=fake.unique.name(),
            contact_number=fake.numerify(text="##########" ),
            experience_level=random.choice(experience_levels)
        )

        # using session.add() guarantees id will be updated
        session.add(cleaner)
        session.commit()

    # !insert 10 cleaning_tasks instances/objects
    for item in cleaning_tasks:
        cleaning_task = CleaningTask(
            task_description=item["task_description"],
            price=item["price"],
            cleaner_id=random.randint(1, 5)
        )

        session.add(cleaning_task)
        session.commit()

    # !insert 15 client instances/objects
    for item in range(15):
        client = Client(
            client_name=fake.unique.name(),
            email=fake.email(),
            password=fake.password(length=12),
            contact_number=fake.numerify(text="##########"),
        )

        session.add(client)
        session.commit()

    # task_ids list comprehension/tasks will have been inserted atp
    task_ids = [task.task_id for task in session.query
                (CleaningTask)]

    # client_ids list comprehension/clients will have been inserted atp
    client_ids = [client.client_id for client in session.query(Client)]

    # !map client_ids to task_ids/Association/10 instances
    for item in range(10):
        client_task = ClientTask(
            client_id=random.choice(client_ids),
            task_id=random.choice(task_ids)
        )

        session.add(client_task)
        session.commit()

    # terminate session
    session.close()
