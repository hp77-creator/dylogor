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


def print_fancy_response(response, page_start=1, page_end=10):
    if response.status_code == 200:
        response_arr = response.json()
        page_size = min(page_end, len(response_arr))
        start_index = (page_start - 1) * page_size
        end_index = start_index + page_size
        page_data = response_arr[start_index: end_index]
       # click.echo(f'Page {page_start}/{len(page_data)//page_size + 1}')
        for elems in page_data:
            res_new = elems['_source']
            click.echo("\n")
            for key in res_new:
                if key == 'level':
                    level_value = res_new[key]
                    if level_value == 'error':
                        click.echo(click.style(f"{key} -> {level_value}", fg="red"))
                    elif level_value == 'warn':
                        click.echo(click.style(f"{key} -> {level_value}", fg="yellow"))
                    elif level_value == 'info':
                        click.echo(click.style(f"{key} -> {level_value}", fg="green"))
                    elif level_value == 'debug':
                        click.echo(click.style(f"{key} -> {level_value}", fg="bright_yellow"))
                else:
                    click.echo(click.style(f"{key} -> {res_new[key]}", fg="cyan"))
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
@click.option("--page", default=1,help="page number from which they want to see response", type=click.types.INT)
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
