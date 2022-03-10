# Chaos Engineering Concepts in the Chaos Toolkit

If you haven't already, we strongly recommend reading the fantastic
[Chaos Engineering][chaos-engineering-book] book from O'Reilly Media. This
book will give you some fantastic background on the whole Chaos Engineering
discipline, and it's free!

[chaos-engineering-book]: http://www.oreilly.com/webops-perf/free/chaos-engineering.csp

Chaos Engineering is a discipline that allows you to surface weaknesses, and
eventually build confidence, in complex and often distributed systems.

The Chaos Toolkit aims to give you the simplest experience for writing and
running your own Chaos Engineering experiments. The main concepts are all
expressed in an experiment definition, of which the following is an example
from the
[Chaos Toolkit Samples](https://github.com/chaostoolkit/chaostoolkit-samples)
project:

=== "JSON"
    ```json
    {
        "title": "System is resilient to provider's failures",
        "description": "Can our consumer survive gracefully a provider's failure?",
        "tags": [
            "service",
            "kubernetes",
            "spring"
        ],
        "steady-state-hypothesis": {
            "title": "Services are all available and healthy",
            "probes": [
                {
                    "type": "probe",
                    "name": "all-services-are-healthy",
                    "tolerance": true,
                    "provider": {
                        "type": "python",
                        "module": "chaosk8s.probes",
                        "func": "all_microservices_healthy"
                    }
                }
            ]
        },
        "method": [
            {
                "type": "action",
                "name": "stop-provider-service",
                "provider": {
                    "type": "python",
                    "module": "chaosk8s.actions",
                    "func": "kill_microservice",
                    "arguments": {
                        "name": "my-provider-service"
                    }
                },
                "pauses": {
                    "after": 10
                }
            },
            {
                "ref": "all-services-are-healthy"
            },
            {
                "type": "probe",
                "name": "consumer-service-must-still-respond",
                "provider": {
                    "type": "http",
                    "url": "http://192.168.42.58:31018/invokeConsumedService"
                }
            }
        ],
        "rollbacks": []
    }
    ```
=== "YAML"
    ```yaml
    title: System is resilient to provider's failures
    description: Can our consumer survive gracefully a provider's failure?
    tags:
      - service
      - kubernetes
      - spring
    steady-state-hypothesis:
        title: Services are all available and healthy
        probes:
          - type: probe
            name: all-services-are-healthy
            tolerance: true
            provider:
              type: python
              module: chaosk8s.probes
              func: all_microservices_healthy
    method:
      - type: action
        name: stop-provider-service
        provider:
          type: python
          module: chaosk8s.actions
          func: kill_microservice
          arguments:
            name: my-provider-service
        pauses:
          after: 10
      - ref: all-services-are-healthy
      - type: probe
        name: consumer-service-must-still-respond
        provider:
          type: http
          url: http://192.168.42.58:31018/invokeConsumedService
    rollbacks: []
    ```

The key concepts of the Chaos Toolkit are `Experiments`,
`Steady State Hypothesis` and the experiment's `Method`. The `Method`
contains a combination of `Probes` and `Actions`.

## Experiments

A Chaos Toolkit experiment is provided in a single file and is currently
expressed in JSON.

## Steady State Hypothesis

A Steady State Hypothesis describes "what normal looks like" for your system
in order for the experiment to surface information about weaknesses when compared against the declared "normal" tolerances of what is measured.

The Chaos Toolkit uses the Steady State Hypothesis for two purposes. It is used as a check before an experiment is run that the target system is in a recognised ***normal*** state. It is also used as the template for comparison of the state of your system ***after*** the experiment has been run, forming the results provided by the experiment's report.

## Method

An experiment's activities are contained within its `Method` block.

## Probes

A probe is a way of observing a particular set of conditions in the system that
is undergoing experimentation.

## Actions

An action is a particular activity that needs to be enacted on the system under
experimentation.

## Rollbacks

An experiment may define a sequence of actions that revert what was undone
during the experiment.

## Controls

An experiment may declare a set of controls which have an impact over the
execution of the experiment itself. Controls are operational elements rather
than experimental.
