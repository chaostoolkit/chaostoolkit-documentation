# Extension `chaosprometheus`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.3.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-prometheus |

N/A

## Exported Activities



### probes



***

#### `query`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosprometheus.probes |
| **Name**              | query |
| **Return**              | mapping |


Run an instant query against a Prometheus server and returns its result
as-is.

**Signature:**

```python
def query(query: str,
          when: str = None,
          timeout: float = None,
          configuration: Dict[str, Dict[str, str]] = None,
          secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **query**      | string |  | Yes |
| **when**      | string | null | No |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "query",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosprometheus.probes",
    "func": "query",
    "arguments": {
      "query": ""
    }
  }
}
```

```yaml
name: query
provider:
  arguments:
    query: ''
  func: query
  module: chaosprometheus.probes
  type: python
type: probe

```



***

#### `query_interval`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosprometheus.probes |
| **Name**              | query_interval |
| **Return**              | mapping |


Run a range query against a Prometheus server and returns its result as-is.

The `start` and `end` arguments can be a RFC 3339 date or expressed more
colloquially such as `"5 minutes ago"`.

**Signature:**

```python
def query_interval(
        query: str,
        start: str,
        end: str,
        step: int = 1,
        timeout: float = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **query**      | string |  | Yes |
| **start**      | string |  | Yes |
| **end**      | string |  | Yes |
| **step**      | integer | 1 | No |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "query-interval",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosprometheus.probes",
    "func": "query_interval",
    "arguments": {
      "query": "",
      "start": "",
      "end": ""
    }
  }
}
```

```yaml
name: query-interval
provider:
  arguments:
    end: ''
    query: ''
    start: ''
  func: query_interval
  module: chaosprometheus.probes
  type: python
type: probe

```


