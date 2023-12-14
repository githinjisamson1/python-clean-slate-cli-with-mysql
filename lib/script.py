#! /usr/bin/env python3
# saves the hustle of having to run python3 lib/script.py


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

Display Task Information/similar to "receipt"
Retrieve and display detailed information of task selected
Task ID
Task Description
Assigned Cleaner
Task Status

'''
# cli made easier
import click

# working with regex
import re

from models import Client, session


def home_page():
    pass


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
@click.option('--password', '-p', prompt="Enter your password")
def sign_in(email, password):
    """Log in using email and password"""

    # filter using provided credentials
    user = session.query(Client).filter_by(
        email=email, password=password).first()

    if user:
        click.echo(user)
        click.secho(("Login successful! 😁"), fg="green")
        # TODO: invoke home_page after successful login
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
        session.close()
        click.secho(("Account created successfully! 😁"), fg="green")
        # TODO: invoke home_page after successful signup
    else:
        click.secho(("Invalid email address! 🙃 Please try again."), fg="red")
        # sign_up()


if __name__ == "__main__":
    welcome()

