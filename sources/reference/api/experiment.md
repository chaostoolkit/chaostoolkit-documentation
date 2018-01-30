# An Open API for Chaos Engineering Experiments

!!! info
    The current specification has not reached its 1.0.0 stable version yet. Make
    sure to [join the discussion][join] to provide any feedback you might have.

[join]: https://join.chaostoolkit.org/

[exp]: #experiment
[hypo]: #steady-state-hypothesis
[meth]: #method
[pb]: #probe
[action]: #action
[secrets]: #secrets
[conf]: #configuration

## Introduction

The purpose of this specification is to formalize the elements of a Chaos
Engineering experiment and offer a way to federate the community around a
common syntax and semantic.

As a fairly recent field, Chaos Engineering is a dynamic and its foundations
are still emerging. However, it appears certain concepts are settling down
enough to start agreeing on a shared understanding.

This specification is not prescriptive and does not aim at forcing the
community into one direction, rather it strives at providing a common
vocabulary that new practicionners can easily make sense of.

It is necessary to appreciate that this document does not specify what tools,
such as the Chaos Monkey or similar, should look like. Instead, this document
specifies how Chaos Engineering Experiment could be described, shared and
conducted collaboratively.

## Conventions Used in This Document

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [RFC 2119][rfc2119].

[rfc2119]: https://tools.ietf.org/html/rfc2119

The terms "JSON", "JSON text", "JSON value", "member", "element", "object",
"array", "number", "string", "boolean", "true", "false", and "null" in this
document are to be interpreted as defined in [RFC 7159][rfc7159].

[rfc7159]: https://tools.ietf.org/html/rfc7159

## Chaos Engineering Elements

### Overview

An Experiment is one possible description of the
[principles of the Chaos Engineering][principles]. The intention of such a
description is to provide shared understanding around a hypothesis on how
to discover system's behavior under certain conditions.

An [Experiment][exp] declares a steady [state hypothesis][hypo], alongside
[probes][pb] to validate this steady state is met, and a [method][meth] as a
sequence [actions][action] and [probes][pb], to interact and query the system
respectively.

By using a variety of [probes][pb], experiments should gather information to
sense behaviors in the system, potentially leading to systemic patterns that can
be stabilized.

[principles]: http://principlesofchaos.org/

### Experiment

A Chaos Engineering experiment, or simply an experiment, describes both the
elements and the order in which they should be applied.

An experiment is a JSON object.

An experiment MUST declare:

* a `version` property
* a `title` property
* a `description` property
* a `steady-state-hypothesis` property
* a `method` property

The `version` property MUST be `"0.1.0"`.

The experiment's `title` and `description` are meant for humans and therefore
should be as descriptive as possible to clarify the experiment's rationale.

Title and description are JSON strings with no maximum length.

An experiment SHOULD also declare:

* a `rollbacks` property

An experiment MAY finally declare:

* a `tags` property
* a `secrets` property

Tags provide a way of categorizing experiments. It is a sequence of JSON
strings.

### Steady State Hypothesis

The Steady State Hypothesis element describes what normal looks like in your
system before the Method element is applied. If the steady state is not met,
the Method element is not applied and the experiment MUST bail out.

The Steady State Hypothesis element is a JSON object.

Steady State Hypothesis element MUST declare:

* a `title` property
* a `probes` property

The `title` is meant for humans and therefore should clarify the rationale for
this hypothesis.

Each [Probe][pb] MUST define a `tolerance` property that acting as a gate
mechanism for the experiment to carry on or bail. Any [Probe][pb] that does not
fall into the [tolerance][] zone MUST fail the experiment.

[tolerance]: #steady-state-probe-tolerance

#### Steady State Probe Tolerance

[Probes][pb] of the Steady State Hypothesis MUST declare an additional property
named `tolerance`.

The `tolerance` property's value MUST be one of:

* a scalar: JSON string, number (an integer), boolean
* a sequence of two scalars defining a lower and upper bounds
* a Probe object

In the case of a scalar or the sequence, the tolerance validation MUST be
strict. The value returned by the [Probe][pb] MUST be checked against the
scalar value. The experiment MUST bail when both fail to match.

When the `tolerance` is a sequence of two scalars, the returned value from
the [Probe][pb] MUST fall within the boundaries they form.

In the case of a [Probe][pb] object, the tolerance validation is left
undefined as it is controlled by the [Probe][pb] itself. However, it is
RECOMMENDED that the `tolerance` [Probe][pb] acts strictly in order to improve
the readability of the experiment's results.

Some examples of `tolerance` properties.

A boolean tolerance:
```json
"tolerance": true
```

A integer tolerance:
```json
"tolerance": 8
```

A string tolerance:
```json
"tolerance": "OK"
```

A sequence tolerance:
```json
"tolerance": [4, 9]
```

A [Probe][pb] tolerance:
```json
"tolerance": {
    "type": "probe",
    "name": "should-exist",
    "provider": {
        "type": "python",
        "module": "os.path",
        "func": "exists",
        "arguments": {
            "path": "some/file"
        }
    }
}
```

### Method

The Method describes the sequence of [Probe][pb] and [Action][action] elements
to apply. The Method is declared under `method` property at the top-level of the
experiment.

The `method` MUST have at least one element but this can be either a [Probe][pb]
or an [Action][action].

The elements MUST be applied in the order they are declared.

### Probe

A Probe collects information from the system during the experiment.

A Probe is a JSON object. A Probe is declared fully or reference another Probe
through the `ref` property.

When declared fully, a Probe MUST declare:

* a `type` property
* a `name` property
* a `provider` property

The `type` property MUST be the JSON string `"probe"`. 

The `name` property is a free-form JSON string that MAY be considered as an
identifier withing the experiment.

It MAY also declare:

* a `secret` property
* a `configuration` property
* a `background` property

The `secret` property MUST be a JSON string referencing an identifier declared
in the top-level `secrets` [property][secrets]. It is assumed that when not
declared, the Probe requires no secrets.

The `configuration` property MUST be a JSON string referencing an identifier
declared in the top-level `configuration` [property][conf]. It is assumed that
when not declared, the Probe requires no configuration.

The `background` property MUST be a JSON boolean value either `true` or `false`.
It is assumed that, when that property is not declared, it is set to `false`.
When that property is set to `true` it indicates the Probe MUST not block
and the next Action or Probe should immediatly be applied.

When a Probe references another Probe in the Experiment, the Probe MUST
declare a single property called `ref`.

The `ref` property MUST be a JSON string which MUST be the name of a declared
Probe.

### Action

An Action performs an operation against the system.

An Action collects information from the system during the experiment.

An Action is a JSON object. An Action is declared fully or reference another
Action through the `ref` property.

When declared fully, a Action MUST declare:

* a `type` property
* a `name` property
* a `provider` property

The `type` property MUST be the JSON string `"action"`. 

The `name` property is a free-form JSON string that MAY be considered as an
identifier withing the experiment.

It MAY also declare:

* a `secret` property
* a `configuration` property
* a `background` property
* a `pauses` property

The `secret` property MUST be a JSON string referencing an identifier declared
in the top-level `secrets` [property][secrets]. It is assumed that when not
declared, the Action requires no secrets.

The `configuration` property MUST be a JSON string referencing an identifier
declared in the top-level `configuration` [property][conf]. It is assumed that
when not declared, the Action requires no configuration.

The `background` property MUST be a JSON boolean value either `true` or `false`.
It is assumed that, when that property is not declared, it is set to `false`.
When that property is set to `true` it indicates the Action MUST not block
and the next Action or Probe should immediatly be applied.

The `pauses` property MUST be a JSON object which MAY have one or the two
following properties:

* `before`
* `after`

In both cases, the value MUST be JSON number indicating the number of seconds to
wait before continuining. The `before` pause MUST be performed before the Action
while the `after` MUST be performed afterwards.

When a Action references another Action in the Experiment, the Action MUST
declare a single property called `ref`.

The `ref` property MUST be a JSON string which MUST be the name of a declared
Action.

### Action or Probe Provider

A provider MUST be a JSON object which MUST declare a `type` property that
decides the other expected properties.

The `type` property MUST be one of `"python"`, `"http"` or `"process"`.

#### Python Provider

A Python Provider declares a Python function to be applied.

A Python Provider MUST declare the following:

* a `module` property
* a `func` property

It SHOULD also declare an `arguments` property when the function expects them.

The `module` property is the fully qualified module exposing the function. It
MUST be a JSON string.

The `func` property is the name of the function to apply. It MUST be a JSON
string.

When provided, the `arguments` property MUST be a JSON object which
properties are the names of the [function's arguments][farg]. When a function's
signature has [default values][fdef] for some of its arguments, those MAY be
omitted from the `arguments` object. In that case, those default values will be
used.

Argument values MUST be valid JSON entities.

[farg]: https://docs.python.org/3/glossary.html#term-argument
[fdef]: https://docs.python.org/3/reference/compound_stmts.html#function-definitions

#### HTTP Provider

A HTTP Provider declares a URL to be called.

A HTTP Provider MUST declare the following:

* a `url` property

The `url` property MUST be a JSON string representing a URL as per
[RFC 3986][rfc3986].

[rfc3986]: https://tools.ietf.org/html/rfc3986

In addition, the `provider` object MAY declare any of the followings:

* a `method` property
* a `headers` property
* a `expected_status` property
* a `arguments` property
* a `timeout` property

[rfc2616]: https://www.w3.org/Protocols/rfc2616/

The `method` property MUST be a JSON string, such as `"POST"`, as per
[RFC 2616][rfc2616]. It defaults to `"GET"`.

The `headers` property MUST be a JSON object which properties are header names
and values are header values, as per [RFC 2616][rfc2616].

The `expected_status` property MUST be a JSON number as per [RFC 2616][rfc2616]
definining the expected HTTP response status for the Probe or Action to be
considered failed or successful. It defaults to `200`.

When provided, the `arguments` property MUST be a JSON object which
properties are parameters of the HTTP request.

When `method` is `"GET"`, the `arguments` are mapped as a query-string of the
URL. Otherwise, the `arguments` are passed as the request body's data and the
encoding depends on the `"Content-Type"` provided in the `headers` object.

The `timeout` property MUST be a JSON number specifying how long the request
should take to complete.

#### Process Provider

A Process Provider declares a process to be called.

A Process Provider MUST declare the following:

* a `path` property

The `path` property MUST be a JSON string of a path to an executable.

In addition, the `provider` object MAY declare any of the followings:

* a `arguments` property
* a `timeout` property

The `arguments` property MUST be a JSON object which defines the process
arguments. The properties are the names and each property's value is the
the argument's value. An argument that does not expect a value MUST set that
value to the empty string `""`.

The `timeout` property MUST be a JSON number specifying how long the process
should take to complete.

### Rollbacks

Rollbacks declare the sequence of actions that attempt to put the system back
to its initial state.

The experiment MAY declare a single `rollbacks` property which is a JSON array
consisting of [Actions][action].

A failed rollback MUST not bail the sequence of rollbacks.

### Secrets

Secrets declare values that need to be passed on to [Actions][action] or
[Probes][pb] in a secure manner.

The `secrets` property MUST be a JSON object. Its properties are identifiers
referenced by [Actions][action] and [Probes][pb].

The value of each identifier is a JSON object which properties are the secrets
keys and the properties values are the secrets values.

Referenced secrets MUST be injected into probes and actions when they are
applied. Probes and actions MUST NOT modify the secrets.

Secrets MUST be passed a mapping of keys and values to probes and actions.

An example of a `secrets` element at the top-level:

```json
{
    "secrets": {
        "kubernetes": {
            "token": "XYZ"
        }
    }
}
```

This can then referenced from probes or actions:

```json
{
    "type": "probe",
    "secrets": "kubernetes"
}
```

#### Inline Secrets

Secrets MAY be inlined in the [Experiment][exp] directly.

#### Environment Secrets

Secrets MAY be retrieved from the environment. In that case, they must be
declared as a JSON object with a `type` property set to `"env"`. The
environment variable MUST be declared in the `key` property as a JSON string.

```json
{
    "secrets": {
        "kubernetes": {
            "token": {
                "type": "env",
                "key": "KUBERNETES_TOKEN"
            }
        }
    }
}
```

#### Vault Secrets

Secrets MAY be retrieved from a [HashiCorp vault instance][vault]. In that case,
they must be declared as a JSON object with a `type` property set to `"vault"`.
The path to the key MUST be declared in the `key` property as a JSON
string.

[vault]: https://www.vaultproject.io/

```json
{
    "secrets": {
        "myapp": {
            "token": {
                "type": "vault",
                "key": "secrets/something"
            }
        }
    }
}
```

### Configuration

Configuration is meant to provide runtime values to [actions][action] and
[probes][pb].

The `configuration` element MUST be a JSON object. The value of each property
MUST be a JSON string or object which properties are considered the
configuration lookup. Configuration must be passed to all Probes and actions
requring it. Probes and actions MUST NOT modify the configuration.

Configurations MUST be passed a mapping of keys and values to probes and
actions.

An example of a `configuration` element at the top-level:

```json
{
    "configuration": {
        "some_service": "http://127.0.0.1:8080",
        "vault_addr": {
            "type": "env",
            "key": "VAULT_ADDR"
        }
    }
}
```

#### Inline Configurations

Configurations MAY be inlined in the [Experiment][exp] directly.

#### Environment Configurations

Configurations MAY be retrieved from the environment. In that case, they must be
declared as a JSON object with a `type` property set to `"env"`. The
environment variable MUST be declared in the `key` property as a JSON string.

```json
{
    "configuration": {
        "vault_address": {
            "type": "env",
            "key": "VAULT_ADDR"
        }
    }
}
```

### Variable Substitution

Probes and Actions argument values MAY be dynamically resolved at runtime. 

Dynamic values MUST follow the syntax `${name}` where `name` is an identifier
declared in either the Configuration or Secrets sections. When `name` is
declared in both sections, the Configuration section MUST take precedence.

Dynamic values MUST be substituted before being passed to Probes or Actions.

Other values, such as the HTTP Probe url, MAY be sustituted as well.

## Examples

The following examples MUST NOT be considered normatives.

### Minimal Experiment

Here is an example of the most minimal experiment:

```json
{
    "version": "0.1.0",
    "title": "Moving a file from under our feet is forgivable",
    "description": "Our application should re-create a file that was removed",
    "steady-state-hypothesis": {
        "title": "The file must be around first",
        "probes": [
            {
                "type": "python",
                "name": "file-must-exist",
                "tolerance": true,
                "provider": {
                    "module": "os.path",
                    "func": "exists",
                    "arguments": {
                        "path": "some/file"
                    }
                }
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "file-be-gone",
            "provider": {
                "module": "os.path",
                "func": "remove",
                "arguments": {
                    "path": "some/file"
                }
            },
            "pauses": {
                "after": 5
            }
        },
        {
            "ref": "file-must-exist"
        }
    ]
}
```