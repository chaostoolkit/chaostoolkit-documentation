# Learn all about Controls

Controls are one of the most powerful tool available to a Chaos Toolkit author
or operator. They work at a different level than actions and probes however.

Indeed, controls are executed at various times during the execution of an
experiment and have direct impacts over it, to the point where they can
change its content entirely or even interrupt at will. In that regard, controls
are most often used by operators of Chaos Toolkit experiments to exercise
runtime adjustments or checks during the execution.

## A first look at a control

A control is simply a callback applied by Chaos Toolkit during the execution
of an experiment. 

!!! warning
    Currently, controls can only be implemented in Python but this may change.
    The entire page is written for Python controls

The fact a control is a callback means Chaos Toolkit is responsible for
calling it, once it has been declared.

Below is a basic control that is applied after the experiment has finished
its execution, assuming the next piece of code lives in a Python module named
`chaosstuff/control.py`:

```python
from chaoslib.types import Activity, Configuration, Experiment, Journal, Secrets


def after_experiment_control(context: Experiment, state: Journal, 
                             configuration: Configuration = None,
                             secrets: Secrets = None, **kwargs):
    pass
```

### Declaring a control

A control can be declared in two places:

* in the experiment itself
* in the global settings of your installation

When declared in the experiment itself, controls only impact this particular
experiment. Conversely, when declared in the settings, controls impact all
experiments run with said settings, usually all experiments of the current
user.

In an experiment, you declare a control as follows:

```json
"controls": [
    {
        "name": "my-stuff",
        "provider": {
            "type": "python",
            "module": "chaosstuff.control"
        }
    }
]
```

In the [settings][] file:

[settings]: ../usage/settinds.md

```yaml
controls:
    my-stuff:
        provider:
            type: python
            module: chaosstuff.control
```

As you can notice, controls are declared in a very similar way to actions and
probes.

