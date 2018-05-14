# Extension `chaosprometheus`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.3.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-prometheus |


[![Build Status](https://travis-ci.org/chaostoolkit/chaostoolkit-prometheus.svg?branch=master)](https://travis-ci.org/chaostoolkit/chaostoolkit-prometheus)

[Prometheus][prometheus] support for the [Chaos Toolkit][chaostoolkit].

[prometheus]: https://prometheus.io/
[chaostoolkit]: http://chaostoolkit.org/

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-prometheus
```

## Usage

To use this package, you must create have access to a Prometheus instance via
HTTP and be allowed to connect to it.

This package only exports probes to query for some aspects of your system as
monitored by Prometheus.

Here is an example of querying Prometheus at a given moment

```json
{
    "type": "probe",
    "name": "fetch-cpu-just-2mn-ago",
    "provider": {
        "type": "python",
        "module": "chaosprometheus.probes",
        "func": "query",
        "arguments": {
            "query": "process_cpu_seconds_total{job='websvc'}",
            "when": "2 minutes ago"
        }
    }
}
```

You can also ask for an interval as follows:

```json
{
    "type": "probe",
    "name": "fetch-cpu-over-interval",
    "provider": {
        "type": "python",
        "module": "chaosprometheus.probes",
        "func": "query_interval",
        "arguments": {
            "query": "process_cpu_seconds_total{job='websvc'}",
            "start": "2 minutes ago",
            "end": "now",
            "step": 5
        }
    }
}
```

In both cases, the probe returns the [JSON payload as-is][api] from Prometheus
or raises an exception when an error is met.

[api]: https://prometheus.io/docs/querying/api/

The result is not further process and should be found in the generated report
of the experiment run.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/


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


