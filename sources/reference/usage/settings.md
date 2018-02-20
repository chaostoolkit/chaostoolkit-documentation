# Configure the Chaos Toolkit

For the most part, the Chaos Toolkit does not necessitate to be configured.
These settings are stored in a YAML file on your local machine.

!!! tip
    Unless you enable one of the features requiring extra configuration,
    you don't need to create that file.

## Create The Settings File

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

## Features Settings

The settings file entries depend on which features you wish to enable.

### Notification

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
