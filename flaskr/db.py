import os
import psycopg
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            host=os.getenv('HOST'),
            port=os.getenv('PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    curr = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        curr.execute(f.read().decode('utf8'))
    
    curr.close()
    db.commit()


@click.command('init-db')
def init_db_command():
    """Create new tables if not exist."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)