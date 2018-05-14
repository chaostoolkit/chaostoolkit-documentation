# Extension `chaoshumio`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-humio |


[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio)

This project is an extension for the Chaos Toolkit to target [Humio][humio].

[humio]: https://www.humio.com/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install -U chaostoolkit-humio
```

## Humio Dataspace & Token

To use this extension, you will need two pieces of information from Humio.
First, the dataspace which you want to send logs to. Second a [API token][token]
for an user with permissions to that space.

[token]: https://cloud.humio.com/docs/http-api/index.html#api-token

## Usage

To use this extension, edit your [chaostoolkit settings][settings] by adding the
following payload:

[settings]: http://chaostoolkit.org/reference/usage/settings/

```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    dataspace: my-space
    token: my-token
```

By default all events will be forwarded to that channel. You may filter only
those events you care for:


```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    dataspace: my-space
    token: my-token
    events:
      - run-failed
      - run-started
```

Only sends those two events.

## Test

To run the tests for the project execute the following:

```
$ pytest
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works


## Exported Activities



### notification



***

#### `notify`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoshumio.notification |
| **Name**              | notify |
| **Return**              | None |


Send a log message to the Humio ingest endpoint.

The settings must contain:

- `"token"`: a slack API token
- `"url"`: the channel where to send this event notification

If one of these two attributes is missing, no notification is sent.

**Signature:**

```python
def notify(settings: Dict[str, Any], event: Dict[str, Any]):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **settings**      | mapping |  | Yes |
| **event**      | mapping |  | Yes |


**Usage:**

```json
{
  "name": "notify",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoshumio.notification",
    "func": "notify",
    "arguments": {
      "settings": {},
      "event": {}
    }
  }
}
```

```yaml
name: notify
provider:
  arguments:
    event: {}
    settings: {}
  func: notify
  module: chaoshumio.notification
  type: python
type: ''

```


