<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/qf8ab2dXoTWAmEkozneFCKvc6.js" id="asciicast-qf8ab2dXoTWAmEkozneFCKvc6" async data-autoplay="true"></script></div>

The heart of the Chaos Toolkit is the `chaos` command line.

!!! note "Activate the Python virtual environment"

    If you run the Chaos Toolkit directly, rather than using a container,
    always ensure you have activated the virtual environment so that it can
    be found along its dependencies:

    ```
    $ source ~/.venvs/chaostk/bin/activate
    (chaostk) $
    ```

Once [installed](install.md), the Chaos Toolkit CLI will display the commands it supports 
by executing:

```
(chaostk) $ chaos --help
```

## Configure the Chaos Toolkit

For the most part, the Chaos Toolkit does not necessitate to be configured.
These settings are stored in a YAML file on your local machine.

!!! tip
    Unless you enable one of the features requiring extra configuration,
    you don't need to create that file.

### Create The Settings File

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

### Features Settings

The settings file entries depend on which features you wish to enable.

#### Notification

If you want to get notified of the Chaos Toolkit events, you should set the
following section:

```
notifications:
 -
  type: http
  url: https://mystuff.com/api
  verify_tls: false
  headers:
    Auth: "Bearer 1234"
```

This entry is a list of mapping. Each item of this list defines one channel
of notification, and potentially which events this channel should receive.

Please refer to the [notifications](notification.md) section for more
information.

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