## Experiment

### Objective

A Chaos experiment is an hypothesis you make about your system. The Chaos
Toolkit runs it and observes the state of the system. On completion, a report
is generated for analsyis.

### Overview

An experiment has a simple structure with the following elements:

* some high-level metadata
* a method: a sequence of activities that together represent the experiment

The metadata found in the experiment helps the shared understanding of its
context and objective among the team. In other words, the metadata target the
humans dealing with this experiment.

The method is the meat of the experiment. It tells the Chaos Toolkit what to
run. It is a sequence of activities:

* actions
* probes

Actions represent the enactment of your hypothesis, e.g. "Let's shutdown
service A and confirm this should not bring our entire system down by ripple
effect".

Probes observe the system as the experiment runs. Two kinds of probes can be
declared: steady and close. A steady probe looks for the state of a resource
or the whole system before an action (or another probe) is applied. Likewsise,
the close probe look for the state after the action was applied.

Probes inform your about what was happening in your system as the experiment
took place but also the effect of actioning the system.

### Method Activities

#### Probe

A probe lets you observe your system (or any external system relevant to the
experiment). Think of a probe as a view on a specific aspect of your system.
Through probes, you can assess the conditions of your system at a
given point of your experiment.

As seen before, the Chaos Toolkit defines two kinds of probes:

* steady probes: appropriate to observe the steady state of your system before
  an action is trggered
* close probes: appropriate to observe the close state after an action is 
  triggered

Both probes have the same structure and only differ about when you apply them.

#### Action

An action interacts with the system, either stopping or starting a service, or
maybe triggering a resource failure.

Although an experiment can declare many actions, it is better to keep the
hypothesis comprehensible to make the analysis simpler and conclusive.


### Structure Schema

An experiment is stored in a JSON-encoded file. It has the following schema:

```json
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "required": [
        "method",
        "title" 
    ],
    "properties": {
        "description": {
            "type": "string",
            "description": "Describing the Chaos experiment to provide context"
        },
        "title": {
            "type": "string",
            "description": "The high-level title of the Chaos experiment"
        },
        "method": {
            "type": "array",
            "description": "The activities to try our the hypothesis",
            "items": [
                { "$ref": "#definitions/step" }   
            ]
        }
    },
    "definitions": {
        "step": {
            "type": "object",
            "title": "A step of the method. Made of actions and/or probes",
            "properties": {
                "title": {
                    "type": "string",
                    "title": "A description of the step"
                }
            },
            "additionalProperties": {
                "anyOf": [
                    {
                        "$ref": "#/definitions/probes"
                    },
                    {
                        "$ref": "#/definitions/action"
                    }
                ]
            }
        },
        "action": {
            "type": "object",
            "description": "The hypothesis enactment",
            "required": [
                "arguments",
                "layer",
                "title",
                "type"
            ],
            "properties": {
                "arguments": {
                    "type": "object",
                    "properties": {}
                },
                "type": {
                    "type": "string"
                },
                "layer": {
                    "type": "string"
                },
                "title": {
                    "type": "string"
                },
                "negate": {
                    "type": "boolean",
                    "title": "Sould the Chaos Toolkit take the opposite of the action's result?",
                    "enum": [true, false]
                },
                "timeout": {
                    "type": "number",
                    "title": "The maximum duration the Chaos toolkit will wait for the action to complete"
                },
                "pauses": {
                    "type": "number",
                    "title": "Pauses the Chaos toolkit may pause before or after an action",
                    "properties": {
                        "before": {
                            "type": "number",
                            "title": "How long before triggering the action (in seconds)"
                        },
                        "after": {
                            "type": "number",
                            "title": "How long after the action was triggered (in seconds)"
                        }
                    }
                }
            }
        },
        "probe": {
            "type": "object",
            "oneOf": [
                {
                    "$ref": "#/definitions/python-probe"
                },
                {
                    "$ref": "#/definitions/process-probe"
                },
                {
                    "$ref": "#/definitions/http-probe"
                }
            ]
        },
        "python-probe": {
            "type": "object",
            "required": [
                "layer",
                "title",
                "type",
                "module",
                "func"
            ],
            "properties": {
                "type": {
                    "type": "string",
                    "title": "The kind of probe implementation",
                    "pattern": "^(python)$"
                },
                "layer": {
                    "type": "string",
                    "title": "The layer the probe applies at",
                    "enum": [
                        "infrastructure",
                        "platform",
                        "application"
                    ]
                },
                "title": {
                    "type": "string",
                    "title": "A short description of the probe"
                },
                "arguments": {
                    "type": "object",
                    "title": "A K->V mapping that is passed as-is to the probe",
                    "properties": {}
                },
                "negate": {
                    "type": "boolean",
                    "title": "Sould the Chaos Toolkit take the opposite of the probe's result?",
                    "enum": [true, false]
                },
                "module": {
                    "type": "string",
                    "title": "A Python module path the Chaos Toolkit can import at runtime"
                },
                "func": {
                    "type": "string",
                    "title": "A function name exposed in the module"
                }
            }
        },
        "process-probe": {
            "type": "object",
            "required": [
                "layer",
                "title",
                "type",
                "path"
            ],
            "properties": {
                "type": {
                    "type": "string",
                    "title": "The kind of probe implementation",
                    "pattern": "^(process)$"
                },
                "layer": {
                    "type": "string",
                    "title": "The layer the probe applies at",
                    "enum": [
                        "infrastructure",
                        "platform",
                        "application"
                    ]
                },
                "title": {
                    "type": "string",
                    "title": "A short description of the probe"
                },
                "arguments": {
                    "type": "object",
                    "title": "A K->V mapping that is passed as-is to the probe",
                    "properties": {}
                },
                "negate": {
                    "type": "boolean",
                    "title": "Sould the Chaos Toolkit take the opposite of the probe's result?",
                    "enum": [true, false]
                },
                "path": {
                    "type": "string",
                    "title": "The path to an executable to call"
                }
            }
        },
        "http-probe": {
            "type": "object",
            "required": [
                "layer",
                "title",
                "type",
                "url"
            ],
            "properties": {
                "type": {
                    "type": "string",
                    "title": "The kind of probe implementation",
                    "pattern": "^(http)$"
                },
                "layer": {
                    "type": "string",
                    "title": "The layer the probe applies at",
                    "enum": [
                        "infrastructure",
                        "platform",
                        "application"
                    ]
                },
                "title": {
                    "type": "string",
                    "title": "A short description of the probe"
                },
                "arguments": {
                    "type": "object",
                    "title": "A K->V mapping that is passed as-is to the probe",
                    "properties": {}
                },
                "url": {
                    "type": "string",
                    "title": "A deferencable URL"
                },
                "method": {
                    "type": "string",
                    "title": "A valid HTTP method",
                    "enum": [
                        "GET",
                        "POST",
                        "PUT",
                        "DELETE",
                        "PATCH"
                    ]
                },
                "headers": {
                    "type": "object",
                    "properties": {}
                },
                "negate": {
                    "type": "boolean",
                    "title": "Sould the Chaos Toolkit take the opposite of the probe's result?",
                    "enum": [true, false]
                }
            }
        },
        "probes": {
            "type": "object",
            "properties": {
                "steady": {
                    "$ref": "#/definitions/probe"
                },
                "close": {
                    "$ref": "#/definitions/probe"
                }
            }
        }
    }
}
```
