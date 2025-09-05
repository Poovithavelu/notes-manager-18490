from flask.cli import with_appcontext
import click
from .models import db


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database by creating all tables."""
    db.create_all()
    click.echo("Initialized the database.")
