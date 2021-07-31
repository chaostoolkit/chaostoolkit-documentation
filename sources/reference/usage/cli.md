The heart of the Chaos Toolkit is the `chaos` command line.

!!! note "Activate the Python virtual environment"

    If you run the Chaos Toolkit directly, rather than using a container,
    always ensure you have activated the virtual environment so that it can
    be found along its dependencies:

    ```
    source ~/.venvs/chaostk/bin/activate
    ```

Once [installed](install.md), the Chaos Toolkit CLI will display the commands it supports 
by executing:

```
chaos --help
```
```
Usage: chaos [OPTIONS] COMMAND [ARGS]...

Options:
  --version                   Show the version and exit.
  --verbose                   Display debug level traces.
  --no-version-check          Do not search for an updated version of the
                              chaostoolkit.
  --change-dir TEXT           Change directory before running experiment.
  --no-log-file               Disable logging to file entirely.
  --log-file TEXT             File path where to write the command's log.
                              [default: chaostoolkit.log]
  --log-format [string|json]  Console logging format: string, json.
  --settings TEXT             Path to the settings file.  [default:
                              /Users/ciaran/.chaostoolkit/settings.yaml]
  --help                      Show this message and exit.

Commands:
  discover  Discover capabilities and experiments.
  info      Display information about the Chaos Toolkit environment.
  init      Initialize a new experiment from discovered capabilities.
  run       Run the experiment loaded from SOURCE, either a local file or...
  settings  Read, write or remove from your settings file.
  validate  Validate the experiment at SOURCE.
```

## Configure the Chaos Toolkit

For the most part, the Chaos Toolkit does not need to be configured.
However, if it does, the settings are stored in a YAML file on your local machine.

!!! tip
    Unless you enable one of the features requiring extra configuration,
    you don't need to create that file. If a feature requires extra configuration,
    its documentation will say so.

### Create the settings file

The settings file for the Chaos Toolkit should be located under the following
path:

```
$HOME/.chaostoolkit/settings.yaml
```

As this file may hold sensitive data, it is advised to make it readable only
for your own user:

```
chmod 600 $HOME/.chaostoolkit/settings.yaml
```

## How to Investigate Issues

When your experiment fails to work as you would expect, you should start
looking at the `chaostoolkit.log` file written to by the `chaos` command.

This file contains a lot of traces from the Chaos Toolkit core but also any
extensions that used the toolkit's logger.

As new logs are appended to that file, it may grow big. Do not hesitate to
wipe it out from time to time.

Please, do make sure to visit our [Slack][slack] or [GitHub][gh] when you have
a question around how the toolkit does things. The community will be pleased
to help you out.

[slack]: https://join.chaostoolkit.org/
[gh]: https://github.com/chaostoolkit
