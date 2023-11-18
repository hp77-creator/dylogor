import json
import sys

import click
import time
import requests
from requests import exceptions


@click.group()
@click.version_option(version='0.0.1')
def cli():
    pass


def progress_animation():
    """Simulate a long-running task."""
    with click.progressbar(range(10), label='Processing') as bar:
        for _ in bar:
            time.sleep(0.5)


# interface for search
# dialoger search --level error
@click.command()
@click.option("--level", type=click.Choice(
        [
            "error",
            "warn",
            "debug",
            "info"
        ]))
def search(level):
    params = {"level": level}
    response = ""
    try:
        response = requests.get("http://localhost:3000/search", json=params)
    except exceptions.ConnectionError as nce:
        click.echo(click.style(f"NewConnectionError: {nce}", fg="red"))
        sys.exit(1)
    except exceptions.RequestException as re:
        click.echo(click.style(f"RequestExceptionError: {re}", fg="red"))
        sys.exit(1)

    if response.status_code == 200:
        res = response.json()[0]
        res_new = res['_source']
        for key in res_new:
            click.echo(click.style(f"{key} -> {res_new[key]}", fg="blue"))

#        click.echo(click.style(res, fg="blue"))
    else:
        click.echo(click.style(f"Server says you are using foul language", fg="yellow"))


cli.add_command(search)

if __name__ == "__main__":
    cli()
