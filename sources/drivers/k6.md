# Extension `chaosk6`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.2.0 |
| **Repository**        | https://github.com/k6io/chaostoolkit-k6 |


N/A




## Exported Activities



### actions



***

#### `run_script`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk6.actions |
| **Name**              | run_script |
| **Return**              | None |


Run an arbitrary k6 script with a configurable amount of VUs and duration.
Depending on the specs of the attacking machine, possible VU amount may
vary.
For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.


--
scriptPath : str
  Full path to the k6 test script
vus : int
  Amount of virtual users to run the test with
duration : str
  Duration, written as a string, ie: `1h2m3s` etc

**Signature:**

```python
def run_script(scriptPath: str = None, vus: int = 1, duration: str = '1s'):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **scriptPath**      | string | null | No |
| **vus**      | integer | 1 | No |
| **duration**      | string | "1s" | No |




**Usage:**

```json
{
  "name": "run-script",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk6.actions",
    "func": "run_script"
  }
}
```

```yaml
name: run-script
provider:
  func: run_script
  module: chaosk6.actions
  type: python
type: action

```



***

#### `stress_endpoint`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk6.actions |
| **Name**              | stress_endpoint |
| **Return**              | None |


Stress a single endpoint with a configurable amount of VUs and duration.
Depending on the specs of the attacking machine, possible VU amount may
vary.
For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.


--
endpoint : str
  The URL to the endpoint you want to stress, including the scheme prefix.
vus : int
  Amount of virtual users to run the test with
duration : str
  Duration, written as a string, ie: `1h2m3s` etc

**Signature:**

```python
def stress_endpoint(endpoint: str = None, vus: int = 1, duration: str = '1s'):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **endpoint**      | string | null | No |
| **vus**      | integer | 1 | No |
| **duration**      | string | "1s" | No |




**Usage:**

```json
{
  "name": "stress-endpoint",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk6.actions",
    "func": "stress_endpoint"
  }
}
```

```yaml
name: stress-endpoint
provider:
  func: stress_endpoint
  module: chaosk6.actions
  type: python
type: action

```




### probes



***

#### `http`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk6.probes |
| **Name**              | http |
| **Return**              | boolean |


Probe an endpoint to make sure it responds to an http request
with the expected HTTP status code. Depending on the endpoint and your
payload, this action might be destructive. Use with caution.


--
endpoint : str
    The URL to the endpoint to probe
method : str
    A valid http request method name, like GET, POST, PUT, DELETE, OPTIONS, or PATCH
status : int
    The expected HTTP Response status code.
vus : int
    The amount of concurrent virtual users accessing the endpoint
duration : str
    How long to probe the endpoint. Expressed as a duration string,
    i.e "20s", "1m", "1h" etc.
timeout : int
    Timeout duration for http requests. Defaults to 1 second

**Signature:**

```python
def http(endpoint: str,
         method: str = 'GET',
         status: int = 200,
         body: str = '',
         headers: dict = {},
         vus: int = 1,
         duration: str = '',
         debug: bool = False,
         timeout: int = 1) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **endpoint**      | string |  | Yes |
| **method**      | string | "GET" | No |
| **status**      | integer | 200 | No |
| **body**      | string | "" | No |
| **headers**      | mapping | {} | No |
| **vus**      | integer | 1 | No |
| **duration**      | string | "" | No |
| **debug**      | boolean | false | No |
| **timeout**      | integer | 1 | No |




**Usage:**

```json
{
  "name": "http",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk6.probes",
    "func": "http",
    "arguments": {
      "endpoint": ""
    }
  }
}
```

```yaml
name: http
provider:
  arguments:
    endpoint: ''
  func: http
  module: chaosk6.probes
  type: python
type: probe

```



