# Create a new Chaos Toolkit Extension with Custom Probes

The Chaos Toolkit can be extended to observe specific information about your system, using probes, as well as provide custom actions that can be used from within your experiment's method. 

In this tutorial you will learn how to create a new custom Python extension to the Chaos Toolkit to expose some custom probes in order to gather more data from the observability of your system. This is done so that you can customize how you specify your Steady State Hypothesis as well as providing a custom means of gathering additional data during your experiment execution.

!!! note
    The next tutorial in this series will show how to construct custom actions as well so that those can be used within your Chaos experiment's method.

## Introducing the Extension

The extension we are going to create here will be a simple integration with [Prometheus][] to provide a couple of new probes that we can use in our Chaos Engineering experiments. The probes will be:

* `query` - Runs an instant query against a [Prometheus][] server and returns its result as-is.
* `query_interval` - Runs a range query against a [Prometheus][] server and returns its result as-is.

The `query` probe will naturally, if specified with some tolerances, be a good candidate for use as part of a [Stead State Hypothesis][steady-state] as well as a general-purpose probe.

!!! note
    There is already a [chaostoolkit-prometheus extension project](https://github.com/chaostoolkit/chaostoolkit-prometheus) and the tutorial shown here is based on how it was originally developed.

[steady-state]: /overview/concepts/#steady-state-hypothesis

## Creating a new Extension based on the Template project

To create a new project based on the Chaos Toolkit Extension Template grab the [latest released code for the template][template-latest-release] and place this code in a new project that ideally follows the naming convention of `chaostoolkit-<your extension name here>`. 

For our purposes we will create a new project based on the templates code called `chaostoolkit-prometheus`. You will also need to change any references to `chaosext` to the name of your new extension and its associated package. Once you have made those changes you should have a project contents that looks like the following:

```
.
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── chaosprometheus
│   ├── __init__.py
│   └── probes.py
├── ci.bash
├── coverage.xml
├── junit-test-results.xml
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
├── setup.py
└── tests
    └── test_probes.py
```

[template-latest-release]: https://github.com/chaostoolkit/chaostoolkit-extension-template/releases/latest

## (Optional) Create a virtual environment for your new extension

A Python virtual environment is a great way of managing your project's dependencies. We recommend creating a virtual environment for your new Chaos Toolkit extension project using the following command:

```
> python3 -m venv ~/.venvs/<your-ext-venv>
```

## Setup your extensions dependencies

Now you can added dependencies into the `requirements-dev.txt`, for dependencies you only need at development time, and `requirements.txt`, for dependencies you only need at runtime. We need a few extra dependencies to work with Prometheus:

```
logzero
requests
dateparser
maya
```

Briefly, these dependencies are useful because they:

* `logzero` - Makes it simpler to add logging to the Python extension. Also it is what the core Chaos Toolkit uses so this is consistent.
* `requests` - Adds an HTTP client for working against the Prometheus API
* `dateparser` - Provides support for manupulating dates and time, including generalinh time/date ranges.
* `maya` - Provides support for serialising dates and times to and from the dates and times needed for the Prometheus API.

With those changes made you can now install your dependencies for your development work using the following command:

```
> python setup.py develop
```

## Create tests for the new probes

You're now ready to start coding up your new probes for Prometheus. Using TDD, you can construct tests that exercise the success and failure scenarios of the expected probe functions in a `tests/test_probes.py` module:

``` python
# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock

from chaoslib.exceptions import FailedActivity
from chaosprometheus.probes import query, query_interval


def test_failed_parsing_when_date():
    with pytest.raises(FailedActivity) as exc:
        query("request_processing_seconds_count", when="2 mns ago")
    assert "failed to parse '2 mns ago'" in str(exc)


def test_failed_parsing_start_date():
    with pytest.raises(FailedActivity) as exc:
        query_interval("request_processing_seconds_count", start="2 mns ago",
                       end="now")
    assert "failed to parse '2 mns ago'" in str(exc)


def test_failed_parsing_end_date():
    with pytest.raises(FailedActivity) as exc:
        query_interval("request_processing_seconds_count",
                       start="2 minutes ago", end="right now")
    assert "failed to parse 'right now'" in str(exc)


def test_failed_running_query():
    with requests_mock.mock() as m:
        m.get(
            "http://localhost:9090/api/v1/query_range", status_code=400,
            text="Bad Request")

        with pytest.raises(FailedActivity) as ex:
            query_interval(query="request_processing_seconds_count",
                           start="2 minutes ago", end="now")
    assert "Prometheus query" in str(ex)
```

## Create the new Probes

Finally it's time to create the new probes to meet the needs as specified by your tests in a file called `chaosprometheus/probes.py`:

``` python
# -*- coding: utf-8 -*-
from typing import Any, Dict

import dateparser
from logzero import logger
import maya
import requests

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets

__all__ = ["query", "query_interval"]


def query(query: str, when: str = None, timeout: float = None,
          configuration: Configuration = None,
          secrets: Secrets = None) -> Dict[str, Any]:
    """
    Run an instant query against a Prometheus server and returns its result
    as-is.
    """
    base = (configuration or {}).get(
        "prometheus_base_url", "http://localhost:9090")
    url = "{base}/api/v1/query".format(base=base)

    params = {"query": query}

    if timeout is not None:
        params["timeout"] = timeout

    if when:
        when_dt = dateparser.parse(when, settings={
            'RETURN_AS_TIMEZONE_AWARE': True})
        if not when_dt:
            raise FailedActivity("failed to parse '{s}'".format(s=when))
        params["time"] = maya.MayaDT.from_datetime(when_dt).rfc3339()

    logger.debug("Querying with: {q}".format(q=params))

    r = requests.get(
        url, headers={"Accept": "application/json"}, params=params)

    if r.status_code != 200:
        raise FailedActivity(
            "Prometheus query {q} failed: {m}".format(q=str(params), m=r.text))

    return r.json()


def query_interval(query: str, start: str, end: str, step: int = 1,
                   timeout: float = None, configuration: Configuration = None,
                   secrets: Secrets = None) -> Dict[str, Any]:
    """
    Run a range query against a Prometheus server and returns its result as-is.

    The `start` and `end` arguments can be a RFC 3339 date or expressed more
    colloquially such as `"5 minutes ago"`.
    """
    base = (configuration or {}).get(
        "prometheus_base_url", "http://localhost:9090")
    url = "{base}/api/v1/query_range".format(base=base)

    params = {"query": query}

    if timeout is not None:
        params["timeout"] = timeout

    if step:
        params["step"] = step

    start_dt = dateparser.parse(start, settings={
        'RETURN_AS_TIMEZONE_AWARE': True})
    if not start_dt:
        raise FailedActivity("failed to parse '{s}'".format(s=start))
    params["start"] = maya.MayaDT.from_datetime(start_dt).rfc3339()

    end_dt = dateparser.parse(end, settings={
        'RETURN_AS_TIMEZONE_AWARE': True})
    if not end_dt:
        raise FailedActivity("failed to parse '{s}'".format(s=end))
    params["end"] = maya.MayaDT.from_datetime(end_dt).rfc3339()

    logger.debug("Querying with: {q}".format(q=params))

    r = requests.get(
        url, headers={"Accept": "application/json"}, params=params)

    if r.status_code != 200:
        raise FailedActivity(
            "Prometheus query range {q} failed: {m}".format(
                q=str(params), m=r.text))

    return r.json()
```

## Execute the tests

With the implementations in place you can now run your tests to assert that everything is as expected:

```
> pytest
```

And you should then get an output similar to the following:

```
> pytest
Test session starts (platform: darwin, Python 3.6.2, pytest 3.3.0, pytest-sugar 0.9.0)
cachedir: .cache
rootdir: /Users/russellmiles/code/src/github.com/chaostoolkit/chaostoolkit-prometheus, inifile: pytest.ini
plugins: sugar-0.9.0, cov-2.5.1

 tests/test_probes.py::test_failed_parsing_when_date ✓                                                                                         25% ██▌       
 tests/test_probes.py::test_failed_parsing_start_date ✓                                                                                        50% █████     
 tests/test_probes.py::test_failed_parsing_end_date ✓                                                                                          75% ███████▌  
 tests/test_probes.py::test_failed_running_query ✓                                                                                            100% ██████████
------------------ generated xml file: /Users/russellmiles/code/src/github.com/chaostoolkit/chaostoolkit-prometheus/junit-test-results.xml ------------------

---------- coverage: platform darwin, python 3.6.2-final-0 -----------
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
chaosprometheus/probes.py      45      9    80%   29, 36-47, 66, 93
---------------------------------------------------------
TOTAL                          46      9    80%

1 file skipped due to complete coverage.
Coverage XML written to file coverage.xml


Results (3.64s):
       4 passed
```

## Using your new probes

That's all you need to do! You have now created your first Python-based extension to the Chaos Toolkit. You can now release and distribute this project using a system such as PyPi so that it can be installed and called from Chaos Toolkit experiments all over the world.

As an example, here is a snippet showing how a chaos experiment could look using your new [Prometheus][] `query` probe:

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
[Prometheus]: https://prometheus.io/

## Next Steps

In the next tutorial we will take a look at how to create an extension that includes actions that can be called to inject failure from your chaos experiments.
