# Extension `chaosspring`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.2.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-spring |



[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-spring.svg)](https://www.python.org/) [![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-spring.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-spring)


This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
pip install -U chaostoolkit-spring
```

## Usage

Currently this driver supports interactions with a [Spring Boot-based](https://spring.io/projects/spring-boot) service that has included the [2.0.0.-SNAPSHOT](https://codecentric.github.io/chaos-monkey-spring-boot/2.0.0-SNAPSHOT/) release of the [Chaos Monkey for Spring Boot](https://github.com/codecentric/chaos-monkey-spring-boot). This snapshot includes the necessary Spring Boot Actuator HTTP endpoints so that the Chaos Toolkit to interact with the chaos features at runtime.

Once you have [added the Chaos Monkey for Spring Boot](https://codecentric.github.io/chaos-monkey-spring-boot/2.0.0-SNAPSHOT/#getting-started) and [enabled the Spring Boot Actuator HTTP endpoints](https://codecentric.github.io/chaos-monkey-spring-boot/2.0.0-SNAPSHOT/#endpoints) you can then use the probes and actions from this driver.

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "name": "enable_chaosmonkey",
    "provider": {
        "arguments": {
            "base_url": "http://localhost:8080/actuator"
        },
        "func": "enable_chaosmonkey",
        "module": "chaosspring.actions",
        "type": "python"
    },
    "type": "action"
}
```

This will interact with the specified service and enable the Chaos Monkey features. You can also turn off the Chaos Monkey if you wish by specifying the following action:

```json
{
    "name": "disable_chaosmonkey",
    "provider": {
        "arguments": {
            "base_url": "http://localhost:8080/actuator"
        },
        "func": "disable_chaosmonkey",
        "module": "chaosspring.actions",
        "type": "python"
    },
    "type": "action"
}
```

You can then manipulate the [Chaos Monkey assaults](https://codecentric.github.io/chaos-monkey-spring-boot/2.0.0-SNAPSHOT/#assaults) active on your service by specifing the following action:

```json
{
    "name": "configure_assaults",
    "provider": {
        "arguments": {
            "base_url": "http://localhost:8080/actuator",
            "assaults_configuration": {
                "level": 5,
                "latencyRangeStart": 2000,
                "latencyRangeEnd": 5000,
                "latencyActive": false,
                "exceptionsActive": false,
                "killApplicationActive": true,
                "restartApplicationActive": false
            }
        },
        "func": "change_assaults_configuration",
        "module": "chaosspring.actions",
        "type": "python"
    },
    "type": "action"
}
```

That's it!

Please explore the code to use further probes and actions.

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
pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
pytest
```





## Exported Activities



### actions



***

#### `change_assaults_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | change_assaults_configuration |
| **Return**              | string |


Change Assaults configuration on a specific service.

**Signature:**

```python
('def change_assaults_configuration(\n        base_url: str,\n        assaults_configuration: Dict[str, Any],\n        headers: Dict[str, Any] = None,\n        timeout: float = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> str:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **assaults_configuration**      | mapping |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "change-assaults-configuration",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "change_assaults_configuration",
    "arguments": {
      "base_url": "",
      "assaults_configuration": {}
    }
  }
}
```

```yaml
name: change-assaults-configuration
provider:
  arguments:
    assaults_configuration: {}
    base_url: ''
  func: change_assaults_configuration
  module: chaosspring.actions
  type: python
type: action

```



***

#### `disable_chaosmonkey`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | disable_chaosmonkey |
| **Return**              | string |


Disable Chaos Monkey on a specific service.

**Signature:**

```python
('def disable_chaosmonkey(base_url: str,\n                        headers: Dict[str, Any] = None,\n                        timeout: float = None,\n                        configuration: Dict[str, Dict[str, str]] = None,\n                        secrets: Dict[str, Dict[str, str]] = None) -> str:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "disable-chaosmonkey",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "disable_chaosmonkey",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: disable-chaosmonkey
provider:
  arguments:
    base_url: ''
  func: disable_chaosmonkey
  module: chaosspring.actions
  type: python
type: action

```



***

#### `enable_chaosmonkey`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | enable_chaosmonkey |
| **Return**              | string |


Enable Chaos Monkey on a specific service.

**Signature:**

```python
('def enable_chaosmonkey(base_url: str,\n                       headers: Dict[str, Any] = None,\n                       timeout: float = None,\n                       configuration: Dict[str, Dict[str, str]] = None,\n                       secrets: Dict[str, Dict[str, str]] = None) -> str:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "enable-chaosmonkey",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "enable_chaosmonkey",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: enable-chaosmonkey
provider:
  arguments:
    base_url: ''
  func: enable_chaosmonkey
  module: chaosspring.actions
  type: python
type: action

```




### probes



***

#### `assaults_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | assaults_configuration |
| **Return**              | mapping |


Get the current assaults configuration from the specified service.

**Signature:**

```python
('def assaults_configuration(\n        base_url: str,\n        headers: Dict[str, Any] = None,\n        timeout: float = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "assaults-configuration",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "assaults_configuration",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: assaults-configuration
provider:
  arguments:
    base_url: ''
  func: assaults_configuration
  module: chaosspring.probes
  type: python
type: probe

```



***

#### `chaosmonkey_enabled`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | chaosmonkey_enabled |
| **Return**              | boolean |


Enquire whether Chaos Monkey is enabled on the
specified service.

**Signature:**

```python
('def chaosmonkey_enabled(base_url: str,\n                        headers: Dict[str, Any] = None,\n                        timeout: float = None,\n                        configuration: Dict[str, Dict[str, str]] = None,\n                        secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "chaosmonkey-enabled",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "chaosmonkey_enabled",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: chaosmonkey-enabled
provider:
  arguments:
    base_url: ''
  func: chaosmonkey_enabled
  module: chaosspring.probes
  type: python
type: probe

```



***

#### `watcher_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | watcher_configuration |
| **Return**              | mapping |


Get the current watcher configuration from the specified service.

**Signature:**

```python
('def watcher_configuration(\n        base_url: str,\n        headers: Dict[str, Any] = None,\n        timeout: float = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **headers**      | mapping | null | No |
| **timeout**      | number | null | No |




**Usage:**

```json
{
  "name": "watcher-configuration",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "watcher_configuration",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: watcher-configuration
provider:
  arguments:
    base_url: ''
  func: watcher_configuration
  module: chaosspring.probes
  type: python
type: probe

```



