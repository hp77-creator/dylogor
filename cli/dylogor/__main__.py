import click

from . import commands


@click.group()
@click.version_option(version='0.0.1')
def cli():
    pass


cli.add_command(commands.search)
cli.add_command(commands.search_regex)
cli.add_command(commands.search_timestamp)
cli.add_command(commands.intro)

