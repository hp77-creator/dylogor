import click

from . import commands


@click.group()
@click.version_option(version='0.0.1')
def cli():
    pass


cli.add_command(commands.search)
