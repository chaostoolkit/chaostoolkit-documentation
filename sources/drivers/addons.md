# Extension `chaosaddons`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.3.0 |
| **Repository**        | https://github.com/chaostoolkit/chaostoolkit-addons |



This project provides a set of commnly requested actions, probes, tolerances
or controls that can benefit the community.

## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-addons
```

## Develop

### Test

To run the tests for the project execute the following:

```
$ pytest
```

### Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/



## Exported Controls



### bypass




Sets the `dry` property on activities that match either by type or by names.

This allows to bypass some activities in certain contexts. For instance, you
want to run on development but not in production certain actions.

For instance, to bypass the execution of the `say-hello` activity:

```json
"controls": [
        {
            "name": "bypass-actions",
            "provider": {
                "type": "python",
                "module": "chaosaddons.controls.bypass",
                "arguments": {
                    "target_names": [
                        "say-hello"
                    ]
                }
            }
        }
    ],
```

For instance, to bypass the execution of all actions in the experiment:

```json
"controls": [
        {
            "name": "bypass-actions",
            "provider": {
                "type": "python",
                "module": "chaosaddons.controls.bypass",
                "arguments": {
                    "target_type": "action"
                }
            }
        }
    ],
```



This module exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment Loading**       | False | False |
| **Experiment**               | True | False |
| **Steady-state Hypothesis**  | False | False |
| **Method**                   | False | False |
| **Rollback**                 | False | False |
| **Activities**               | True | True |

In addition, the controls may define the followings:

|            Level             |             Enabled             |
| -----------------------------| ------------------------------ |
| **Validate Control**       | False |
| **Configure Control**       | False |
| **Cleanup Control**       | False |

To use this control module, please add the following section to your experiment:

```json
{
  "controls": [
    {
      "name": "chaosaddons",
      "provider": {
        "type": "python",
        "module": "chaosaddons.controls.bypass"
      }
    }
  ]
}
```

```yaml
controls:
- name: chaosaddons
  provider:
    module: chaosaddons.controls.bypass
    type: python

```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.



### safeguards




The safeguard control provides a mechanism to keep an eye on the system
while running an experiment to decide if the experiment ought to stop as soon
as possible or not.

For instance, let's say your system detects a dire condition that has nothing
to do with this experiment. It may decide it's time for the experiment to
terminate as it could create even more noise or problems.

To use this control, simply add the following to your global (or per
experiment) controls block:

```json
"controls": [
    {
        "name": "safeguard",
        "provider": {
            "type": "python",
            "module": "chaosaddons.controls.safeguards",
            "arguments": {
                "probes": [
                    {
                        "name": "safeguard_1",
                        "type": "probe",
                        "provider": {
                            "type": "python",
                            "module": "mymodule",
                            "func": "checkstuff"
                        },
                        "background": true,
                        "tolerance": true
                    },
                    {
                        "name": "safeguard_2",
                        "type": "probe",
                        "provider": {
                            "type": "python",
                            "module": "mymodule",
                            "func": "checkstuff"
                        },
                        "tolerance": true
                    },
                    {
                        "name": "safeguard_3",
                        "type": "probe",
                        "provider": {
                            "type": "python",
                            "module": "mymodule",
                            "func": "checkstuff"
                        },
                        "frequency": 2,
                        "tolerance": true
                    }
                ]
            }
        }
    }
],
```

In this example, we declare three safeguard probes. The first one will run
once in the background as soon as possible. The second one will run once
before the experiment starts. The third one will run repeatedly every 2
seconds.

If either of them doesn't meet its tolerance, the entire execution will
terminate as soon as possible and leave the status of the experiment to
`interrupted`.

Probes that do not declare the `background` or `frequency` properties are meant
to run before the experiment really starts and will block until they are all
finished. This offers a mechanism for pre-checking the system's health.

When the properties are set, the probes run as soon as possible but do not
block the experiment from carrying on.

Bear in mind that your probes can also block the process from exiting. This
means that while the experiment has ended, your probe could be not returning
and therefore blocking the process. Make sure your probe do not make blocking
calls for too long.



This module exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment Loading**       | False | False |
| **Experiment**               | True | True |
| **Steady-state Hypothesis**  | False | False |
| **Method**                   | False | False |
| **Rollback**                 | False | False |
| **Activities**               | False | False |

In addition, the controls may define the followings:

|            Level             |             Enabled             |
| -----------------------------| ------------------------------ |
| **Validate Control**       | True |
| **Configure Control**       | True |
| **Cleanup Control**       | False |

To use this control module, please add the following section to your experiment:

```json
{
  "controls": [
    {
      "name": "chaosaddons",
      "provider": {
        "type": "python",
        "module": "chaosaddons.controls.safeguards"
      }
    }
  ]
}
```

```yaml
controls:
- name: chaosaddons
  provider:
    module: chaosaddons.controls.safeguards
    type: python

```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.



### synchronization




This module exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment Loading**       | False | False |
| **Experiment**               | False | True |
| **Steady-state Hypothesis**  | False | False |
| **Method**                   | False | False |
| **Rollback**                 | False | False |
| **Activities**               | False | False |

In addition, the controls may define the followings:

|            Level             |             Enabled             |
| -----------------------------| ------------------------------ |
| **Validate Control**       | False |
| **Configure Control**       | False |
| **Cleanup Control**       | False |

To use this control module, please add the following section to your experiment:

```json
{
  "controls": [
    {
      "name": "chaosaddons",
      "provider": {
        "type": "python",
        "module": "chaosaddons.controls.synchronization"
      }
    }
  ]
}
```

```yaml
controls:
- name: chaosaddons
  provider:
    module: chaosaddons.controls.synchronization
    type: python

```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.




## Exported Activities



### controls




### utils



***

#### `idle_for`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaosaddons.utils.idle |
| **Name**              | idle_for |
| **Return**              | null |


Pauses the experiment without blocking the process completely.

**Signature:**

```python
def idle_for(duration: float) -> None:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **duration**      | number |  | Yes |




**Usage:**

```json
{
  "name": "idle-for",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaosaddons.utils.idle",
    "func": "idle_for",
    "arguments": {
      "duration": null
    }
  }
}
```

```yaml
name: idle-for
provider:
  arguments:
    duration: null
  func: idle_for
  module: chaosaddons.utils.idle
  type: python
type: ''

```



