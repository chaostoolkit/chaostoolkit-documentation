# Extension `chaosazure`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.7.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-azure |



[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-azure.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-azure)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-azure.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Microsoft Azure][azure] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[azure]: https://azure.microsoft.com/en-us/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```console
pip install -U chaostoolkit-azure
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
        "module": "chaosazure.vm.actions",
        "func": "stop_machines",
        "secrets": ["azure"],
        "arguments": {
            "parameters": {
                "TimeToRunInSeconds": 45
            }
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.



## Configuration

### Credentials
This extension uses the [Azure SDK][sdk] libraries under the hood. The Azure SDK library
expects that you have a tenant and client identifier, as well as a client secret and subscription, that allows you to 
authenticate with the Azure resource management API.

[creds]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-connect-to-secure-cluster
[requests]: http://docs.python-requests.org/en/master/
[sdk]: https://github.com/Azure/azure-sdk-for-python

There are two ways of doing this:

* you can either pass the name of the environment variables to the experiment definition as follows (recommended):

    ```json
    {
        "azure": {
            "client_id": {
                "type": "env",
                "key": "AZURE_CLIENT_ID"
            },
            "client_secret": {
                "type": "env",
                "key": "AZURE_CLIENT_SECRET"
            },
            "tenant_id": {
                "type": "env",
                "key": "AZURE_TENANT_ID"
            }
        }
    }
    ```
    
* or you inject the secrets explicitly to the experiment definition:

    ```json
    {
        "azure": {
            "client_id": "your-super-secret-client-id",
            "client_secret": "your-even-more-super-secret-client-secret",
            "tenant_id": "your-tenant-id"
        }
    }
    ```

    Also if you are not working with Public Global Azure, e.g. China Cloud
    You can feed the cloud environment name as well.
    Please refer to msrestazure.azure_cloud

    ```json
        {
            "azure": {
                "client_id": "xxxxxxx",
                "client_secret": "*******",
                "tenant_id": "@@@@@@@@@@@",
                "azure_cloud": "AZURE_CHINA_CLOUD"
            }
        }
    ```
    
    Additionally you need to provide the Azure subscription id.
    Either by reading from the environment variable named, for example,
    `SUBSCRIPTION_ID`:

    ```json
    {
        "configuration": {
            "azure_subscription_id": {
                "type": "env",
                "key": "SUBSCRIPTION_ID"
            }
        }
    }
    ```

    Or statically set into the configuration:

    ```json
    {
        "configuration": {
            "azure_subscription_id": "your-azure-subscription-id"
        }
    }
    ```

    An old, bu deprecated way of doing it was as follows, this still works
    but should not be favoured over the previous approaches as it's not the
    Chaos Toolkit way to pass structured configurations.

    ```json
    {
        "configuration": {
            "azure": {
                "subscription_id": "your-azure-subscription-id"
            }
        }
    }
    ```

### Putting it all together

Here is a full example:

```json
{
  "title": "...",
  "description": "...",
  "tags": [
    "azure",
    "kubernetes",
    "aks",
    "node"
  ],
  "configuration": {
    "azure": {
      "azure_subscription_id": {
        "type": "env",
        "key": "SUBSCRIPTION_ID"
      }
 }
  },
  "secrets": {
    "azure": {
      "client_id": "xxx",
      "client_secret": "xxx",
      "tenant_id": "xxx"
    }
  },
  "steady-state-hypothesis": {
    "title": "Services are all available and healthy",
    "probes": [
      {
        "type": "probe",
        "name": "consumer-service-must-still-respond",
        "tolerance": 200,
        "provider": {
          "type": "http",
          "url": "https://some-url/"
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "restart-node-at-random",
      "provider": {
        "type": "python",
        "module": "chaosazure.machine.actions",
        "func": "restart_machines",
        "secrets": [
          "azure"
        ],
        "config": [
          "azure"
        ]
      }
    }
  ],
  "rollbacks": [
    
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



### aks



***

#### `delete_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.aks.actions |
| **Name**              | delete_node |
| **Return**              | None |


Delete a node at random from a managed Azure Kubernetes Service.

**Be aware**: Deleting a node is an invasive action. You will not be able
to recover the node once you deleted it.

Parameters
----------
filter : str
    Filter the managed AKS. If the filter is omitted all AKS in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def delete_node(filter: str = None,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "delete-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.aks.actions",
    "func": "delete_node"
  }
}
```

```yaml
name: delete-node
provider:
  func: delete_node
  module: chaosazure.aks.actions
  type: python
type: action

```



***

#### `restart_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.aks.actions |
| **Name**              | restart_node |
| **Return**              | None |


Restart a node at random from a managed Azure Kubernetes Service.

Parameters
----------
filter : str
    Filter the managed AKS. If the filter is omitted all AKS in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def restart_node(filter: str = None,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "restart-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.aks.actions",
    "func": "restart_node"
  }
}
```

```yaml
name: restart-node
provider:
  func: restart_node
  module: chaosazure.aks.actions
  type: python
type: action

```



***

#### `stop_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.aks.actions |
| **Name**              | stop_node |
| **Return**              | None |


Stop a node at random from a managed Azure Kubernetes Service.

Parameters
----------
filter : str
    Filter the managed AKS. If the filter is omitted all AKS in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def stop_node(filter: str = None,\n              configuration: Dict[str, Dict[str, str]] = None,\n              secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "stop-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.aks.actions",
    "func": "stop_node"
  }
}
```

```yaml
name: stop-node
provider:
  func: stop_node
  module: chaosazure.aks.actions
  type: python
type: action

```




### machine



***

#### `burn_io`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | burn_io |
| **Return**              | None |


Increases the Disk I/O operations per second of the virtual machine.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.
duration : int, optional
    How long the burn lasts. Defaults to 60 seconds.
timeout : int
    Additional wait time (in seconds) for filling operation to be completed
    Getting and sending data from/to Azure may take some time so it's not
    recommended to set this value to less than 30s. Defaults to 60 seconds.


Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> burn_io("where resourceGroup=='rg'", configuration=c, secrets=s)
Increase the I/O operations per second of all machines from the group 'rg'

>>> burn_io("where resourceGroup=='rg' and name='name'",
                configuration=c, secrets=s)
Increase the I/O operations per second of the machine from the group 'rg'
having the name 'name'

>>> burn_io("where resourceGroup=='rg' | sample 2",
                configuration=c, secrets=s)
Increase the I/O operations per second of two machines at random from
the group 'rg'

**Signature:**

```python
('def burn_io(filter: str = None,\n            duration: int = 60,\n            timeout: int = 60,\n            configuration: Dict[str, Dict[str, str]] = None,\n            secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |
| **duration**      | integer | 60 | No |
| **timeout**      | integer | 60 | No |




**Usage:**

```json
{
  "name": "burn-io",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "burn_io"
  }
}
```

```yaml
name: burn-io
provider:
  func: burn_io
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `count_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosazure.machine.probes |
| **Name**              | count_machines |
| **Return**              | integer |


Return count of Azure virtual machines.

Parameters
----------
filter : str
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected for the probe.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def count_machines(filter: str = None,\n                   configuration: Dict[str, Dict[str, str]] = None,\n                   secrets: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "count-machines",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.probes",
    "func": "count_machines"
  }
}
```

```yaml
name: count-machines
provider:
  func: count_machines
  module: chaosazure.machine.probes
  type: python
type: probe

```



***

#### `delete_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | delete_machines |
| **Return**              | None |


Delete virtual machines at random.

**Be aware**: Deleting a machine is an invasive action. You will not be
able to recover the machine once you deleted it.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.

Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> delete_machines("where resourceGroup=='rg'", c, s)
Delete all machines from the group 'rg'

>>> delete_machines("where resourceGroup=='rg' and name='name'", c, s)
Delete the machine from the group 'rg' having the name 'name'

>>> delete_machines("where resourceGroup=='rg' | sample 2", c, s)
Delete two machines at random from the group 'rg'

**Signature:**

```python
('def delete_machines(filter: str = None,\n                    configuration: Dict[str, Dict[str, str]] = None,\n                    secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "delete-machines",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "delete_machines"
  }
}
```

```yaml
name: delete-machines
provider:
  func: delete_machines
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `describe_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosazure.machine.probes |
| **Name**              | describe_machines |
| **Return**              | None |


Describe Azure virtual machines.

Parameters
----------
filter : str
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected for the probe.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def describe_machines(filter: str = None,\n                      configuration: Dict[str, Dict[str, str]] = None,\n                      secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "describe-machines",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.probes",
    "func": "describe_machines"
  }
}
```

```yaml
name: describe-machines
provider:
  func: describe_machines
  module: chaosazure.machine.probes
  type: python
type: probe

```



***

#### `fill_disk`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | fill_disk |
| **Return**              | None |


Fill the disk with random data.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.
duration : int, optional
    Lifetime of the file created. Defaults to 120 seconds.
timeout : int
    Additional wait time (in seconds)
    for filling operation to be completed.
    Getting and sending data from/to Azure may take some time so it's not
    recommended to set this value to less than 30s. Defaults to 60 seconds.
size : int
    Size of the file created on the disk. Defaults to 1GB.


Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> fill_disk("where resourceGroup=='rg'", configuration=c, secrets=s)
Fill all machines from the group 'rg'

>>> fill_disk("where resourceGroup=='rg' and name='name'",
                configuration=c, secrets=s)
Fill the machine from the group 'rg' having the name 'name'

>>> fill_disk("where resourceGroup=='rg' | sample 2",
                configuration=c, secrets=s)
Fill two machines at random from the group 'rg'

**Signature:**

```python
('def fill_disk(filter: str = None,\n              duration: int = 120,\n              timeout: int = 60,\n              size: int = 1000,\n              configuration: Dict[str, Dict[str, str]] = None,\n              secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |
| **duration**      | integer | 120 | No |
| **timeout**      | integer | 60 | No |
| **size**      | integer | 1000 | No |




**Usage:**

```json
{
  "name": "fill-disk",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "fill_disk"
  }
}
```

```yaml
name: fill-disk
provider:
  func: fill_disk
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `network_latency`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | network_latency |
| **Return**              | None |


Increases the response time of the virtual machine.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.
duration : int, optional
    How long the latency lasts. Defaults to 60 seconds.
timeout : int
    Additional wait time (in seconds) for filling operation to be completed
    Getting and sending data from/to Azure may take some time so it's not
    recommended to set this value to less than 30s. Defaults to 60 seconds.
delay : int
    Added delay in ms. Defaults to 200.
jitter : int
    Variance of the delay in ms. Defaults to 50.


Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> network_latency("where resourceGroup=='rg'", configuration=c,
                secrets=s)
Increase the latency of all machines from the group 'rg'

>>> network_latency("where resourceGroup=='rg' and name='name'",
                configuration=c, secrets=s)
Increase the latecy of the machine from the group 'rg' having the name
'name'

>>> network_latency("where resourceGroup=='rg' | sample 2",
                configuration=c, secrets=s)
Increase the latency of two machines at random from the group 'rg'

**Signature:**

```python
('def network_latency(filter: str = None,\n                    duration: int = 60,\n                    delay: int = 200,\n                    jitter: int = 50,\n                    timeout: int = 60,\n                    configuration: Dict[str, Dict[str, str]] = None,\n                    secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |
| **duration**      | integer | 60 | No |
| **delay**      | integer | 200 | No |
| **jitter**      | integer | 50 | No |
| **timeout**      | integer | 60 | No |




**Usage:**

```json
{
  "name": "network-latency",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "network_latency"
  }
}
```

```yaml
name: network-latency
provider:
  func: network_latency
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `restart_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | restart_machines |
| **Return**              | None |


Restart virtual machines at random.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.

Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> restart_machines("where resourceGroup=='rg'", c, s)
Restart all machines from the group 'rg'

>>> restart_machines("where resourceGroup=='rg' and name='name'", c, s)
Restart the machine from the group 'rg' having the name 'name'

>>> restart_machines("where resourceGroup=='rg' | sample 2", c, s)
Restart two machines at random from the group 'rg'

**Signature:**

```python
('def restart_machines(filter: str = None,\n                     configuration: Dict[str, Dict[str, str]] = None,\n                     secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "restart-machines",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "restart_machines"
  }
}
```

```yaml
name: restart-machines
provider:
  func: restart_machines
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `start_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | start_machines |
| **Return**              | None |


Start virtual machines at random. Thought as a rollback action.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.

Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> start_machines("where resourceGroup=='rg'", c, s)
Start all stopped machines from the group 'rg'

>>> start_machines("where resourceGroup=='rg' and name='name'", c, s)
Start the stopped machine from the group 'rg' having the name 'name'

>>> start_machines("where resourceGroup=='rg' | sample 2", c, s)
Start two stopped machines at random from the group 'rg'

**Signature:**

```python
('def start_machines(filter: str = None,\n                   configuration: Dict[str, Dict[str, str]] = None,\n                   secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "start-machines",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "start_machines"
  }
}
```

```yaml
name: start-machines
provider:
  func: start_machines
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `stop_machines`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | stop_machines |
| **Return**              | None |


Stop virtual machines at random.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.

Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> stop_machines("where resourceGroup=='rg'", c, s)
Stop all machines from the group 'rg'

>>> stop_machines("where resourceGroup=='mygroup' and name='myname'", c, s)
Stop the machine from the group 'mygroup' having the name 'myname'

>>> stop_machines("where resourceGroup=='mygroup' | sample 2", c, s)
Stop two machines at random from the group 'mygroup'

**Signature:**

```python
('def stop_machines(filter: str = None,\n                  configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "stop-machines",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "stop_machines"
  }
}
```

```yaml
name: stop-machines
provider:
  func: stop_machines
  module: chaosazure.machine.actions
  type: python
type: action

```



***

#### `stress_cpu`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.machine.actions |
| **Name**              | stress_cpu |
| **Return**              | None |


Stress CPU up to 100% at random machines.

Parameters
----------
filter : str, optional
    Filter the virtual machines. If the filter is omitted all machines in
    the subscription will be selected as potential chaos candidates.
duration : int, optional
    Duration of the stress test (in seconds) that generates high CPU usage.
    Defaults to 120 seconds.
timeout : int
    Additional wait time (in seconds) for stress operation to be completed.
    Getting and sending data from/to Azure may take some time so it's not
    recommended to set this value to less than 30s. Defaults to 60 seconds.

Examples
--------
Some calling examples. Deep dive into the filter syntax:
https://docs.microsoft.com/en-us/azure/kusto/query/

>>> stress_cpu("where resourceGroup=='rg'", configuration=c, secrets=s)
Stress all machines from the group 'rg'

>>> stress_cpu("where resourceGroup=='rg' and name='name'",
                configuration=c, secrets=s)
Stress the machine from the group 'rg' having the name 'name'

>>> stress_cpu("where resourceGroup=='rg' | sample 2",
                configuration=c, secrets=s)
Stress two machines at random from the group 'rg'

**Signature:**

```python
('def stress_cpu(filter: str = None,\n               duration: int = 120,\n               timeout: int = 60,\n               configuration: Dict[str, Dict[str, str]] = None,\n               secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |
| **duration**      | integer | 120 | No |
| **timeout**      | integer | 60 | No |




**Usage:**

```json
{
  "name": "stress-cpu",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.machine.actions",
    "func": "stress_cpu"
  }
}
```

```yaml
name: stress-cpu
provider:
  func: stress_cpu
  module: chaosazure.machine.actions
  type: python
type: action

```




### vmss



***

#### `deallocate_vmss`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.vmss.actions |
| **Name**              | deallocate_vmss |
| **Return**              | None |


Deallocate a virtual machine scale set instance at random.
 Parameters
----------
filter : str
    Filter the virtual machine scale set. If the filter is omitted all
    virtual machine scale sets in the subscription will be selected as
    potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def deallocate_vmss(filter: str = None,\n                    configuration: Dict[str, Dict[str, str]] = None,\n                    secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "deallocate-vmss",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.vmss.actions",
    "func": "deallocate_vmss"
  }
}
```

```yaml
name: deallocate-vmss
provider:
  func: deallocate_vmss
  module: chaosazure.vmss.actions
  type: python
type: action

```



***

#### `delete_vmss`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.vmss.actions |
| **Name**              | delete_vmss |
| **Return**              | None |


Delete a virtual machine scale set instance at random.

**Be aware**: Deleting a VMSS instance is an invasive action. You will not
be able to recover the VMSS instance once you deleted it.

 Parameters
----------
filter : str
    Filter the virtual machine scale set. If the filter is omitted all
    virtual machine scale sets in the subscription will be selected as
    potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def delete_vmss(filter: str = None,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "delete-vmss",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.vmss.actions",
    "func": "delete_vmss"
  }
}
```

```yaml
name: delete-vmss
provider:
  func: delete_vmss
  module: chaosazure.vmss.actions
  type: python
type: action

```



***

#### `restart_vmss`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.vmss.actions |
| **Name**              | restart_vmss |
| **Return**              | None |


Restart a virtual machine scale set instance at random.
 Parameters
----------
filter : str
    Filter the virtual machine scale set. If the filter is omitted all
    virtual machine scale sets in the subscription will be selected as
    potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def restart_vmss(filter: str = None,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "restart-vmss",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.vmss.actions",
    "func": "restart_vmss"
  }
}
```

```yaml
name: restart-vmss
provider:
  func: restart_vmss
  module: chaosazure.vmss.actions
  type: python
type: action

```



***

#### `stop_vmss`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.vmss.actions |
| **Name**              | stop_vmss |
| **Return**              | None |


Stop a virtual machine scale set instance at random.
 Parameters
----------
filter : str
    Filter the virtual machine scale set. If the filter is omitted all
    virtual machine scale sets in the subscription will be selected as
    potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'
instance_criteria :  Iterable[Mapping[str, any]]
    Allows specification of criteria for selection of a given virtual
    machine scale set instance. If the instance_criteria is omitted,
    an instance will be chosen at random. All of the criteria within each
    item of the Iterable must match, i.e. AND logic is applied.
    The first item with all matching criterion will be used to select the
    instance.
    Criteria example:
    [
     {"name": "myVMSSInstance1"},
     {
      "name": "myVMSSInstance2",
      "instanceId": "2"
     }
     {"instanceId": "3"},
    ]
    If the instances include two items. One with name = myVMSSInstance4
    and instanceId = 2. The other with name = myVMSSInstance2 and
    instanceId = 3. The criteria {"instanceId": "3"} will be the first
    match since both the name and the instanceId did not match on the
    first criteria.

**Signature:**

```python

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |
| **instance_criteria**      | object | null | No |




**Usage:**

```json
{
  "name": "stop-vmss",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.vmss.actions",
    "func": "stop_vmss"
  }
}
```

```yaml
name: stop-vmss
provider:
  func: stop_vmss
  module: chaosazure.vmss.actions
  type: python
type: action

```




### webapp



***

#### `delete_webapp`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.webapp.actions |
| **Name**              | delete_webapp |
| **Return**              | None |


Delete a web app at random.

***Be aware**: Deleting a web app is an invasive action. You will not be
able to recover the web app once you deleted it.

Parameters
----------
filter : str
    Filter the web apps. If the filter is omitted all web apps in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def delete_webapp(filter: str = None,\n                  configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "delete-webapp",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.webapp.actions",
    "func": "delete_webapp"
  }
}
```

```yaml
name: delete-webapp
provider:
  func: delete_webapp
  module: chaosazure.webapp.actions
  type: python
type: action

```



***

#### `restart_webapp`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.webapp.actions |
| **Name**              | restart_webapp |
| **Return**              | None |


Restart a web app at random.

Parameters
----------
filter : str
    Filter the web apps. If the filter is omitted all web apps in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def restart_webapp(filter: str = None,\n                   configuration: Dict[str, Dict[str, str]] = None,\n                   secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "restart-webapp",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.webapp.actions",
    "func": "restart_webapp"
  }
}
```

```yaml
name: restart-webapp
provider:
  func: restart_webapp
  module: chaosazure.webapp.actions
  type: python
type: action

```



***

#### `start_webapp`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.webapp.actions |
| **Name**              | start_webapp |
| **Return**              | None |


Start a web app at random.

Parameters
----------
filter : str
    Filter the web apps. If the filter is omitted all web apps in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def start_webapp(filter: str = None,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "start-webapp",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.webapp.actions",
    "func": "start_webapp"
  }
}
```

```yaml
name: start-webapp
provider:
  func: start_webapp
  module: chaosazure.webapp.actions
  type: python
type: action

```



***

#### `stop_webapp`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.webapp.actions |
| **Name**              | stop_webapp |
| **Return**              | None |


Stop a web app at random.

Parameters
----------
filter : str
    Filter the web apps. If the filter is omitted all web apps in
    the subscription will be selected as potential chaos candidates.
    Filtering example:
    'where resourceGroup=="myresourcegroup" and name="myresourcename"'

**Signature:**

```python
('def stop_webapp(filter: str = None,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filter**      | string | null | No |




**Usage:**

```json
{
  "name": "stop-webapp",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosazure.webapp.actions",
    "func": "stop_webapp"
  }
}
```

```yaml
name: stop-webapp
provider:
  func: stop_webapp
  module: chaosazure.webapp.actions
  type: python
type: action

```



