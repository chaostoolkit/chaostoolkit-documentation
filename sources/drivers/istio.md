# Extension `chaosistio`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.4 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-istio |



[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-istio.svg)](https://www.python.org/)


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
$ pip install -U chaostoolkit-istio
```

## Usage

Below is an example of using this extension to inject a delay of 5 seconds to
a specific user.

Note this example can be applied against the
[bookinfo Istio sample application](https://istio.io/docs/examples/bookinfo/).

To run it, simple set the `KUBERNETES_CONTEXT` environment variable to the
target cluster and ensure your local kubeconfig is properly populated for that
context. Set also the `PRODUCT_PAGE_SERVICE_BASE_URL` to the address of the
Istio gateway.

For instance:

```
$ export PRODUCT_PAGE_SERVICE_BASE_URL=$(kubectl get po -l istio=ingressgateway -n istio-system -o 'jsonpath={.items[0].status.hostIP}'):$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
```

```json
{
    "title": "Network latency does not impact our users",
    "description": "Using Istio fault injection capability, let's explore how latency impacts a single user",
    "configuration": {
        "product_page_url": {
            "type": "env",
            "key": "PRODUCT_PAGE_SERVICE_BASE_URL"
        }
    },
    "secrets": {
        "istio": {
            "KUBERNETES_CONTEXT": {
                "type": "env",
                "key": "KUBERNETES_CONTEXT"
            }
        }
    },
    "steady-state-hypothesis": {
        "title": "Our service should respond under 1 second",
        "probes": [
            {
                "type": "probe",
                "name": "sign-in-as-jason",
                "tolerance": 0,
                "provider": {
                    "type": "process",
                    "path": "curl",
                    "arguments": "-v -X POST -d 'username=jason&passwd=' -c /tmp/cookie.txt --silent ${product_page_url}/login"
                }
            },
            {
                "type": "probe",
                "name": "fetch-productpage-for-jason-in-due-time",
                "tolerance": 0,
                "provider": {
                    "type": "process",
                    "path": "curl",
                    "arguments": "-v --connect-timeout 1 --max-time 1 -b /tmp/cookie.txt --silent ${product_page_url}/productpage"
                }
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "inject-fault-for-jason-only",
            "provider": {
                "type": "python",
                "module": "chaosistio.fault.actions",
                "func": "add_delay_fault",
                "secrets": ["istio"],
                "arguments": {
                    "virtual_service_name": "reviews",
                    "fixed_delay": "5s",
                    "percentage": {
                        "value":  100.0
                    },
                    "routes": [
                        {
                            "destination": {
                                "host": "reviews",
                                "subset": "v2"
                            }
                        }
                    ]
                }
            },
            "pauses": {
                "after": 2
            }
        }
    ],
    "rollbacks": [
        {
            "type": "action",
            "name": "remove-fault-for-jason-only",
            "provider": {
                "type": "python",
                "module": "chaosistio.fault.actions",
                "func": "remove_delay_fault",
                "secrets": ["istio"],
                "arguments": {
                    "virtual_service_name": "reviews",
                    "routes": [
                        {
                            "destination": {
                                "host": "reviews",
                                "subset": "v2"
                            }
                        }
                    ]
                }
            }
        }
    ]
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

This extension needs you specify how to connect to the Kubernetes cluster. This
can be done by setting the `KUBERNETES_CONTEXT` in the `secrets` payload.


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
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```





## Exported Activities



### fault



***

#### `add_abort_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | add_abort_fault |
| **Return**              | mapping |


Abort requests early by the virtual service identified by `name`

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection-Abort

**Signature:**

```python
("def add_abort_fault(\n        virtual_service_name: str,\n        http_status: int,\n        routes: List[Dict[str, str]],\n        percentage: float = None,\n        ns: str = 'default',\n        version: str = 'networking.istio.io/v1alpha3',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **http_status**      | integer |  | Yes |
| **routes**      | list |  | Yes |
| **percentage**      | number | null | No |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "add-abort-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "add_abort_fault",
    "arguments": {
      "virtual_service_name": "",
      "http_status": 0,
      "routes": []
    }
  }
}
```

```yaml
name: add-abort-fault
provider:
  arguments:
    http_status: 0
    routes: []
    virtual_service_name: ''
  func: add_abort_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



***

#### `add_delay_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | add_delay_fault |
| **Return**              | mapping |


Add delay to the virtual service identified by `name`

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection-Delay

**Signature:**

```python
("def add_delay_fault(\n        virtual_service_name: str,\n        fixed_delay: str,\n        routes: List[Dict[str, str]],\n        percentage: float = None,\n        ns: str = 'default',\n        version: str = 'networking.istio.io/v1alpha3',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **fixed_delay**      | string |  | Yes |
| **routes**      | list |  | Yes |
| **percentage**      | number | null | No |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "add-delay-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "add_delay_fault",
    "arguments": {
      "virtual_service_name": "",
      "fixed_delay": "",
      "routes": []
    }
  }
}
```

```yaml
name: add-delay-fault
provider:
  arguments:
    fixed_delay: ''
    routes: []
    virtual_service_name: ''
  func: add_delay_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



***

#### `get_virtual_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosistio.fault.probes |
| **Name**              | get_virtual_service |
| **Return**              | mapping |


Get a virtual service identified by `name`

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#VirtualService

**Signature:**

```python
("def get_virtual_service(\n        virtual_service_name: str,\n        ns: str = 'default',\n        version: str = 'networking.istio.io/v1alpha3',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "get-virtual-service",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.probes",
    "func": "get_virtual_service",
    "arguments": {
      "virtual_service_name": ""
    }
  }
}
```

```yaml
name: get-virtual-service
provider:
  arguments:
    virtual_service_name: ''
  func: get_virtual_service
  module: chaosistio.fault.probes
  type: python
type: probe

```



***

#### `remove_abort_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | remove_abort_fault |
| **Return**              | mapping |


Remove abort request faults from the virtual service identified by `name`

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection-Abort

**Signature:**

```python
("def remove_abort_fault(\n        virtual_service_name: str,\n        routes: List[Dict[str, str]],\n        ns: str = 'default',\n        version: str = 'networking.istio.io/v1alpha3',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **routes**      | list |  | Yes |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "remove-abort-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "remove_abort_fault",
    "arguments": {
      "virtual_service_name": "",
      "routes": []
    }
  }
}
```

```yaml
name: remove-abort-fault
provider:
  arguments:
    routes: []
    virtual_service_name: ''
  func: remove_abort_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



***

#### `remove_delay_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | remove_delay_fault |
| **Return**              | mapping |


Remove delay from the virtual service identified by `name`

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection-Delay

**Signature:**

```python
("def remove_delay_fault(\n        virtual_service_name: str,\n        routes: List[Dict[str, str]],\n        ns: str = 'default',\n        version: str = 'networking.istio.io/v1alpha3',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **routes**      | list |  | Yes |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "remove-delay-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "remove_delay_fault",
    "arguments": {
      "virtual_service_name": "",
      "routes": []
    }
  }
}
```

```yaml
name: remove-delay-fault
provider:
  arguments:
    routes: []
    virtual_service_name: ''
  func: remove_delay_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



***

#### `set_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | set_fault |
| **Return**              | mapping |


Setfault injection on the virtual service identified by `name`

The `fault` argument must be the object passed as the `spec` property
of a virtual service resource.

If a fault already exists, it is updated with the new specification.

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection

**Signature:**

```python
("def set_fault(virtual_service_name: str,\n              routes: List[Dict[str, str]],\n              fault: Dict[str, Any],\n              ns: str = 'default',\n              version: str = 'networking.istio.io/v1alpha3',\n              configuration: Dict[str, Dict[str, str]] = None,\n              secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **routes**      | list |  | Yes |
| **fault**      | mapping |  | Yes |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "set-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "set_fault",
    "arguments": {
      "virtual_service_name": "",
      "routes": [],
      "fault": {}
    }
  }
}
```

```yaml
name: set-fault
provider:
  arguments:
    fault: {}
    routes: []
    virtual_service_name: ''
  func: set_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



***

#### `unset_fault`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosistio.fault.actions |
| **Name**              | unset_fault |
| **Return**              | mapping |


Unset fault injection from the virtual service identified by `name`

The `fault` argument must be the object passed as the `spec` property
of a virtual service resource.

See https://istio.io/docs/reference/config/istio.networking.v1alpha3/#HTTPFaultInjection

**Signature:**

```python
("def unset_fault(virtual_service_name: str,\n                routes: List[Dict[str, str]],\n                ns: str = 'default',\n                version: str = 'networking.istio.io/v1alpha3',\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **virtual_service_name**      | string |  | Yes |
| **routes**      | list |  | Yes |
| **ns**      | string | "default" | No |
| **version**      | string | "networking.istio.io/v1alpha3" | No |




**Usage:**

```json
{
  "name": "unset-fault",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosistio.fault.actions",
    "func": "unset_fault",
    "arguments": {
      "virtual_service_name": "",
      "routes": []
    }
  }
}
```

```yaml
name: unset-fault
provider:
  arguments:
    routes: []
    virtual_service_name: ''
  func: unset_fault
  module: chaosistio.fault.actions
  type: python
type: action

```



