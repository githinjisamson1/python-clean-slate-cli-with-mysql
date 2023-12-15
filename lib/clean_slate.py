#! /usr/bin/env python3
# saves the hustle of having to run python3 lib/script.py

# cli made easier
import click

# working with regex
import re

from models import Client, session, CleaningTask, ClientTask

# working with rich text
from rich.table import Table
from rich.console import Console


def home_page(current_user_id):
    # fetch all tasks
    cleaning_tasks = session.query(CleaningTask).all()

    # create console instance
    console = Console()

    # create table instance
    table = Table(show_header=True, header_style="bold yellow")

    # add columns/fields
    table.add_column("task_id", style='bold')
    table.add_column("task_description", style='bold')
    table.add_column("price", style='bold')
    table.add_column("cleaner", style='bold')

    # fill table with fetched tasks
    for item in cleaning_tasks:
        table.add_row(str(item.task_id), item.task_description,
                      str(item.price), item.cleaner.full_name)

    console.print(
        '''Listed below are the variety of services we provide to our esteemed clients.\nEnter a task id to choose and book a cleaning session with us''', style="bold green")

    console.print(table)

    # user input
    selected_task_id = click.prompt("Please select task_id: ", type=int)

    # if selected_id is among ids in cleaning_tasks/is task available?
    if selected_task_id in range(1, (cleaning_tasks[-1].task_id+1)):
        # create client_task instance/association object
        client_task = ClientTask(
            client_id=current_user_id,
            task_id=selected_task_id
        )
        # insert to db
        session.add(client_task)
        session.commit()

        # display info about cleaning_task
        for item in cleaning_tasks:
            if selected_task_id == item.task_id:
                console.print(
                    f'''********************====================********************\n\n{item.task_description} service has been booked successfully!!\n{item.cleaner.full_name} will arrive at your premises in the next hour. Thank you for choosing clean slate 😁\n\n********************====================********************''', style="green")

        session.close()

    else:
        click.secho("Invalid task id! 🙃 Please try again", fg="red")

        # run home_page() again/avoids program exit
        home_page(current_user_id)


# enables nesting of other commands
@click.group()
@click.version_option(version="1.0", prog_name="Clean Slate CLI")
def welcome():
    """ Welcome to Clean Slate.\n
        To sign-in use the sign-in command\n
        ie. lib/script sign-in
    """

    welcome_message = """
    ======================================================================================
        Welcome to 🧼Clean Slate Services🧼
        Hello Client 😁,
        Thank you for choosing Clean Slate. 
        Explore our services, schedule cleanings, and connect with your dedicated cleaner. 
        We're here to assist and provide a seamless experience. 
        Welcome!
        Best regards,
        Clean Slate Management Team
    ======================================================================================
    """

    # control color output
    click.secho((welcome_message), fg="blue", bold=True)


# signin/login
@welcome.command()
@click.option('--email', '-e', prompt="Enter your email")
@click.option('--password', '-p', prompt="Enter your password", hide_input=True)
def sign_in(email, password):
    """Log in using email and password"""

    # filter using provided credentials
    user = session.query(Client).filter_by(
        email=email, password=password).first()

    if user:
        click.echo(user)
        click.secho(("Login successful! 😁"), fg="green")
        # TODO: invoke home_page after successful login
        home_page(user.client_id)
    else:
        click.secho(("Invalid email or password! 🙃"), fg="red")


# signup/register
@welcome.command()
@click.option('--name', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--contact_number', prompt=True)
def sign_up(name, email, password, contact_number):
    """Create a new account"""

    # TODO: check working of:
    # pattern = r"/^[\w+-.]+@[a-z]+\.[a-z]+$"

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    regex = re.compile(pattern)
    # check 0 to end/return re.match object
    valid_email = regex.fullmatch(email)

    # create a/c if credentials are valid
    if valid_email:
        client = Client(
            client_name=name,
            email=email,
            password=password,
            contact_number=contact_number
        )

        # insert to db
        session.add(client)
        session.commit()
        click.secho(("Account created successfully! 😁"), fg="green")
        # TODO: invoke home_page after successful signup
        home_page(client.client_id)
        session.close()
    else:
        click.secho(("Invalid email address! 🙃 Please try again."), fg="red")


if __name__ == "__main__":
    welcome()


'''
Sign Up:
client_name 
email
password
contact_number
Validate email format and confirm password.
Store in database.

Login:
email
password
Validate against the stored information in the database.
If valid, allow access

Homepage:
Display services offered

Task Selection:
Allow client to select service from menu
Retrieve and display relevant information about task
proceed to checkout

'''
