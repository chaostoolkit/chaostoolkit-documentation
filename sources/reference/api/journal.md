# Experiment Journal

## Introduction

This document describes the syntax and grammar of a Chaos Engineering
experiment's output, called a journal. One should be able to walkthrough the
experiment's run through its journal alone.

This specification makes sense in regards to the
[Experiment specification](experiment.md) itself. It is indeed a mirror to that
document.

[action]: experiment.md#action
[method]: experiment.md#method
[hypo]: experiment.md#steady-state-hypothesis
[rollbacks]: experiment.md#rollbacks
[probe]: experiment.md#probe
[probes]: experiment.md#probe

## Conventions Used in This Document

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [RFC 2119][rfc2119].

[rfc2119]: https://tools.ietf.org/html/rfc2119

The terms "JSON", "JSON text", "JSON value", "member", "element", "object",
"array", "number", "string", "boolean", "true", "false", and "null" in this
document are to be interpreted as defined in [RFC 7159][rfc7159].

[rfc7159]: https://tools.ietf.org/html/rfc7159

### Other formats

While this specification uses JSON to define its elements, implementations may
allow loading from other formats, such as [YAML][yaml]. As long as the output
of such format respects the specification herein.

[yaml]: http://yaml.org/spec/

## Journal Elements

### Overview

A Journal is one potential output of a
[Chaos Engineering experiment](experiment.md). The objective of such journal is
to collect all events that took place during the experiment's run.

The journal contains static information, such as the experiment that was run,
as well as runtime entries.

### Format

A journal is a JSON object.

### Required Properties

A journal MUST declare:

* a `experiment` property
* a `status` property
* a `start` property
* a `end` property
* a `duration` property

The `experiment` property MUST be a copy of the run experiment as-is and is
therefore a JSON object. It MUST follow the [Experiment](experiment.md)
definition.

The ̀`status` property MUST be a JSON string, one of:

* `"completed"`: when the experiment runs fully. It does not indicate the
  activities in the experiment suceeded, only that they were executed as
  expected
* `"failed"`: when one of the activity reports a failed condition
* `"aborted"`: when the experiment breaks for unforeseen reason
* `"interrupted"`: when the experiment is interrupted (for instance after a
  signal is received)

!!! note
    It is important to understand the `"completed"` status expresses that
    everything ran all the way. An action may not have resulted in what the
    operator wanted but it did not fail. Always review the entire journal to
    fully appreciate the actual outcome of the experiment.
    
    There are two reasons it could be marked as `"failed"`. Either a tolerance
    failed or if an extension made a check for a condition. So, for
    instance, let's say the extension made a HTTP call to your service, that
    call returned a 400 rather than 200. If the extension was not designed to
    care for this difference, then the status will be marked as `"completed"`.
    However, if the extension validated the HTTP response, it may have decided
    to fail the action which would lead to a ̀ "failed"` status.

    The `"aborted"` and `"interrupted"` are different, the former means of a
    crash somehow (say, because of a bug). The latter indicates a signal was
    received. Both MUST bail the entire process.

The `start` property MUST be a JSON string formatted as per [RFC 3339](rfc3339)
in UTC timezone.

The `end` property MUST be a JSON string formatted as per [RFC 3339](rfc3339) in
UTC timezone.

[rfc3339]: https://www.ietf.org/rfc/rfc3339.txt

The `duration` MUST be a JSON number of difference between the `end` datetime
and the `start` datetime.

### Recommended Properties

In addition to those required properties, the journal SHOULD also declare the
followings:

* a `steady_states` property
* a `run` property
* a `rollbacks` property

The `steady_states` property MUST be a JSON object defining the result of the
[steady state hypothesis][hypo] outcome.

The `run` property MUST be a JSON array defining the result of each activity
in the [method][] element of the experiment.

The `rollbacks` property MUST be a JSON array defining the result of each
[action][] in the [rollbacks][] element of the experiment.

### Optional Properties

In addition to those required properties, the journal MAY also declare the
followings:

* a `platform` property
* a `node` property

The `platform` property MUST be a JSON string defining the machine on which
the experiment was executed. The content is free form but may be similar to the
output of the `uname -a` command.

The `node` property MUST be a JSON string representing the name of the machine
where the experiment was run. The content is free form.

## Steady State

The `steady_states` property holds the outcomes of the steady state hypothesis.

The `steady_states` property MAY declare the following properties:

* a `before` property
* a `after` property

The `before` property MUST be a JSON object describing the outcome of the
hypothesis run before the [method][] is executed.

The `after` property MUST be a JSON object describing the outcome of the
hypothesis run after the [method][] is executed.

Notice that either of those properties MAY be missing if they were not run.

### Steady State Outcomes

Both the `before` and `after` properties follow the same definition.

* a `steady_state_met` property
* a `probes` property

The `steady_state_met` property MUST be a JSON boolean. It MUST be `true` if the
steady state hypothesis was met, `false` otherwise.

A steady state is met when all its probes matched their tolerance.
A steady state is not met at the first non-matching tolerance probe.

The `probes` property MUST be a JSON array of [probes][] results.

Each probe result MUST declare the following properties:

* a `activity` property
* a `status` property
* a `start` property
* a `end` property
* a `duration` property
* a `tolerance_met` property
* a `output` property

The `activity` property MUST be a JSON object, a raw copy of the executed
[probe][].

The `status` property MUST be a JSON string, one of `"succeeded"` or `"failed"`.

The `start` property MUST be a JSON string formatted as per [RFC 3339](rfc3339)
in UTC timezone.

The `end` property MUST be a JSON string formatted as per [RFC 3339](rfc3339) in
UTC timezone.

The `duration` MUST be a JSON number of difference between the `end` datetime
and the `start` datetime.

The `tolerance_met` MUST be a JSON boolean indicating if the probe matched its
tolerance or not.

The `output` MUST be a JSON string or `null`.

In addition, the probe result MAY contain an additional property:

* a `exception` property

This property is set when the probe failed in an unforeseeable way and MUST be
a JSON array or JSON string of the error trace. 

## Run

The `run` property holds the outcomes of the [method][] element.

The `run` property MUST be a JSON array of activity results.

Each activity result MUST declare the following properties:

* a `activity` property
* a `status` property
* a `start` property
* a `end` property
* a `duration` property
* a `output` property

The `activity` property MUST be a JSON object, a raw copy of the executed
[probe][] or [action][].

The `status` property MUST be a JSON string, one of `"succeeded"` or `"failed"`.

The `start` property MUST be a JSON string formatted as per [RFC 3339](rfc3339)
in UTC timezone.

The `end` property MUST be a JSON string formatted as per [RFC 3339](rfc3339) in
UTC timezone.

The `duration` MUST be a JSON number of difference between the `end` datetime
and the `start` datetime.

The `output` MUST be a JSON string or `null`.

In addition, the activity result MAY contain an additional property:

* a `exception` property

This property is set when the activity failed in an unforeseeable way and MUST
be a JSON array or JSON string of the error trace.

## Rollbacks

The `rollbacks` property holds the outcomes of the [rollbacks][] element.

The `rollbacks` property MUST be a JSON array of [action][] results.

Each action result MUST declare the following properties:

* a `activity` property
* a `status` property
* a `start` property
* a `end` property
* a `duration` property
* a `output` property

The `activity` property MUST be a JSON object, a raw copy of the executed
[action][].

The `status` property MUST be a JSON string, one of `"succeeded"` or `"failed"`.

The `start` property MUST be a JSON string formatted as per [RFC 3339](rfc3339)
in UTC timezone.

The `end` property MUST be a JSON string formatted as per [RFC 3339](rfc3339) in
UTC timezone.

The `duration` MUST be a JSON number of difference between the `end` datetime
and the `start` datetime.

The `output` MUST be a JSON string or `null`.

In addition, the activity result MAY contain an additional property:

* a `exception` property

This property is set when the action failed in an unforeseeable way and MUST be
a JSON array or JSON string of the error trace. 

Rollbacks MUST NOT to be applied when the experiment status is `"interrupted"`.