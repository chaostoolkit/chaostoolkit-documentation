# Extension `chaoshumio`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.5.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-humio |



[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-humio)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-humio.svg)](https://www.python.org/)

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

## Humio Token

To use this extension, you will need one piece of information from Humio, the
[API token][token] for a user.

[token]: https://cloud.humio.com/docs/http-api/index.html#api-token

## Usage

This extension can be used a control on the experiment or a notification
plugin of the Chaos Toolkit CLI itself. Usually, only one of these two methods
is used at any given time as they serve similar purpose but feel free to
combine them. The control approach is deeper because it logs down to the
activity whereas notifications are much higher level.

This extension can also be used as a probe to fetch information from Humio.

### Query Log Events

To use this extension as a probe as part of your experiment, use it as
follows:

```json
{
  "configuration": {
    "humio_url": {
      "type": "env",
      "key": "HUMIO_URL",
      "default": "https://cloud.humio.com"
    },
    "humio_repository": {
      "type": "env",
      "key": "HUMIO_REPOSITORY",
      "default": "sandbox"
    }
  },
  "secrets": {
    "humio": {
      "token": {
        "type": "env",
        "key": "HUMIO_TOKEN"
      }
    }
  },
  "steady-state-hypothesis": {
    "title": "Running experiment",
    "probes": [
      {
        "name": "run-humio-search-query",
        "type": "probe",
        "provider": {
          "type": "python",
          "module": "chaoshumio.probes",
          "func": "search_query",
          "secrets": [
            "humio"
          ],
          "arguments": {
            "qs": "count(as=_count)",
            "start": "24hours",
            "end": "now"
          }
        },
        "tolerance": {
          "name": "humio-query-result-value-greater-than",
          "type": "probe",
          "provider": {
            "type": "python",
            "module": "chaoshumio.tolerances",
            "func": "field_value_above",
            "arguments": {
              "field": "_count",
              "lower": 1
            }
          }
        }
      }
    ]
  }
}
```

In this example, we are using the `search_query` probe and validate it with
a specific tolerance that can inspect the returned payload from Humio and
ensure each value matches the required expectations.

### Notification

To use this extension to push notifications, edit your
[chaostoolkit settings][settings] by adding the following payload:

[settings]: https://docs.chaostoolkit.org/reference/usage/cli/#configure-the-chaos-toolkit

```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    humio_url: https://myhumio.company.com
    token: my-token
```

By default all events will be forwarded to that channel. You may filter only
those events you care for:


```yaml
notifications:
  -
    type: plugin
    module: chaoshumio.notification
    humio_url: https://myhumio.company.com
    token: my-token
    events:
      - run-failed
      - run-started
```

Only sends those two events.

### Control

To use this extension as a control over the experiment and send logs during
the execution of the experiment to `https://cloud.humio.com`, add the following
payload to your experiment:

```json
{
    "secrets": {
        "humio": {
            "token": {
                "type": "env",
                "key": "HUMIO_INGEST_TOKEN"
            }
        }
    },
    "controls": [
        {
            "name": "humio-logger",
            "provider": {
                "type": "python",
                "module": "chaoshumio.control",
                "secrets": ["humio"]
            }
        }
    ]
}
```

If you want to send logs to a different Humio URL endpoint, specify the
`humio_url` configuration parameter. The following shows how this parameter:

```json
{
    "secrets": {
        "humio": {
            "token": {
                "type": "env",
                "key": "HUMIO_INGEST_TOKEN"
            }
        }
    },
    "configuration": {
        "humio_url": "https://myhumio.company.com"
    },
    "controls": [
        {
            "name": "humio-logger",
            "provider": {
                "type": "python",
                "module": "chaoshumio.control",
                "secrets": ["humio"]
            }
        }
    ]
}
```

This will ensure the results of the experiment, steady-state, method, rollbacks
and each activity are sent to Humio. The experiment itself will also be
send initially.

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

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```



## Exported Controls
This package exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment**               | True | True |
| **Steady-state Hypothesis**  | False | True |
| **Method**                   | False | True |
| **Rollback**                 | False | True |
| **Activities**               | False | True |

To use this control module, please add the following section to your experiment:

```json
{
  "name": "chaoshumio",
  "provider": {
    "type": "python",
    "module": "chaoshumio.control"
  }
}
```

```yaml
name: chaoshumio
provider:
  module: chaoshumio.control
  type: python

```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.



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
- `"humio_url"`: the Humio endpoint to send the event to

If token is missing, no notification is sent. If humio_url is not
specified then the default, https://cloud.humio.com, will be used.

**Signature:**

```python
('def notify(settings: Dict[str, Any], event: Dict[str, Any]):\n    pass\n',)
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




### probes



***

#### `search_query`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaoshumio.probes |
| **Name**              | search_query |
| **Return**              | Any |


Perform a search query against the Humio API and returns its result as-is.

Set `result_as_text` to `true` to get the result as a raw string, otherwise
the probe returns a JSON payload.

Make sure to set the Humio token as part of the experiment secrets and
the repository name as part of its configuration section using the
`humio_repository` key.

See https://docs.humio.com/api/using-the-search-api-with-humio/#query

**Signature:**

```python
("def search_query(qs: str,\n                 start: Union[int, str] = '24hours',\n                 end: Union[int, str] = 'now',\n                 tz_offset: int = 0,\n                 params: Union[str, Dict[str, str]] = None,\n                 result_as_text: bool = False,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None) -> Any:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **qs**      | string |  | Yes |
| **start**      | object | "24hours" | No |
| **end**      | object | "now" | No |
| **tz_offset**      | integer | 0 | No |
| **params**      | object | null | No |
| **result_as_text**      | boolean | false | No |




**Usage:**

```json
{
  "name": "search-query",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaoshumio.probes",
    "func": "search_query",
    "arguments": {
      "qs": ""
    }
  }
}
```

```yaml
name: search-query
provider:
  arguments:
    qs: ''
  func: search_query
  module: chaoshumio.probes
  type: python
type: probe

```




### tolerances



***

#### `field_value_above`

|                       |               |
| --------------------- | ------------- |
| **Type**              | tolerance |
| **Module**            | chaoshumio.tolerances |
| **Name**              | field_value_above |
| **Return**              | boolean |


Validate value at the given field to be above the given lower limit.

**Signature:**

```python
('def field_value_above(value: Any = None,\n                      field: str = None,\n                      lower: float = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **value**      | object | null | No |
| **field**      | string | null | No |
| **lower**      | number | null | No |



!!! info ""
    Tolerances declare the `value` argument which is automatically injected by
    Chaos Toolkit as the output of the probe they are evaluating.


**Usage:**

```json
{
  "steady-state-hypothesis": {
    "title": "...",
    "probes": [
      {
        "type": "probe",
        "tolerance": {
          "name": "field-value-above",
          "type": "tolerance",
          "provider": {
            "type": "python",
            "module": "chaoshumio.tolerances",
            "func": "field_value_above"
          }
        },
        "...": "..."
      }
    ]
  }
}
```

```yaml
steady-state-hypothesis:
  probes:
  - '...': '...'
    tolerance:
      name: field-value-above
      provider:
        func: field_value_above
        module: chaoshumio.tolerances
        type: python
      type: tolerance
    type: probe
  title: '...'

```



***

#### `field_value_between`

|                       |               |
| --------------------- | ------------- |
| **Type**              | tolerance |
| **Module**            | chaoshumio.tolerances |
| **Name**              | field_value_between |
| **Return**              | boolean |


Validate value at the given field to be between the lower/upper boundaries.

**Signature:**

```python
('def field_value_between(value: Any = None,\n                        field: str = None,\n                        lower: float = None,\n                        upper: float = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **value**      | object | null | No |
| **field**      | string | null | No |
| **lower**      | number | null | No |
| **upper**      | number | null | No |



!!! info ""
    Tolerances declare the `value` argument which is automatically injected by
    Chaos Toolkit as the output of the probe they are evaluating.


**Usage:**

```json
{
  "steady-state-hypothesis": {
    "title": "...",
    "probes": [
      {
        "type": "probe",
        "tolerance": {
          "name": "field-value-between",
          "type": "tolerance",
          "provider": {
            "type": "python",
            "module": "chaoshumio.tolerances",
            "func": "field_value_between"
          }
        },
        "...": "..."
      }
    ]
  }
}
```

```yaml
steady-state-hypothesis:
  probes:
  - '...': '...'
    tolerance:
      name: field-value-between
      provider:
        func: field_value_between
        module: chaoshumio.tolerances
        type: python
      type: tolerance
    type: probe
  title: '...'

```



***

#### `field_value_under`

|                       |               |
| --------------------- | ------------- |
| **Type**              | tolerance |
| **Module**            | chaoshumio.tolerances |
| **Name**              | field_value_under |
| **Return**              | boolean |


Validate value at the given field to be under the given upper limit.

**Signature:**

```python
('def field_value_under(value: Any = None,\n                      field: str = None,\n                      upper: float = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **value**      | object | null | No |
| **field**      | string | null | No |
| **upper**      | number | null | No |



!!! info ""
    Tolerances declare the `value` argument which is automatically injected by
    Chaos Toolkit as the output of the probe they are evaluating.


**Usage:**

```json
{
  "steady-state-hypothesis": {
    "title": "...",
    "probes": [
      {
        "type": "probe",
        "tolerance": {
          "name": "field-value-under",
          "type": "tolerance",
          "provider": {
            "type": "python",
            "module": "chaoshumio.tolerances",
            "func": "field_value_under"
          }
        },
        "...": "..."
      }
    ]
  }
}
```

```yaml
steady-state-hypothesis:
  probes:
  - '...': '...'
    tolerance:
      name: field-value-under
      provider:
        func: field_value_under
        module: chaoshumio.tolerances
        type: python
      type: tolerance
    type: probe
  title: '...'

```



