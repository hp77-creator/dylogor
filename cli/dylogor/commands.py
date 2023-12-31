import json
import sys

import click
import requests


from requests import exceptions
from .utils import print_fancy_response, exception_handler, get_param, get_json_body, get_json_body_ts, asciiart


# interface for search
# dialoger search --level error
# dialoger search --traceId

@click.command()
@click.option("--level", type=click.Choice(
    [
        "error",
        "warn",
        "debug",
        "info"
    ]))
@click.option("--trace-id", help="traceId linked with your log", type=click.types.STRING)
@click.option("--message", help="message that is present in your log", type=click.types.STRING)
@click.option("--resource-id", help="resourceId of your log", type=click.types.STRING)
@click.option("--timestamp", help="yyyy-mm-ddThh:mm:ssZ", type=click.types.STRING)
@click.option("--span-id", help="spanId of your log", type=click.types.STRING)
@click.option("--commit", help="commit of your log", type=click.types.STRING)
@click.option("--page", default=1, help="page number from which they want to see response", type=click.types.INT)
@click.option("--page-size", default=10, help="number of response to be shown per array", type=click.types.INT)
@click.pass_context
def search(ctx, level, trace_id, message, resource_id, timestamp, span_id, commit, page, page_size):
    del ctx.params['page']
    del ctx.params['page_size']
    if not any(ctx.params.values()):
        response = ""
        try:
            response = requests.get("http://localhost:3000/search-all", json={})
        except exceptions.ConnectionError as nce:
            exception_handler(nce)
        except exceptions.RequestException as re:
            exception_handler(re)

        print_fancy_response(response, page, page_size)
    else:

        params = get_param(level, trace_id, message, resource_id, timestamp, span_id, commit)
        response = ""
        try:
            response = requests.get("http://localhost:3000/search", json=params)
        except exceptions.ConnectionError as nce:
            exception_handler(nce)
        except exceptions.RequestException as re:
            exception_handler(re)

        print_fancy_response(response)


@click.command()
@click.option("--field", help="name of the field that you want to regex on", type=click.Choice([
    "message",
    "resourceId",
    "spanId",
    "commit",
    "level"
]))
@click.option("--expression", help="regex expression")
def search_regex(field, expression):
    json_body = get_json_body(field, expression)
    response = ""
    try:
        params = {"q": json.dumps(json_body)}
        response = requests.get("http://localhost:3000/search-reg", params=params)
    except exceptions.ConnectionError as nce:
        exception_handler(nce)
    except exceptions.RequestException as re:
        exception_handler(re)

    print_fancy_response(response)


@click.command()
@click.option("--startdate",
              help="Please enter your date in following format: 2023-09-15T00:00:00Z, if you enter 2023-09-15, time will be defaulted.")
@click.option("--enddate",
              help="Please enter your date in following format: 2023-09-15T00:00:00Z, if you enter 2023-09-15, time will be defaulted.")
def search_timestamp(startdate, enddate):
    json_body = get_json_body_ts(startdate, enddate)
    if json_body == -1:
        click.echo("Date is not given properly")
        click.echo("please use --help to know the format")
        sys.exit(1)
    response = ""
    try:
        params = {"q": json.dumps(json_body)}
        response = requests.get("http://localhost:3000/search-reg", params=params)
    except exceptions.ConnectionError as nce:
        exception_handler(nce)
    except exceptions.RequestException as re:
        exception_handler(re)

    print_fancy_response(response)


@click.command()
def intro():
    """
    Welcome to Your CLI Tool!

    This tool helps you manage and analyze logs efficiently.

    Get started with the following commands:
    - Use 'search' to query logs.
    - Explore 'stats' for log statistics.
    - Check 'help' for more options and information.

    Happy logging!
    """
    click.echo(click.style("============================================", fg="blue"))
    # click.echo(click.style("           Welcome to Dylogor CLI Tool         ", fg="blue", bold=True))
    click.echo(click.style(asciiart, fg="cyan"))
    click.echo(click.style("============================================", fg="blue"))

    click.echo("\nThis tool helps you manage and analyze logs efficiently.\n")
    click.echo("Get started with the following commands:")
    click.echo("- Use 'search' to query logs.")
    click.echo("- Check 'help' for more options and information.\n")

    click.echo(click.style("Happy logging!", fg="green", bold=True))
