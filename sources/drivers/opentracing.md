# Extension `chaostracing`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.2.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-opentracing |



[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-opentracing.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-opentracing)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-opentracing.svg)](https://www.python.org/)

This project is an extension for the Chaos Toolkit for [OpenTracing 2][].

[opentracing]: https://opentracing.io/

Here is an example of what it could look like with the Jaeger backend.

![OpenTracing](https://github.com/chaostoolkit-incubator/chaostoolkit-opentracing/raw/master/example.png "Open Tracing with Jaeger")


## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
pip install -U chaostoolkit-opentracing
```

## Usage

Currently, this extension only provides control support to send traces to
your provider during the execution of the experiment. It does not yet expose
any probes or actions per-se.

### Declare within the experiment

To use this control, you can declare it on a per experiment basis like this:


```json
{
    "configuration": {
        "tracing_provider": "jaeger",
        "tracing_host": "127.0.0.1",
        "tracing_port": 6831,
        "tracing_propagation": "b3"
    },
    "controls": [
        {
            "name": "opentracing",
            "provider": {
                "type": "python",
                "module": "chaostracing.control"
            }
        }
    ]
}
```

This will automatically create a [Jaeger][] client to emit traces onto the
address `127.0.0.1:6831` (over UDP).

### Declare within the settings

You may also declare the control to be applied to all experiments by declaring
the control from within the [Chaos Toolkit settings file][ctksettings]. In that
case, you do not need to set the configuration or the controls at the
experiment level and the control will be applied to every experiments you run.

```yaml
controls:
  opentracing:
    provider:
      type: python
      module: chaostracing.control
      arguments:
        provider: jaeger
        host: 127.0.0.1
        port: 6831
        propagation: b3
```

[ctksettings]: https://docs.chaostoolkit.org/reference/usage/cli/#configure-the-chaos-toolkit
[jaeger]: https://www.jaegertracing.io/

## Send traces from other extensions

You may also access the tracer from other extensions as follows.

For instance, assuming you have an extension that makes a HTTP call you want
to trace specifically, you could do this from your extension's code:


```python
from chaoslib import Configuration, Secrets
import requests
import opentracing

def some_function(configuration: Configuration, secrets: Secrets):
    tracer = opentracing.global_tracer()
    scope = tracer.scope_manager.active
    parent = scope.span

    with tracer.start_span("call-service1", child_of=parent) as span:
        span.set_tag('http.method','GET')
        span.set_tag('http.url', url)
        span.set_tag('span.kind', 'client')
        span.tracer.inject(span, 'http_headers', headers)

        r = requests.get(url, headers=headers)
        span.set_tag('http.status_code', r.status_code)
```

Because the opentracing exposes a noop tracer when non has been initialized,
it should be safe to have that code in your extensions without having to
determine if the extension has been enabled in the experiment.

Please note that, Open Tracing scope cannot be shared across threads
(while spans can). So, when running this in a background activity, the tracer
will not actually be set to the one that was initialized.

## Open Tracing Provider Support

For now, only the Jaeger tracer is supported but [other backends][backends]
will be added as need be in the future.

[backends]: https://opentracing.io/docs/supported-tracers/

### Jaeger tracer

To install the necessary dependencies for the Jaeger tracer, please run:

```
pip install -U jaeger-client~=4.1
```

## Test

To run the tests for the project execute the following:

```
pytest
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


## Exported Controls
This package exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment**               | True | True |
| **Steady-state Hypothesis**  | True | True |
| **Method**                   | True | True |
| **Rollback**                 | True | True |
| **Activities**               | True | True |

To use this control module, please add the following section to your experiment:

```json
{
  "name": "chaostracing",
  "provider": {
    "type": "python",
    "module": "chaostracing.control"
  }
}
```

```yaml
name: chaostracing
provider:
  module: chaostracing.control
  type: python

```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.


