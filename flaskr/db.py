# SQLITE database engine
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# The first thing to do when working with a SQLite database is to create a connection to
# it. Any queries and operations are performed using the connection, which is closed after
# the work is finished.

# Function that gets the database object (using SQLITE)
def get_db():
    # g is a special object that is unique for each request - contains
    # important information about the request
    if 'db' not in g:
        # If the database has not been initialized, then do it
        g.db = sqlite3.connect(
            # Won't create/initiate the file until later
            current_app.config['DATABASE'], # Defined in __init__.py
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # Return the database as rows that acts like dictionary -- enables access by rows
        g.db.row_factory = sqlite3.Row

    # Returns the final db
    return g.db

# Closes the database
def close_db(e=None):
    # Gets a reference to the database variable (if it exists)
    db = g.pop('db', None)

    # If the database exists, close it.
    if db is not None:
        db.close()

# Initiate the database
def init_db():
    # This will create the new database instance
    db = get_db()

    # Load the database using the schema.sql file
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Defines a command line command call init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables
    init_db()

    # Send message to the CLI
    click.echo('Initialized the database.')

# Set app settings that will link the database with flask
def init_app(app):
    # Tells app to tell close_db() when cleaning up after returning response
    app.teardown_appcontext(close_db)

    # Adds the new cli command that can be called with the flask cli command
    app.cli.add_command(init_db_command)
