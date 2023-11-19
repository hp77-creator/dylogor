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
  --help                          Show this message and exit.

```

Reference: [Real Python help to install cli tool locally](https://realpython.com/python-click/#preparing-a-click-app-for-installation-and-use)