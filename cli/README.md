## CLI Tool

### Installation

- Create a virtual environment using `virtualenv`. I used `pyenv-virtualenv`
- Follow the below commands

(Assuming you have created a virtual environment)

```shell
source venv/bin/activate
cd cli
python -m pip install -e .
```

Hurray `dylogor` is installed in your virtualenv
you can run it by following below steps

```shell

Usage: dylogor [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  search
  search-regex
  search-timestamp
```


```shell
Usage: dylogor search [OPTIONS]

Options:
  --level [error|warn|debug|info]
  --trace-id TEXT                 traceId linked with your log
  --message TEXT                  message that is present in your log
  --resource-id TEXT              resourceId of your log
  --timestamp TEXT                yyyy-mm-ddThh:mm:ssZ
  --span-id TEXT                  spanId of your log
  --commit TEXT                   commit of your log
  --page INTEGER                  page number from which they want to see
                                  response
  --page-size INTEGER             number of response to be shown per array
  --help                          Show this message and exit.

```

```shell
Usage: dylogor search-regex [OPTIONS]

Options:
  --field [message|resourceId|spanId|commit|level]
                                  name of the field that you want to regex on
  --expression TEXT               regex expression
  --help                          Show this message and exit.

```

```shell
Usage: dylogor search-timestamp [OPTIONS]

Options:
  --startdate TEXT  Please enter your date in following format:
                    2023-09-15T00:00:00Z, if you enter 2023-09-15, time will
                    be defaulted.
  --enddate TEXT    Please enter your date in following format:
                    2023-09-15T00:00:00Z, if you enter 2023-09-15, time will
                    be defaulted.
  --help            Show this message and exit.
```

Reference: [Real Python help to install cli tool locally](https://realpython.com/python-click/#preparing-a-click-app-for-installation-and-use)