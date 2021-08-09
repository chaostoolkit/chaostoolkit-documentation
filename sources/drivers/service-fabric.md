# Extension `chaosservicefabric`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-service-fabric |



[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-service-fabric.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Microsoft Service Fabric][servicefabric] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[servicefabric]: https://azure.microsoft.com/en-us/services/service-fabric/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```console
pip install -U chaostoolkit-service-fabric
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "start-service-factory-chaos",
    "provider": {
        "type": "python",
        "module": "chaosservicefabric.factory.actions",
        "func": "start_chaos",
        "secrets": ["azure"],
        "arguments": {
            "parameters": {
                "TimeToRunInSeconds": 45
            }
        }
    }
},
{
    "type": "action",
    "name": "stop-service-factory-chaos",
    "provider": {
        "type": "python",
        "module": "chaosservicefabric.factory.actions",
        "func": "stop_chaos",
        "secrets": ["azure"]
    }
}
```

That's it!

Please explore the code to see existing probes and actions.



## Configuration

### Credentials

This extension uses the [requests][] library under the hood. The requests library
expects that you have a PFX certificate, converted as to the PEM format, that allows you to 
authenticate with the [Service Factory][sf] endpoint.

[sf]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-controlled-chaos
[creds]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-connect-to-secure-cluster
[requests]: http://docs.python-requests.org/en/master/
[sdk]: https://github.com/Azure/azure-sdk-for-python

Generally speaking, there are two ways of doing this:

* you have [created][creds] a configuration file where you will run the
  experiment from (so with a `~/.sfctl/config` file)
* you explicitly pass the correct environment variables to the experiment
  definition as follows:

    Configuration section:

    ```json
    {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify_tls": false,
        "use_ca": false
    }
    ```

    Secrets section:

    ```json
    {
        "azure": {
            "security": "pem",
            "pem_path": "./cluster-client-cert.pem"
        }
    }
    ```

    The PEM can also be passed as an environment variable:

    ```json
    {
        "azure": {
            "security": "pem",
            "pem_content": {
                "type": "env",
                "key": "AZURE_PEM"
            }
        }
    }
    ```

    The environment variable name can be anything.

### Putting it all together

Here is a full example:

```json
{
    "title": "...",
    "description": "...",
    "configuration": {
        "endpoint": "https://XYZ.westus.cloudapp.azure.com:19080",
        "verify_tls": false,
        "use_ca": false
    },
    "secrets": {
        "azure": {
            "security": "pem",
            "pem_path": "./cluster-client-cert.pem"
        }
    },
    "steady-state-hypothesis": {
        "title": "Services is healthy",
        "probes": [
            {
                "type": "probe",
                "name": "application-must-respond",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "verify_tls": false,
                    "url": "https://some-url-in-cluster/"
                }
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "start-service-factory-chaos",
            "provider": {
                "type": "python",
                "module": "chaosservicefabric.factory.actions",
                "func": "start_chaos",
                "secrets": ["azure"],
                "arguments": {
                    "parameters": {
                        "TimeToRunInSeconds": 45
                    }
                }
            },
            "pauses": {
                "after": 30
            }
        },
        {
            "type": "probe",
            "ref": "application-must-respond"
        },
        {
            "type": "action",
            "name": "stop-service-factory-chaos",
            "provider": {
                "type": "python",
                "module": "chaosservicefabric.factory.actions",
                "func": "stop_chaos",
                "secrets": ["azure"]
            },
            "pauses": {
                "after": 5
            }
        },
        {
            "type": "probe",
            "name": "get-service-factory-chaos-report",
            "provider": {
                "type": "python",
                "module": "chaosservicefabric.factory.probes",
                "func": "chaos_report",
                "secrets": ["azure"],
                "arguments": {
                    "start_time_utc": "1 minute ago",
                    "end_time_utc": "now"
                }
            }
        }
    ]
}
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

To run the tests for the project execute the following:

```console
pytest
```





## Exported Activities



### cluster



***

#### `chaos_report`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosservicefabric.cluster.probes |
| **Name**              | chaos_report |
| **Return**              | mapping |


Get Chaos report using following the Service Fabric API:

https://docs.microsoft.com/en-us/rest/api/servicefabric/sfclient-v60-model-chaosparameters

Please see the :func:`chaosazure.fabric.auth` help for more information
on authenticating with the service.

**Signature:**

```python
('def chaos_report(timeout: int = 60,\n                 start_time_utc: str = None,\n                 end_time_utc: str = None,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **timeout**      | integer | 60 | No |
| **start_time_utc**      | string | null | No |
| **end_time_utc**      | string | null | No |




**Usage:**

```json
{
  "name": "chaos-report",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosservicefabric.cluster.probes",
    "func": "chaos_report"
  }
}
```

```yaml
name: chaos-report
provider:
  func: chaos_report
  module: chaosservicefabric.cluster.probes
  type: python
type: probe

```



***

#### `start_chaos`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosservicefabric.cluster.actions |
| **Name**              | start_chaos |
| **Return**              | mapping |


Start Chaos in your cluster using the given `parameters`. This is a mapping
of keys as declared in the Service Fabric API:

https://docs.microsoft.com/en-us/rest/api/servicefabric/sfclient-v60-model-chaosparameters

Please see the :func:`chaosservicefabric.fabric.auth` help for more
information on authenticating with the service.

**Signature:**

```python
('def start_chaos(parameters: Dict[str, Any],\n                timeout: int = 60,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parameters**      | mapping |  | Yes |
| **timeout**      | integer | 60 | No |




**Usage:**

```json
{
  "name": "start-chaos",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosservicefabric.cluster.actions",
    "func": "start_chaos",
    "arguments": {
      "parameters": {}
    }
  }
}
```

```yaml
name: start-chaos
provider:
  arguments:
    parameters: {}
  func: start_chaos
  module: chaosservicefabric.cluster.actions
  type: python
type: action

```



***

#### `stop_chaos`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosservicefabric.cluster.actions |
| **Name**              | stop_chaos |
| **Return**              | mapping |


Stop Chaos in your cluster.

Please see the :func:`chaosservicefabric.fabric.auth` help for more
information on authenticating with the service.

**Signature:**

```python
('def stop_chaos(timeout: int = 60,\n               configuration: Dict[str, Dict[str, str]] = None,\n               secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **timeout**      | integer | 60 | No |




**Usage:**

```json
{
  "name": "stop-chaos",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosservicefabric.cluster.actions",
    "func": "stop_chaos"
  }
}
```

```yaml
name: stop-chaos
provider:
  func: stop_chaos
  module: chaosservicefabric.cluster.actions
  type: python
type: action

```



