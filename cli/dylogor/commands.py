import sys
import time

import click
import requests
from requests import exceptions


def progress_animation():
    """Simulate a long-running task."""
    with click.progressbar(range(10), label='Processing') as bar:
        for _ in bar:
            time.sleep(0.5)


def print_fancy_response(response):
    if response.status_code == 200:
        try:
            res = response.json()[0]
        except IndexError as e:
            exception_handler("Empty response from server")
        res_new = res['_source']
        for key in res_new:
            click.echo(click.style(f"{key} -> {res_new[key]}", fg="blue"))

    #        click.echo(click.style(res, fg="blue"))
    else:
        click.echo(click.style(f"Server says you are using foul language", fg="yellow"))


def exception_handler(exception):
    click.echo(click.style(f"Error: {exception}", fg="red"))
    sys.exit(1)


def get_param(level, trace_id, message, resource_id, timestamp, span_id, commit):
    if level is not None:
        return {"level": level}
    elif trace_id is not None:
        return {"traceId": trace_id}
    elif message is not None:
        return {"message": message}
    elif resource_id is not None:
        return {"resourceId": resource_id}
    elif timestamp is not None:
        return {"timestamp": timestamp}
    elif span_id is not None:
        return {"spanId": span_id}
    elif commit is not None:
        return {"commit": commit}
    else:
        return None


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
@click.pass_context
def search(ctx, level, trace_id, message, resource_id, timestamp, span_id, commit):
    if not any(ctx.params.values()):
        click.echo(ctx.get_help())
        sys.exit(1)
    params = get_param(level, trace_id, message, resource_id, timestamp, span_id, commit)
    response = ""
    try:
        response = requests.get("http://localhost:3000/search", json=params)
    except exceptions.ConnectionError as nce:
        exception_handler(nce)
    except exceptions.RequestException as re:
        exception_handler(re)

    print_fancy_response(response)
