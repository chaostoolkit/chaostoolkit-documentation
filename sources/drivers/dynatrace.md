# Extension `chaosdynatrace`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-dynatrace |



![Build](https://github.com/chaostoolkit-incubator/chaostoolkit-dynatrace/workflows/Build/badge.svg)

[Dynatrace][dynatrace] support for the [Chaos Toolkit][chaostoolkit].

[dynatrace]: https://www.dynatrace.es/
[chaostoolkit]: http://chaostoolkit.org/

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
pip install chaostoolkit-dynatrace
```

## Usage

To use this package, you must create have access to a Dynatrace instance via
[DynatraceApi][]  and be allowed to connect to it.

[DynatraceApi]:https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/

the access credentials to the api must be specified in the configuration section

```json
{

    "configuration": {
        "dynatrace": {
            "dynatrace_base_url": "$dynatrace_base_url",
            "dynatrace_token": "$dynatrace_token"
        }
    }
}
```

This package only exports probes to get some aspects of your system 
monitored by Dynatrace.

Here is an example of how to get the failure rate of a service in Dynatrace.
for this example, the api for validate de failure rate is [Metric-v1][mv1]

[mv1]:https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v1/


```json
{
    "type": "probe",
    "name": "get-failure-rate-services",
    "provider": {
        "type": "python",
        "module": "chaosdynatrace.probes",
        "func": "failure_rate",
        "arguments": {
            "entity": "SERVICE-665B05BC92550119",
            "relative_time":"30mins",
            "failed_percentage": 1
        }
    }
}
```

The probe returns true if the api request failure percentage is less than 
"failed_percentage" or raises an exception when an error is met.


The result is not further process and should be found in the generated report
of the experiment run.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

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

### Add new Dynatrace API Support

Once you have setup your environment, you can start adding new
[Dynatrace API support] [dynatraceapi] by adding new actions, probes and entire sub-packages
for those.

[dynatraceapi]: https://www.dynatrace.com/support/help/dynatrace-api




## Exported Activities



### probes



***

#### `failure_rate`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosdynatrace.probes |
| **Name**              | failure_rate |
| **Return**              | boolean |


Validates the failure rate of a specific service.
Returns true if the failure rate is less than the expected failure rate
For more information check the api documentation.
https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v1/

**Signature:**

```python
def failure_rate(entity: str,
                 relative_time: str,
                 failed_percentage: int,
                 configuration: Dict[str, Dict[str, str]],
                 secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **entity**      | string |  | Yes |
| **relative_time**      | string |  | Yes |
| **failed_percentage**      | integer |  | Yes |




**Usage:**

```json
{
  "name": "failure-rate",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosdynatrace.probes",
    "func": "failure_rate",
    "arguments": {
      "entity": "",
      "relative_time": "",
      "failed_percentage": 0
    }
  }
}
```

```yaml
name: failure-rate
provider:
  arguments:
    entity: ''
    failed_percentage: 0
    relative_time: ''
  func: failure_rate
  module: chaosdynatrace.probes
  type: python
type: probe

```



