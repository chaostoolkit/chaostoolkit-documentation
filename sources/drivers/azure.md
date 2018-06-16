# Extension `chaosazure`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.3 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-azure |

N/A

## Exported Activities



### fabric



***

#### `chaos_report`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosazure.fabric.probes |
| **Name**              | chaos_report |
| **Return**              | mapping |


Get Chaos report using following the Service Fabric API:

https://docs.microsoft.com/en-us/rest/api/servicefabric/sfclient-v60-model-chaosparameters

Please see the :func:`chaosazure.fabric.auth` help for more information
on authenticating with the service.

**Signature:**

```python
def chaos_report(timeout: int = 60,
                 start_time_utc: str = None,
                 end_time_utc: str = None,
                 configuration: Dict[str, Dict[str, str]] = None,
                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

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
    "module": "chaosazure.fabric.probes",
    "func": "chaos_report"
  }
}
```

```yaml
name: chaos-report
provider:
  func: chaos_report
  module: chaosazure.fabric.probes
  type: python
type: probe

```



***

#### `start_chaos`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.fabric.actions |
| **Name**              | start_chaos |
| **Return**              | mapping |


Start Chaos in your cluster using the given `parameters`. This is a mapping
of keys as declared in the Service Fabric API:

https://docs.microsoft.com/en-us/rest/api/servicefabric/sfclient-v60-model-chaosparameters

Please see the :func:`chaosazure.fabric.auth` help for more information
on authenticating with the service.

**Signature:**

```python
def start_chaos(parameters: Dict[str, Any],
                timeout: int = 60,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

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
    "module": "chaosazure.fabric.actions",
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
  module: chaosazure.fabric.actions
  type: python
type: action

```



***

#### `stop_chaos`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosazure.fabric.actions |
| **Name**              | stop_chaos |
| **Return**              | mapping |


Stop Chaos in your cluster.

Please see the :func:`chaosazure.fabric.auth` help for more information
on authenticating with the service.

**Signature:**

```python
def stop_chaos(timeout: int = 60,
               configuration: Dict[str, Dict[str, str]] = None,
               secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

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
    "module": "chaosazure.fabric.actions",
    "func": "stop_chaos"
  }
}
```

```yaml
name: stop-chaos
provider:
  func: stop_chaos
  module: chaosazure.fabric.actions
  type: python
type: action

```


