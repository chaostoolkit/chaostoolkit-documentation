# Extension `chaostoxi`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.2.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-toxiproxy |



[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-toxiproxy.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/haostoolkit-toxiproxy)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-toxiproxy.svg)](https://www.python.org/)

Welcome to the [Chaos Toolkit][chaostoolkit] driver for [Toxiproxy][toxiproxy]! This extension allows you to setup toxy proxy probes and methods from chaostoolkit by leveraging the toxyproxy [http management api](https://github.com/Shopify/toxiproxy#http-api). 

[toxiproxy]: https://github.com/Shopify/toxiproxy
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
pip install -U chaostoolkit-toxiproxy
```

## Usage

### Configuration

To start using the actions and probes all you need to do is add the toxiproxy host with "toxiproxy_host" as the key, and optionally the port with "toxiproxy_port" as the key, to the configuration section in your experiment json. If not provided the port defaults to 8474.

Example in experiment.json

```json
"configuration": {
    "toxiproxy_host" : "10.124.23.183",
    "some_environment_variable": {
      "type": "environment",
      "key": "ENVIRONMENT_VARIABLE"
    }
  },
```

This extension follows the toxiproxy rules. A proxy is the channel where toxicity can be added. For this reason the extension is broken into proxy management and toxic management. 

All actions and probes in the extension are of python type and are used like any other python extension.

### Proxy actions

#### create_proxy

Creates a proxy to which toxics can be added. In toxiproxy a listen port of value 0 tells the API to assign a random available port. The value where the proxy is listenting will be attached to the **chaostoolkit configuration object** as *\<proxyname\>_PORT*. Should the creation of the proxy fail, an assertion error is raised stopping all subsequent actions.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|
|upstream_host|ip address of the host to send traffic to|Yes|None|
|upstream_port|port of the application to send traffic to|Yes|None|
|listen_host| IP address to bind where toxiproxy listens|No| 0.0.0.0|
|listen_port|port to listen for requests, 0 means pick random value|No|0|
|enabled| Whether to start listening or not|No|True|

#### modify_proxy

Modify the configuration of a given proxy. Useful to change the upstream configuration. Only arguments supplied result in modification of the proxy.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|
|listen_addres|ip:port address to modify|No|None|
|upstream_addres|ip:port of the upstream|No|None|
|enabled| Toggle enabled/disabled state|No|None|

#### disable_proxy

Disables the proxy, this is useful to simulate a proxied service being down.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy to disable|Yes|None|


#### enable_proxy

Enables a disabled proxy.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy to enable|Yes|None|

#### delete_proxy

Removes the proxy from the system.

Example usage

```json
 "method": [
      {
            "type": "action",
            "name": "setup_toxiproxy_proxy",
            "provider": {
                "type": "python",
                "module": "chaostoxi.proxy.actions",
                "func": "create_proxy",
                "arguments": {
                    "proxy_name": "myproxy",
                    "listen_port" : 6666,
                    "upstream_host" : "10.28.188.118",
                    "upstream_port" : 6040
                }
            },
            "pauses": {
                "after": 1
            }
        }
      ] 
```

#### reset

Enable all proxies and remove all active toxics.

Example usage:  
```json
"method": [
    {
        "type": "action",
        "name": "reset all proxies",
        "provider": {
            "type": "python",
            "module": "chaostoxi.proxy.actions",
            "func": "reset"
        },
        "pauses": {
            "after": 1
        }
    }
]
```

### Proxy probes

#### proxy_exist

Returns True of False if a given proxy exists.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|


### Toxic actions
All actions provided by this extension match the types and attributes of [toxics](https://github.com/Shopify/toxiproxy#toxics). 

#### create\_toxic

Allows you to create any of the supported types of toxics with their attributes. 

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|toxic_type|A valid toxic type|Yes|None|
|stream| The direction of the toxic "upstream" or "downstream"|No|downstream|
|toxicity|Percentage of toxiciy 1.0 is 100%, 0.5 is 50% etc| No| 1.0|
|attributes|Dictionary of attributes for the type of toxic|No|None|

#### create\_latency\_toxic

Add a delay to all data going through the proxy using a downstream with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|latency| time in milliseconds to add for latency| Yes|None|
|jitter| time in milliseconds to jitter|No|0

#### create\_bandwith\_degradation\_toxic

Limit the bandwith of a  downstream connection with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|rate| desired bandwith rate in KB/s| Yes|None|

#### create\_slow\_connection\_close\_toxic

Generate as downstream delayed TCP close with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|delay| desired close delay in milliseconds| Yes|None|

#### create\_slicer\_toxic

Slices TCP data up into small bits, optionally adding a delay between each sliced "packet" with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|average_size| size in bytes for the average package| Yes|None|
|size_variation| variation in bytes of an average pkg (should be smaller than average_size)|Yes|None
|delay| time in microseconds to delay each packet by|Yes|None

#### create\_limiter\_toxic

Closes connections when transmitted data after the limit, sets it up as a downstream, 100% toxicity.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|bytes| number of bytes to transmit before connection is closed| Yes|None|

#### delete\_toxic

Deletes the a given toxic.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|

Example usage:

```json
 "method": [        
      {
            "type": "action",
            "name": "create_latency_toxic",
            "provider": {
                "type": "python",
                "module": "toxiproxy.toxic.actions",
                "func": "create_downstream_latency_toxic",
                "arguments": {
                    "for_proxy": "edsproxy",
                    "toxic_name": "latency_toxic",
                    "latency": 5000,
                    "jitter": 200
                }
            },
            "pauses": {
                "after": 1
            }
        }    
 ]
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

To run the unit tests for the project execute the following:

```
pytest
```

To run the integration tests for the project execute the following:

```
tox
```





## Exported Activities



### proxy



***

#### `create_proxy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | create_proxy |
| **Return**              | None |


Creates a proxy to which toxics can be added.

**Signature:**

```python
("def create_proxy(proxy_name: str,\n                 upstream_host: str,\n                 upstream_port: int,\n                 listen_host: str = '0.0.0.0',\n                 listen_port: int = 0,\n                 enabled: bool = True,\n                 configuration: Dict[str, Dict[str, str]] = None):\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |
| **upstream_host**      | string |  | Yes |
| **upstream_port**      | integer |  | Yes |
| **listen_host**      | string | "0.0.0.0" | No |
| **listen_port**      | integer | 0 | No |
| **enabled**      | boolean | true | No |




**Usage:**

```json
{
  "name": "create-proxy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.actions",
    "func": "create_proxy",
    "arguments": {
      "proxy_name": "",
      "upstream_host": "",
      "upstream_port": 0
    }
  }
}
```

```yaml
name: create-proxy
provider:
  arguments:
    proxy_name: ''
    upstream_host: ''
    upstream_port: 0
  func: create_proxy
  module: chaostoxi.proxy.actions
  type: python
type: action

```



***

#### `delete_proxy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | delete_proxy |
| **Return**              | None |


Removes the proxy from the system.

**Signature:**

```python
('def delete_proxy(proxy_name: str,\n                 configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "delete-proxy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.actions",
    "func": "delete_proxy",
    "arguments": {
      "proxy_name": ""
    }
  }
}
```

```yaml
name: delete-proxy
provider:
  arguments:
    proxy_name: ''
  func: delete_proxy
  module: chaostoxi.proxy.actions
  type: python
type: action

```



***

#### `disable_proxy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | disable_proxy |
| **Return**              | None |


Disables the proxy, this is useful to simulate a proxied service being down.

**Signature:**

```python
('def disable_proxy(proxy_name: str,\n                  configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "disable-proxy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.actions",
    "func": "disable_proxy",
    "arguments": {
      "proxy_name": ""
    }
  }
}
```

```yaml
name: disable-proxy
provider:
  arguments:
    proxy_name: ''
  func: disable_proxy
  module: chaostoxi.proxy.actions
  type: python
type: action

```



***

#### `enable_proxy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | enable_proxy |
| **Return**              | None |


Enables a disabled proxy.

**Signature:**

```python
('def enable_proxy(proxy_name: str,\n                 configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "enable-proxy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.actions",
    "func": "enable_proxy",
    "arguments": {
      "proxy_name": ""
    }
  }
}
```

```yaml
name: enable-proxy
provider:
  arguments:
    proxy_name: ''
  func: enable_proxy
  module: chaostoxi.proxy.actions
  type: python
type: action

```



***

#### `get_proxy_attribute`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaostoxi.proxy.probes |
| **Name**              | get_proxy_attribute |
| **Return**              | None |


Returns an attribute of a specified proxy.

**Signature:**

```python
('def get_proxy_attribute(proxy_name: str,\n                        attribute: str,\n                        configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |
| **attribute**      | string |  | Yes |




**Usage:**

```json
{
  "name": "get-proxy-attribute",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.probes",
    "func": "get_proxy_attribute",
    "arguments": {
      "proxy_name": "",
      "attribute": ""
    }
  }
}
```

```yaml
name: get-proxy-attribute
provider:
  arguments:
    attribute: ''
    proxy_name: ''
  func: get_proxy_attribute
  module: chaostoxi.proxy.probes
  type: python
type: probe

```



***

#### `modify_proxy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | modify_proxy |
| **Return**              | None |


Modify the configuration of a given proxy.
Useful to change the upstream configuration.
Only arguments supplied result in modification of the proxy.

**Signature:**

```python
('def modify_proxy(proxy_name: str,\n                 listen_address: str = None,\n                 upstream_address: str = None,\n                 enabled: bool = None,\n                 configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |
| **listen_address**      | string | null | No |
| **upstream_address**      | string | null | No |
| **enabled**      | boolean | null | No |




**Usage:**

```json
{
  "name": "modify-proxy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.actions",
    "func": "modify_proxy",
    "arguments": {
      "proxy_name": ""
    }
  }
}
```

```yaml
name: modify-proxy
provider:
  arguments:
    proxy_name: ''
  func: modify_proxy
  module: chaostoxi.proxy.actions
  type: python
type: action

```



***

#### `proxy_exist`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaostoxi.proxy.probes |
| **Name**              | proxy_exist |
| **Return**              | None |


Returns True of False if a given proxy exists.

**Signature:**

```python
('def proxy_exist(proxy_name: str,\n                configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **proxy_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "proxy-exist",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaostoxi.proxy.probes",
    "func": "proxy_exist",
    "arguments": {
      "proxy_name": ""
    }
  }
}
```

```yaml
name: proxy-exist
provider:
  arguments:
    proxy_name: ''
  func: proxy_exist
  module: chaostoxi.proxy.probes
  type: python
type: probe

```



***

#### `reset`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.proxy.actions |
| **Name**              | reset |
| **Return**              | None |


Enable all proxies and remove all active toxics

**Signature:**

```python
('def reset(configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
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
    "module": "chaostoxi.proxy.actions",
    "func": "reset"
  }
}
```

```yaml
name: reset
provider:
  func: reset
  module: chaostoxi.proxy.actions
  type: python
type: action

```




### toxic



***

#### `create_bandwith_degradation_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_bandwith_degradation_toxic |
| **Return**              | mapping |


Limit the bandwith of a  downstream connection with a toxicity of 100%.

**Signature:**

```python
('def create_bandwith_degradation_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        rate: int,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **rate**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "create-bandwith-degradation-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_bandwith_degradation_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "rate": 0
    }
  }
}
```

```yaml
name: create-bandwith-degradation-toxic
provider:
  arguments:
    for_proxy: ''
    rate: 0
    toxic_name: ''
  func: create_bandwith_degradation_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_latency_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_latency_toxic |
| **Return**              | mapping |


Add a delay to all data going through the proxy using a downstream
with a toxicity of 100%.

**Signature:**

```python
('def create_latency_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        latency: int,\n        jitter: int = 0,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **latency**      | integer |  | Yes |
| **jitter**      | integer | 0 | No |




**Usage:**

```json
{
  "name": "create-latency-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_latency_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "latency": 0
    }
  }
}
```

```yaml
name: create-latency-toxic
provider:
  arguments:
    for_proxy: ''
    latency: 0
    toxic_name: ''
  func: create_latency_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_limiter_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_limiter_toxic |
| **Return**              | mapping |


Closes connections when transmitted data after the limit,
sets it up as a downstream, 100% toxicity.

**Signature:**

```python
('def create_limiter_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        bytes_limit: int,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **bytes_limit**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "create-limiter-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_limiter_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "bytes_limit": 0
    }
  }
}
```

```yaml
name: create-limiter-toxic
provider:
  arguments:
    bytes_limit: 0
    for_proxy: ''
    toxic_name: ''
  func: create_limiter_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_slicer_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_slicer_toxic |
| **Return**              | mapping |


Slices TCP data up into small bits, optionally adding a delay between
each sliced "packet" with a toxicity of 100%.

**Signature:**

```python
('def create_slicer_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        average_size: int,\n        size_variation: int,\n        delay: int,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **average_size**      | integer |  | Yes |
| **size_variation**      | integer |  | Yes |
| **delay**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "create-slicer-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_slicer_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "average_size": 0,
      "size_variation": 0,
      "delay": 0
    }
  }
}
```

```yaml
name: create-slicer-toxic
provider:
  arguments:
    average_size: 0
    delay: 0
    for_proxy: ''
    size_variation: 0
    toxic_name: ''
  func: create_slicer_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_slow_connection_close_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_slow_connection_close_toxic |
| **Return**              | mapping |


Limit the bandwith of a  downstream connection with a toxicity of 100%.

**Signature:**

```python
('def create_slow_connection_close_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        delay: int,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **delay**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "create-slow-connection-close-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_slow_connection_close_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "delay": 0
    }
  }
}
```

```yaml
name: create-slow-connection-close-toxic
provider:
  arguments:
    delay: 0
    for_proxy: ''
    toxic_name: ''
  func: create_slow_connection_close_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_timeout_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_timeout_toxic |
| **Return**              | mapping |


Generate as downstream delayed TCP close with a toxicity of 100%.

**Signature:**

```python
('def create_timeout_toxic(\n        for_proxy: str,\n        toxic_name: str,\n        timeout: int,\n        configuration: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **timeout**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "create-timeout-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_timeout_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "timeout": 0
    }
  }
}
```

```yaml
name: create-timeout-toxic
provider:
  arguments:
    for_proxy: ''
    timeout: 0
    toxic_name: ''
  func: create_timeout_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `create_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | create_toxic |
| **Return**              | boolean |


Allows you to create any of the supported types of toxics
with their attributes.

**Signature:**

```python
("def create_toxic(for_proxy: str,\n                 toxic_name: str,\n                 toxic_type: str,\n                 stream: str = 'downstream',\n                 toxicity: float = 1.0,\n                 attributes: Dict[str, Any] = None,\n                 configuration: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |
| **toxic_type**      | string |  | Yes |
| **stream**      | string | "downstream" | No |
| **toxicity**      | number | 1.0 | No |
| **attributes**      | mapping | null | No |




**Usage:**

```json
{
  "name": "create-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "create_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": "",
      "toxic_type": ""
    }
  }
}
```

```yaml
name: create-toxic
provider:
  arguments:
    for_proxy: ''
    toxic_name: ''
    toxic_type: ''
  func: create_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



***

#### `delete_toxic`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaostoxi.toxic.actions |
| **Name**              | delete_toxic |
| **Return**              | None |


Deletes the a given toxic.

**Signature:**

```python
('def delete_toxic(for_proxy: str,\n                 toxic_name: str,\n                 configuration: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **for_proxy**      | string |  | Yes |
| **toxic_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "delete-toxic",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaostoxi.toxic.actions",
    "func": "delete_toxic",
    "arguments": {
      "for_proxy": "",
      "toxic_name": ""
    }
  }
}
```

```yaml
name: delete-toxic
provider:
  arguments:
    for_proxy: ''
    toxic_name: ''
  func: delete_toxic
  module: chaostoxi.toxic.actions
  type: python
type: action

```



