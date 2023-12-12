#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Cleaner, Client, CleaningTask, ClientTask, Base


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

    engine = create_engine('sqlite:///clean_slate.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Cleaner).delete()
    session.query(CleaningTask).delete()
    session.query(Client).delete()
    session.query(ClientTask).delete()

    for _ in range(5):
        cleaner = Cleaner(
            full_name=fake.unique.name(),
            contact_number=fake.phone_number(),
            experience_level=random.choice(experience_levels)
        )

        session.add(cleaner)
        session.commit()

    for item in cleaning_tasks:
        cleaning_task = CleaningTask(
            task_description=item["task_description"],
            price=item["price"],
            cleaner_id=random.randint(1, 5)
        )
        session.add(cleaning_task)
        session.commit()

    for _ in range(15):
        client = Client(
            client_name=fake.unique.name(),
            email=fake.email(),
            password=fake.password(length=12),
            contact_number=fake.phone_number()
        )
        session.add(client)
        session.commit()

    task_ids = [task.task_id for task in session.query
                (CleaningTask)]
    client_ids = [client.client_id for client in session.query(Client)]

    for _ in range(10):
        client_task = ClientTask(
            client_id=random.choice(client_ids),
            task_id=random.choice(task_ids)
        )
        session.add(client_task)
        session.commit()

    session.close()
