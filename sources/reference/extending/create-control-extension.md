# Create a Control Extension

A control extension implements the interface defined by the Chaos
Toolkit to support the [Controls element of the specification][spec].

[spec]: ../api/experiment.md#controls

Controls are good for changing the experiment or its environment during
execution. They have the power to impact the experiment, configuration,
secrets on the fly, which is unlike probes and actions.

## Controls Interface

When implementing a control module, you must simply define a set of functions
that are called by the Chaos Toolkit when executing the experiment.

!!! tip
    All of these functions are optional, only implement the one you need.

```python
from typing import Any, Dict, List

from chaoslib.types import Activity, Configuration, \
    Experiment, Hypothesis, Journal, Run, Secrets, Settings


def configure_control(configuration: Configuration = None,
                      secrets: Secrets = None, settings: Settings = None,
                      experiment: Experiment = None):
    """
    Configure the control's global state

    This is called once only per Chaos Toolkit's run and should be used to
    initialize any state your control may require.

    The `settings` are only passed when the control is declared in the
    settings file of the Chaos Toolkit.
    """
    pass


def cleanup_control():
    """
    Cleanup the control's global state

    Called once only during the experiment's execution.
    """
    pass


def before_loading_experiment_control(context: str, **kwargs):
    """
    before loading the experiment from its source.

    The context is the file path or URL given to the loader. Use this loader
    if you want to interact with that source before it is loaded.
    """
    pass


def after_loading_experiment_control(context: str, state: Experiment, **kwargs):
    """
    after loading the experiment from its source.

    Use this loader if you want to interact with the experiment once it's been
    loaded and parsed but before the validation or execution take place.
    """
    pass


def before_experiment_control(context: Experiment,
                              configuration: Configuration = None,
                              secrets: Secrets = None, **kwargs):
    """
    before-control of the experiment's execution

    Called by the Chaos Toolkit before the experiment's begin but after the
    configuration and secrets have been loaded.
    """
    pass


def after_experiment_control(context: Experiment, state: Journal, 
                             configuration: Configuration = None,
                             secrets: Secrets = None, **kwargs):
    """
    after-control of the experiment's execution

    Called by the Chaos Toolkit after the experiment's completed. It passes the
    journal of the execution. At that stage, the after control has no influence
    over the execution however. Please see
    https://docs.chaostoolkit.org/reference/api/journal/#journal-elements
    for more information about the journal.
    """
    pass


def before_hypothesis_control(context: Hypothesis,
                              configuration: Configuration = None,
                              secrets: Secrets = None, **kwargs):
    """
    before-control of the hypothesis's execution

    Called by the Chaos Toolkit before the steady-state hypothesis is
    applied.
    """
    pass


def after_hypothesis_control(context: Hypothesis, state: Dict[str, Any],
                             configuration: Configuration = None,
                             secrets: Secrets = None, **kwargs):
    """
    after-control of the hypothesis's execution

    Called by the Chaos Toolkit after the steady-state hypothesis is
    complete. The `state` contains the result of the hypothesis. Refer to
    https://docs.chaostoolkit.org/reference/api/journal/#steady-state-outcomes
    for the description of that state.
    """
    pass


def before_method_control(context: Experiment, 
                          configuration: Configuration = None,
                          secrets: Secrets = None, **kwargs):
    """
    before-control of the method's execution

    Called by the Chaos Toolkit before the activities of the method are
    applied.
    """
    pass


def after_method_control(context: Experiment, state: List[Run], 
                         configuration: Configuration = None,
                         secrets: Secrets = None, **kwargs):
    """
    after-control of the method's execution

    Called by the Chaos Toolkit after the activities of the method have been
    applied. The `state` is the list of activity results. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    pass


def before_rollback_control(context: Experiment, 
                            configuration: Configuration = None,
                            secrets: Secrets = None, **kwargs):
    """
    before-control of the rollback's execution

    Called by the Chaos Toolkit before the actions of the rollback are
    applied.
    """
    pass


def after_rollback_control(context: Experiment, state: List[Run], 
                           configuration: Configuration = None,
                           secrets: Secrets = None, **kwargs):
    """
    after-control of the rollback's execution

    Called by the Chaos Toolkit after the actions of the rollback have been
    applied. The `state` is the list of actions results. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    pass


def before_activity_control(context: Activity, 
                            configuration: Configuration = None,
                            secrets: Secrets = None, **kwargs):
    """
    before-control of the activity's execution

    Called by the Chaos Toolkit before the activity is applied.
    """
    pass


def after_activity_control(context: Activity, state: Run,  
                           configuration: Configuration = None,
                           secrets: Secrets = None, **kwargs):
    """
    after-control of the activity's execution

    Called by the Chaos Toolkit before the activity is applied. The result of
    the execution is passed as `state`. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    pass

```

## Use your control

Define those functions into a module that is used as a provider. For instance,
assume the above definition is stored into a module `chaosstuff.control`, in
other words a `control.py` module of the `chaosstuff` package.

The package must obviously be available to the `PYTHONPATH` in which the
`chaos` runs.

### Declare it in the experiment

Controls can be applied per-experiment only:

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

### Declare it in your settings

Controls can be also applied globally to all runs by declaring them in the
Chaos Toolkit settings file:

```yaml
controls:
    my-stuff:
        provider:
            type: python
            module: chaosstuff.control
```

## Things to note

### Unforeseen errors

The Chaos Toolkit will not let a control abort the execution of the experiment.
So if an exception is raised, it will be caught by the Chaos Toolkit, logged
and the execution will carry on.

### Interrupting the execution

While unforeseen errors in your controls cannot stop the execution, you can
interrupt the execution by raising `chaoslib.exceptions.InterruptExecution`
from any of your control functions.

Note however, this is a harsh way to terminate the execution since, none of
the rollbacks will be applied.

Here is an example:

```python
from chaoslib.exceptions import InterruptExecution


def after_activity_control(context: Activity, state: Run,  
                           configuration: Configuration = None,
                           secrets: Secrets = None, **kwargs):
    if check_stuff(state["output"]):
        raise InterruptExecution("Well things went really bad!")
```

In that case, the experiment's execution will have its `status` set to
`"interrupted"` as described [here][interrupted].

[interrupted]: ../api/journal.md#required-properties