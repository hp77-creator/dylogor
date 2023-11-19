
import click
import sys
import re

from datetime import date, timedelta


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


def get_json_body(field, expression):
    query_object = {
        "query_string": {
            "query": expression,
            "default_field": field
        }
    }
    return query_object


def get_json_body_ts(from_, to_):
    if from_ is None and to_ is not None:
        from_ = date.today().strftime("%Y-%m-%d")
    elif to_ is None and from_ is not None:
        to_ = date.today().strftime("%Y-%m-%d")
    else:
        to_ = date.today()
        from_ = to_ - timedelta(1)
        to_ = to_.strftime("%Y-%m-%d")
        from_ = from_.strftime("%Y-%m-%d")
    try:
        to_ = fix_ts(to_)
        from_ = fix_ts(from_)
        if not check_valid_ts(to_):
            raise ValueError
        if not check_valid_ts(from_):
            raise ValueError
    except ValueError as ve:
        return -1
    query_object = {
        "query_string": {
            "query": f"[{from_} TO {to_}]",
            "default_field": "timestamp"
        }
    }
    return query_object


def fix_ts(ts):
    if not check_valid_ts(ts):
        ts += "T00:00:00Z"
        return ts
    else:
        return ts


def check_valid_ts(ts):
    """
    Function to check if timestamp is in 2023-09-15T00:00:00Z format or not
    :param ts:
    :return bool:
    """
    # Define a regex pattern for the date format 'YYYY-MM-DDTHH:MM:SSZ'
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

    # Check if the string matches the pattern
    return bool(pattern.match(ts))
