# Extension `chaoswm`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.2 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-wiremock |


=====================

[![Build Status](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-wiremock.svg?branch=master)](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-wiremock)
[![image](https://img.shields.io/pypi/v/chaostoolkit-wiremock.svg)](https://pypi.python.org/pypi/chaostoolkit-wiremock)

[Chaos Toolkit][chaostoolkit] driver for [WireMock][wiremock]. 

[chaostoolkit]: http://chaostoolkit.org
[wiremock]: http://wiremock.org/

Package installation
--------------------

To install the package from pypi.org:

    pip install -U chaostoolkit-wiremock

Installation from source
------------------------

In order to use it, you need python 3.5+ in your environment.
Once downloaded the project, cd into it and run:

    pip install -r requirements.txt -r requirements-dev.txt
    make clean && make test && make install

Configuration
-------------

The following keys can be configured in the experiment global
configuration section, under the \"wiremock\" key:

-   **host**: the wiremock server host
-   **port**: the wiremock server port
-   **contextPath**: the contextPath for your wiremock server (optional)
-   **timeout**: accepted timeout (defaults to 1 sec)
-   **down**: the delayDistribution section used by the `down` action

Configuration example:

    {
        "configuration": {
            "wiremock": {
                "host": "localhost",
                "port": 8080,
                "contextPath": "/wiremock",
                "timeout": 10,
                "down": {
                    "type": "lognormal",
                    "median": 3000,
                    "sigma": 0.2
                }
            }
        }
    }

Exported Actions
----------------

Adding a list of mappings:

    {
      "method": [
        {
          "type": "action",
          "name": "adding a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "add_mappings",
            "arguments": {
              "mappings": [{
                "request": {
                   "method": "GET",
                   "url": "/hello"
                },
                "response": {
                   "status": 200,
                   "body": "Hello world!",
                   "headers": {
                       "Content-Type": "text/plain"
                   }
                } 
              }]
            }
          }
        }
      ]
    }

Deleting a list of mappings:

    {
      "method": [
        {
          "type": "action",
          "name": "deleting a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "delete_mappings",
            "arguments": {
              "filter": [{
                 "method": "GET",
                 "url": "/hello"
              }]
            }
          }
        }
      ]
    }

Adding a global fixed delay:

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a global fixed delay",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "global_fixed_delay",
            "arguments": {
              "fixedDelay": 10
            }
          }
        }
      ]
    }

Adding a global random delay:

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a global random delay",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "global_random_delay",
            "arguments": {
              "delayDistribution": {
                "type": "lognormal",
                "median": 20,
                "sigma": 0.1
              }
            }
          }
        }
      ]
    }

Adding a fixed delay to a list of mappings:

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a fixed delay to a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "fixed_delay",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/hello1"
              }],
              "fixedDelayMilliseconds": 1000
            }
          }
        }
      ]
    }

Adding a random delay to a list of mappings:

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a random delay to a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "random_delay",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/hello2"
              }],
              "delayDistribution": {
                "type": "lognormal",
                "median": 2000,
                "sigma": 0.5
              }
            }
          }
        }
      ]
    }

Adding a ChunkedDribbleDelay to a list of mappings:

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a ChunkedDribbleDelay to a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "chunked_dribble_delay",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/hello"
              }],
              "chunkedDribbleDelay": {
                "numberOfChunks": 5,
                "totalDuration": 1000
              }
            }
          }
        }
      ]
    }

Taking a list of mappings down (heavy distribution delay). This action
will use the parameters specified in the \"down\" key of the
configuration section:

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "down",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/hello"
              }]
            }
          }
        }
      ]
    }

Taking a list of mappings up back again:

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "up",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/hello"
              }]
            }
          }
        }
      ]
    }

Resetting the wiremock server (deleting all mappings):

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "reset"
          }
        }
      ]
    }


### Experiments

The driver comes with an experiments directory where you can find snippets to test all APIs 
against a WireMock server listening on localhost:8080.


### Discovery

You may use the Chaos Toolkit to discover the capabilities of this
extension:

    $ chaos discover chaostoolkit-wiremock  --no-install

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.





## Exported Activities



### actions



***

#### `add_mappings`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | add_mappings |
| **Return**              | list |


adds more mappings to wiremock
returns the list of ids of the mappings added

**Signature:**

```python
('def add_mappings(mappings: List[Any],\n                 configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **mappings**      | list |  | Yes |




**Usage:**

```json
{
  "name": "add-mappings",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "add_mappings",
    "arguments": {
      "mappings": []
    }
  }
}
```

```yaml
name: add-mappings
provider:
  arguments:
    mappings: []
  func: add_mappings
  module: chaoswm.actions
  type: python
type: action

```



***

#### `chunked_dribble_delay`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | chunked_dribble_delay |
| **Return**              | list |


adds a chunked dribble delay to a list of mappings

**Signature:**

```python
('def chunked_dribble_delay(\n        filter: List[Any],\n        chunkedDribbleDelay: Mapping[str, Any],\n        configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |
| **chunkedDribbleDelay**      | object |  | Yes |




**Usage:**

```json
{
  "name": "chunked-dribble-delay",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "chunked_dribble_delay",
    "arguments": {
      "filter": [],
      "chunkedDribbleDelay": null
    }
  }
}
```

```yaml
name: chunked-dribble-delay
provider:
  arguments:
    chunkedDribbleDelay: null
    filter: []
  func: chunked_dribble_delay
  module: chaoswm.actions
  type: python
type: action

```



***

#### `delete_mappings`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | delete_mappings |
| **Return**              | list |


deletes a list of mappings
returns the list of ids of the mappings deleted

**Signature:**

```python
('def delete_mappings(\n        filter: List[Any],\n        configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |




**Usage:**

```json
{
  "name": "delete-mappings",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "delete_mappings",
    "arguments": {
      "filter": []
    }
  }
}
```

```yaml
name: delete-mappings
provider:
  arguments:
    filter: []
  func: delete_mappings
  module: chaoswm.actions
  type: python
type: action

```



***

#### `down`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | down |
| **Return**              | list |


set a list of services down
more correctly it adds a chunked dribble delay to the mapping
as defined in the configuration section (or action attributes)
Returns the list of delayed mappings

**Signature:**

```python
('def down(filter: List[Any],\n         configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |




**Usage:**

```json
{
  "name": "down",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "down",
    "arguments": {
      "filter": []
    }
  }
}
```

```yaml
name: down
provider:
  arguments:
    filter: []
  func: down
  module: chaoswm.actions
  type: python
type: action

```



***

#### `fixed_delay`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | fixed_delay |
| **Return**              | list |


adds a fixed delay to a list of mappings 

**Signature:**

```python
('def fixed_delay(filter: List[Any],\n                fixedDelayMilliseconds: int,\n                configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |
| **fixedDelayMilliseconds**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "fixed-delay",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "fixed_delay",
    "arguments": {
      "filter": [],
      "fixedDelayMilliseconds": 0
    }
  }
}
```

```yaml
name: fixed-delay
provider:
  arguments:
    filter: []
    fixedDelayMilliseconds: 0
  func: fixed_delay
  module: chaoswm.actions
  type: python
type: action

```



***

#### `global_fixed_delay`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | global_fixed_delay |
| **Return**              | integer |


add a fixed delay to all mappings 

**Signature:**

```python
('def global_fixed_delay(fixedDelay: int = 0,\n                       configuration: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **fixedDelay**      | integer | 0 | No |




**Usage:**

```json
{
  "name": "global-fixed-delay",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "global_fixed_delay"
  }
}
```

```yaml
name: global-fixed-delay
provider:
  func: global_fixed_delay
  module: chaoswm.actions
  type: python
type: action

```



***

#### `global_random_delay`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | global_random_delay |
| **Return**              | integer |


adds a random delay to all mappings 

**Signature:**

```python
('def global_random_delay(\n        delayDistribution: Mapping[str, Any],\n        configuration: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **delayDistribution**      | object |  | Yes |




**Usage:**

```json
{
  "name": "global-random-delay",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "global_random_delay",
    "arguments": {
      "delayDistribution": null
    }
  }
}
```

```yaml
name: global-random-delay
provider:
  arguments:
    delayDistribution: null
  func: global_random_delay
  module: chaoswm.actions
  type: python
type: action

```



***

#### `populate_from_dir`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | populate_from_dir |
| **Return**              | list |


adds all mappings found in the passed folder
returns the list of ids of the mappings added

**Signature:**

```python
("def populate_from_dir(\n        dir: str = '.',\n        configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **dir**      | string | "." | No |




**Usage:**

```json
{
  "name": "populate-from-dir",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "populate_from_dir"
  }
}
```

```yaml
name: populate-from-dir
provider:
  func: populate_from_dir
  module: chaoswm.actions
  type: python
type: action

```



***

#### `random_delay`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | random_delay |
| **Return**              | list |


adds a random delay to a list of mappings

**Signature:**

```python
('def random_delay(filter: List[Any],\n                 delayDistribution: Mapping[str, Any],\n                 configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |
| **delayDistribution**      | object |  | Yes |




**Usage:**

```json
{
  "name": "random-delay",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "random_delay",
    "arguments": {
      "filter": [],
      "delayDistribution": null
    }
  }
}
```

```yaml
name: random-delay
provider:
  arguments:
    delayDistribution: null
    filter: []
  func: random_delay
  module: chaoswm.actions
  type: python
type: action

```



***

#### `reset`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | reset |
| **Return**              | integer |


resets the wiremock server: deletes all mappings! 

**Signature:**

```python
('def reset(configuration: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |




**Usage:**

```json
{
  "name": "reset",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "reset"
  }
}
```

```yaml
name: reset
provider:
  func: reset
  module: chaoswm.actions
  type: python
type: action

```



***

#### `up`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoswm.actions |
| **Name**              | up |
| **Return**              | list |


deletes all delays connected with a list of mappings 

**Signature:**

```python
('def up(filter: List[Any],\n       configuration: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | list |  | Yes |




**Usage:**

```json
{
  "name": "up",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoswm.actions",
    "func": "up",
    "arguments": {
      "filter": []
    }
  }
}
```

```yaml
name: up
provider:
  arguments:
    filter: []
  func: up
  module: chaoswm.actions
  type: python
type: action

```




### probes



***

#### `mappings`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaoswm.probes |
| **Name**              | mappings |
| **Return**              | list |


None

**Signature:**

```python
('def mappings(c: Dict[str, Dict[str, str]] = None) -> List[Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **c**      | mapping | null | No |




**Usage:**

```json
{
  "name": "mappings",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaoswm.probes",
    "func": "mappings"
  }
}
```

```yaml
name: mappings
provider:
  func: mappings
  module: chaoswm.probes
  type: python
type: probe

```



***

#### `server_running`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaoswm.probes |
| **Name**              | server_running |
| **Return**              | integer |


None

**Signature:**

```python
('def server_running(c: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **c**      | mapping | null | No |




**Usage:**

```json
{
  "name": "server-running",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaoswm.probes",
    "func": "server_running"
  }
}
```

```yaml
name: server-running
provider:
  func: server_running
  module: chaoswm.probes
  type: python
type: probe

```




### utils



***

#### `can_connect_to`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoswm.utils |
| **Name**              | can_connect_to |
| **Return**              | boolean |


Test a connection to a host/port 

**Signature:**

```python
('def can_connect_to(host: str, port: int) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **host**      | string |  | Yes |
| **port**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "can-connect-to",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoswm.utils",
    "func": "can_connect_to",
    "arguments": {
      "host": "",
      "port": 0
    }
  }
}
```

```yaml
name: can-connect-to
provider:
  arguments:
    host: ''
    port: 0
  func: can_connect_to
  module: chaoswm.utils
  type: python
type: ''

```



***

#### `check_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoswm.utils |
| **Name**              | check_configuration |
| **Return**              | boolean |


None

**Signature:**

```python
('def check_configuration(c: Dict[str, Any] = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **c**      | mapping | null | No |




**Usage:**

```json
{
  "name": "check-configuration",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoswm.utils",
    "func": "check_configuration"
  }
}
```

```yaml
name: check-configuration
provider:
  func: check_configuration
  module: chaoswm.utils
  type: python
type: ''

```



***

#### `get_wm_params`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoswm.utils |
| **Name**              | get_wm_params |
| **Return**              | Union[Dict[str, Any], NoneType] |


None

**Signature:**

```python
('def get_wm_params(c: Dict[str, Any]) -> Union[Dict[str, Any], NoneType]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **c**      | mapping |  | Yes |




**Usage:**

```json
{
  "name": "get-wm-params",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoswm.utils",
    "func": "get_wm_params",
    "arguments": {
      "c": {}
    }
  }
}
```

```yaml
name: get-wm-params
provider:
  arguments:
    c: {}
  func: get_wm_params
  module: chaoswm.utils
  type: python
type: ''

```



