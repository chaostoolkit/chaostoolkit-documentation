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
  an action is triggered
* close probes: appropriate to observe the close state after an action is 
  triggered

Both probes have the same structure and only differ about when you apply them.

#### Action

An action interacts with the system, either stopping or starting a service, or
maybe triggering a resource failure.

Although an experiment can declare many actions, it is better to keep the
hypothesis comprehensible to make the analysis simpler and conclusive.

### Background Activities

Activities run sequentially by default. Sometimes, you may wish to trigger an
action and observe the system for a while. To do so, you can declare that
activities are executed in background. The experiment will start tha backrground
activity and move right away to the next activity. It will wait for all
background activities to complete before terminating.

To declare a background activity, add the following flag to its declaration:

```json
"background": true
```

### Secrets

An experiment may require some secrets to pass to its activities when executed.
The Chaos Toolkit supports for declaring those by either inlining the values
in the experiment itself, or by referencing environmental variables.
Eventually, it will likely support fetching secrets from products such as
[vault][].

[vault]: https://www.vaultproject.io

Declare secrets at the top of your experiment as follows:

```json
"secrets": {
    "prometheus": {
        "username": "env.PROMETHEUS_USERNAME",
        "password": "env.PROMETHEUS_PASSWORD"
    }
}
```

Secrets are loaded when the experiment starts and fails if one of them cannot
be found in the current environment.

Then, reference it from any activity by using:

```json
"secrets": "prometheus"
```

The Chaos Toolkit, will inject those secrets down to the activity function.

!!! note
    The Chaos Toolkit does not log secrets nor does it store them into the
    resulting report it generates.

### Structure Schema

An experiment is stored in a JSON-encoded file. It has the following
[schema][schema].

[schema]: https://github.com/chaostoolkit/chaostoolkit-documentation/blob/master/schema.json
