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
vocabulary that new practitioners can easily make sense of.

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

### Other formats

While this specification uses JSON to define its elements, implementations may
allow loading from other formats, such as [YAML][yaml]. As long as the output
of such format respects the specification herein.

[yaml]: http://yaml.org/spec/

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
* a `method` property

The `version` property MUST be `"0.1.0"`.

The experiment's `title` and `description` are meant for humans and therefore
should be as descriptive as possible to clarify the experiment's rationale.

Title and description are JSON strings with no maximum length.

An experiment SHOULD also declare:

* a `steady-state-hypothesis` property
* a `rollbacks` property

An experiment MAY finally declare:

* a `tags` property
* a `secrets` property
* an `extension` property
* a `contributions` property
* a `controls` property

Tags provide a way of categorizing experiments. It is a sequence of JSON
strings.

[Extensions][ext] define opaque payloads for vendors to carry valuable
information.

[ext]: #extensions

[Contribution][contrib] describes valuable properties of the target system,
such as "reliability" or "durability", that an experiment contribute to. This
information can be aggregated together with other experiments' contributions to
better appreciate where the focus is put and where it is not.

[contrib]: #contributions

[Controls][controls] describe out-of-band capabilities applied during the
experiment's execution.

[controls]: #controls

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

Steady State Hypothesis element MAY declare:

* a `controls` property

[Controls][controls] describe out-of-band capabilities applied during the
experiment's execution.

[tolerance]: #steady-state-probe-tolerance

#### Steady State Probe Tolerance

[Probes][pb] of the Steady State Hypothesis MUST declare an additional property
named `tolerance`.

The `tolerance` property's value MUST be one of:

* a scalar: JSON string, number (an integer), boolean
* a sequence of scalars: JSON string, number, boolean
* an object

In the case of a scalar or the sequence, the tolerance validation MUST be
strict. The value returned by the [Probe][pb] MUST be checked against the
scalar value. The experiment MUST bail when both fail to match.

When the `tolerance` is a sequence. If it has only two values, those two values
represent a lower and upper bound within which the [Probe][pb] returned value
must fall (inclusive).

When the sequence has more than two elements, the [Probe][pb] returned value
must be contained in that sequence.

When the `tolerance` is an object, it MUST have a `type` property which MUST
be one of the followings: `"probe"`, `"regex"`, `"jsonpath"` or `"range"`.

When the `type` property is `"probe"`, the object MUST be a [Probe][pb] that is
applied. The probe should take two arguments, `value` and `secrets` where
the value is the [Probe][pb] returned value and secrets a [Secret][secrets]
object or `null`. Its returned status MUST be successful for the `tolerance` to
be considered valid.

When the `type` property is `"regex"`, the object MUST have a `pattern`
property which MUST be a valid regular expression. The `tolerance` succeeds if
the [Probe][pb] returned value is matched against the pattern.

When the `type` property is `"jsonpath"`, the object MUST have a `path`
property which MUST be a valid [JSON Path][jp]. In addition, the object MAY
have a `expect` property which is used to compare each value matched by the JSON
Path to that value. The `expect` property value MUST be a scalar. When the
`expect` property is not present, the `tolerance` succeeds if the JSON Path
matched at least one item.

When the `type` property is `"range"`, the object MUST have a `range` 
property whuch MUST be a sequence of length two. The first entry of the
sequence MUST be the lower bound and the second entry MUST be the upper bound.
Both entries MUST be JSON numbers.

[jp]: http://goessner.net/articles/JsonPath/

In addition, when the [Probe][pb] returned value is an object with a ̀`status`
property, the tested value is the value of that property.

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

A sequence tolerance with lower and upper bounds:
```json
"tolerance": [4, 9]
```

A sequence tolerance, the value must be contained in that sequence:
```json
"tolerance": [4, 9, 78]
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

A regex tolerance:

```json
"tolerance": {
    "type": "regex",
    "pattern": "[0-9]{3}"
}
```

A jsonpath tolerance:

```json
"tolerance": {
    "type": "jsonpath",
    "path": "foo[*].baz"
}
```

A jsonpath tolerance with an expected value to match:

```json
"tolerance": {
    "type": "jsonpath",
    "path": "foo[*].baz",
    "expect": 4
}
```

Two range tolerances:

```json
"tolerance": {
    "type": "range",
    "range": [4, 8]
}
```

```json
"tolerance": {
    "type": "range",
    "range": [4.6, 8.9]
}
```


### Contributions

Contributions describe the valuable system properties an experiment targets as
well as how much they contributes to it. Those properties usually refer to
aspects stakeholders care about. Aggregated they offer a powerful metric about
the effort and focus on building confidence across the system.

Contributions are declared under the top-level `contributions` property as an
object. Properties of that object MUST be JSON strings representing the name
of a contribution. The values MUST be the weight of a given contribution and
MUST be one of `"high"`, `"medium"`, `"low"` or `"none"`. The `"none"` value
is not the same as a missing contribution from the `contributions` object.
That value marks explicitly that a given contribution is not addressed by an
experiment. A missing contribution means impact via this experiment is unknown
for this contribution.

Here is a contribution example:

```json
"contributions": {  
    "reliability": "high",
    "security": "none",
    "scalability": "medium"
}
```

This sample tells us that the experiment contributes mainly to exploring
reliability of the system and moderately to its scability. However, it is
explicit here this experiment does not address security.

On the other hand:

```json
"contributions": {  
    "reliability": "high",
    "scalability": "medium"
}
```

This tells us the same about reliability and scalability but we can't presume
anything about security.

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
identifier within the experiment.

It MAY also declare:

* a `secret` property
* a `configuration` property
* a `background` property
* a `controls` property

The `secret` property MUST be a JSON string referencing an identifier declared
in the top-level `secrets` [property][secrets]. It is assumed that when not
declared, the Probe requires no secrets.

The `configuration` property MUST be a JSON string referencing an identifier
declared in the top-level `configuration` [property][conf]. It is assumed that
when not declared, the Probe requires no configuration.

The `background` property MUST be a JSON boolean value either `true` or `false`.
It is assumed that, when that property is not declared, it is set to `false`.
When that property is set to `true` it indicates the Probe MUST not block
and the next Action or Probe should immediately be applied.

When a Probe references another Probe in the Experiment, the Probe MUST
declare a single property called `ref`.

The `ref` property MUST be a JSON string which MUST be the name of a declared
Probe.

[Controls][controls] describe out-of-band capabilities applied during the
experiment's execution.

### Action

An Action performs an operation against the system.

An Action collects information from the system during the experiment.

An Action is a JSON object. An Action is declared fully or reference another
Action through the `ref` property.

When declared fully, a Action MUST declare:

* a `type` property
* a `name` property
* a `provider` property
* a `controls` property

The `type` property MUST be the JSON string `"action"`. 

The `name` property is a free-form JSON string that MAY be considered as an
identifier within the experiment.

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
and the next Action or Probe should immediately be applied.

The `pauses` property MUST be a JSON object which MAY have one or the two
following properties:

* `before`
* `after`

In both cases, the value MUST be JSON number indicating the number of seconds to
wait before continuing. The `before` pause MUST be performed before the Action
while the `after` MUST be performed afterwards.

When a Action references another Action in the Experiment, the Action MUST
declare a single property called `ref`.

The `ref` property MUST be a JSON string which MUST be the name of a declared
Action.

[Controls][controls] describe out-of-band capabilities applied during the
experiment's execution.

### Action or Probe Provider

A provider MUST be a JSON object which MUST declare a `type` property that
decides the other expected properties.

The `type` property MUST be one of `"python"`, `"http"` or `"process"`.

!!! info
    This specification only mentions those three providers but it could grow
    to [support more][otherproviders], such as `"go"`, `"rust"` or `"grpc"`...

[otherproviders]: https://github.com/chaostoolkit/chaostoolkit-lib/issues/38

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
[RFC 7231][rfc7231]. It defaults to `"GET"`.

The `headers` property MUST be a JSON object which properties are header names
and values are header values, as per [RFC 7231][rfc7231].

When provided, the `arguments` property MUST be a JSON object which
properties are parameters of the HTTP request.

When `method` is `"GET"`, the `arguments` are mapped as a query-string of the
URL. Otherwise, the `arguments` are passed as the request body's data and the
encoding depends on the `"Content-Type"` provided in the `headers` object.

The `timeout` property MUST be either a JSON number specifying how long the
request should take to complete. Or a JSON array that MUST made of two JSON
numbers, the first one indicating the connection timeout, the second the
request timeout to respond.

The HTTP provider MUST return an object with the following properties:

* `status` which MUST be a valid HTTP returned code as defined in
  [RFC 7231][rfc7231]
* `headers` which MUST be an object
* `body` which MUST be a string

[rfc7231]: https://tools.ietf.org/html/rfc7231

#### Process Provider

A Process Provider declares a process to be called.

A Process Provider MUST declare the following:

* a `path` property

The `path` property MUST be a JSON string of a path to an executable.

In addition, the `provider` object MAY declare any of the followings:

* a `arguments` property
* a `timeout` property

The `arguments` property MUST be a JSON array which defines the process
arguments. Those arguments are passed in order to the process arguments.

The `timeout` property MUST be a JSON number specifying how long the process
should take to complete.

The Process provider MUST return an object with the following properties:

* `status` which MUST be a scalar of the process return code
* `stdout` which MUST be bytes sequence encoded with the `UTF-8` encoding
  representing the stdout payload of the process
* `stderr` which MUST be bytes sequence encoded with the `UTF-8` encoding
  representing the stderr payload of the process

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
The path to the key MUST be declared in the `path` property as a JSON
string.

[vault]: https://www.vaultproject.io/

```json
{
    "secrets": {
        "myapp": {
            "token": {
                "type": "vault",
                "path": "secrets/something"
            }
        }
    }
}
```

When only the `path` property is set, the whole secrets payload at the given
path MUST be set to the Chaos Toolkit secret key.

A `key` property MAY be set to select a specific value from the Vault secret
payload.

Vault authentication MUST at least support:

* [token][vaulttoken] based authentication
  The token MUST be provided in the Configuration section via the
  `"vault_token"` property
* [AppRole][approle] authentication
  The role-id and secret-id MUST be provided in the Configuration section vi
  the `"vault_role_id"` and `"vault_role_secret"` properties

The Vault [KV secrets version][kvversion] MAY be provided via the
`"vault_kv_version"` Configuration key. If not provided, it MUST default to
`"2"`.

[vaulttoken]: https://www.vaultproject.io/api/auth/token/index.html
[approle]: https://www.vaultproject.io/api/auth/approle/index.html
[kvversion]: https://www.vaultproject.io/api/secret/kv/index.html

Examples:

Vault secret at path `secret/something`:

```json
{
    "foo": "bar",
    "baz": "hello"
}
```

Then in your Chaos Toolkit experiment:

```json
{
    "secrets": {
        "myapp": {
            "token": {
                "type": "vault",
                "path": "secrets/something"
            }
        }
    }
}
```

means the secrets will become:

```
"myapp": {
    "foo": "bar",
    "baz": "hello"
}
```

However:

```json
{
    "secrets": {
        "myapp": {
            "token": {
                "type": "vault",
                "path": "secrets/something",
                "key": "foo"
            }
        }
    }
}
```

means the secrets will become:

```
"myapp": "bar"
```

### Configuration

Configuration is meant to provide runtime values to [actions][action] and
[probes][pb].

The `configuration` element MUST be a JSON object. The value of each property
MUST be a JSON string or object which properties are considered the
configuration lookup. Configuration must be passed to all Probes and actions
requiring it. Probes and actions MUST NOT modify the configuration.

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

The `default` key is OPTIONAL and MAY be used when the environment variable
can be undefined and fallback to a default value for the experiment.

```json
{
    "configuration": {
        "vault_address": {
            "type": "env",
            "key": "VAULT_ADDR",
            "default": "https://127.0.0.1:8200"
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

Other values, such as the HTTP Probe url, MAY be substituted as well.

### Controls

Controls describe out-of-band capabilities applied when the experiment is
executed. Controls are used to declare operations that should be carried by
external tools.

Controls MAY be declared at each of the following levels:

* experiment
* steady-state-hypothesis
* activity

Controls MUST be applied before and after each of those levels. Schematically,
this looks like this:

```
apply experiment control before experiment starts
start experiment
    apply steady state control before steady-state probes are started
        start steady-state processing
            apply activity control before each probe is applied
            run each probe
            apply activity control after each probe is applied
    apply steady state control after steady-state probes have completed
    apply steady state control before method activities are started
        start method processing
            apply activity control before each activity is applied
            run each activity
            apply activity control after each activity is applied
    apply steady state control after method activities have completed
    apply steady state control before rollback activities are started
        start rollback processing
            apply activity control before each activity is applied
            run each activity
            apply activity control after each activity is applied
    apply steady state control after rollback activities have completed
apply experiment control after experiment completes
```

Controls MAY be omitted anywhere and MUST NOT be applied at a level they
are not declared.

Controls MUST NOT fail the experiment's execution due to unforeseen conditions.

Controls are declared with the `controls` property which is set to a JSON
array.

An item of that array MUST be a control, which is a JSON object which MUST
have the following properties:

* a `name` property which MUST be a JSON string
* a `provider` property MUST be a JSON object

The `provider` object indicates which implementation of the control to use.
It MUST declare the following properties:

* a `type` JSON string which MUST be `"python"`
* a `module` JSON string when the `type` property is `"python"`. It MUST be a
  a Python module dotted path implementing the control interface

A control object MAY also declare the following property:

* a `scope` property MUST be a JSON string
* `automatic`, a JSON boolean which MUST be `true` by default (when omitted)

The `scope` value MUST be one of `"before"` or `"after"`. When the `scope`
property is omitted, the control MUST be applied before and after. When the
`scope` property is set, the control MUST be applied only on that scope.

When the `automatic` property is set to `false`, it MUST be understood that
the control cannot be applied anywhere but where it is declared.

Examples of Controls:

Just a generic declaration of a control at the top-level of the experiment:

```json
"controls": [
    {
        "name": "tracing",
        "provider": {
            "type": "python",
            "module": "chaostracing.control"
        }
    }
]
```

Another control by applied only as post-control:

```json
"controls": [
    {
        "name": "tracing",
        "scope": "post",
        "provider": {
            "type": "python",
            "module": "chaostracing.control"
        }
    }
]
```

Finally, a top-level level control not applied anywhere else down the tree:

```json
"controls": [
    {
        "name": "tracing",
        "automatic": false,
        "provider": {
            "type": "python",
            "module": "chaostracing.control"
        }
    }
]
```

### Extensions

An Experiment MAY declare an `extensions` property which MUST be an array
of objects. Each object MUST declare a non-empty `name` property.

Extensions are used in two scenarios:

* future core features that need to be ironed out by the community first
* vendor specific payload

In both cases, their actual usage is runtime dependent, this specification
does not declare any meaning to an extension.

Below is an example of an Extension:

```json
{
    "extensions": [{
        "name": "vendorX",
        "data": "..."
    }]
}
```

## Examples

The following examples MUST NOT be considered normative.

### Minimal Experiment

Here is an example of the most minimal experiment:

```json
{
    "version": "1.0.0",
    "title": "Moving a file from under our feet is forgivable",
    "description": "Our application should re-create a file that was removed",
    "contributions": {
        "reliability": "high",
        "availability": "high"
    },
    "steady-state-hypothesis": {
        "title": "The file must be around first",
        "probes": [
            {
                "type": "probe",
                "name": "file-must-exist",
                "tolerance": true,
                "provider": {
                    "type": "python",
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
                "type": "python",
                "module": "os",
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

For reference, here is the YAML equivalent (which is not official but respects
the specification herein):

```yaml
---
version: 1.0.0
title: Moving a file from under our feet is forgivable
description: Our application should re-create a file that was removed
contributions:
  reliability: high
  availability: high
steady-state-hypothesis:
  title: The file must be around first
  probes:
  - type: probe
    name: file-must-exist
    tolerance: true
    provider:
      type: python
      module: os.path
      func: exists
      arguments:
        path: some/file
method:
- type: action
  name: file-be-gone
  provider:
    type: python
    module: os
    func: remove
    arguments:
      path: some/file
  pauses:
    after: 5
- ref: file-must-exist
```

### More Complex Experiment

Below is an example of a fully featured experiment that uses various extensions
to perform actions, probing and steady-state hypothesis validation.

```json
{
    "version": "1.0.0",
    "title": "Are our users impacted by the loss of a function?",
    "description": "While users query the Astre function, they should not be impacted if one instance goes down.",
    "contributions": {
        "reliability": "high",
        "availability": "high",
        "performance": "medium",
        "security": "none"
    },
    "tags": [
        "kubernetes",
        "openfaas",
        "cloudnative"
    ],
    "configuration": {
        "prometheus_base_url": "http://demo.foo.bar"
    },
    "secrets": {
        "global": {
            "auth": "Basic XYZ"
        }
    },
    "controls": [
        {
            "name": "tracing",
            "provider": {
                "type": "python",
                "module": "chaostracing.control"
            }
        }
    ],
    "steady-state-hypothesis": {
        "title": "Function is available",
        "probes": [
            {
                "type": "probe",
                "name": "function-must-exist",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "secrets": ["faas"],
                    "url": "http://demo.foo.bar/system/function/astre",
                    "headers": {
                        "Authorization": "${auth}"
                    }
                }
            },
            {
                "type": "probe",
                "name": "function-must-respond",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "timeout": [3, 5],
                    "secrets": ["global"],
                    "url": "http://demo.foo.bar/function/astre",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "${auth}"
                    },
                    "arguments": {
                        "city": "Paris"
                    }
                }
            }
        ]
    },
    "method": [
        {
            "type": "action",
            "name": "simulate-user-traffic",
            "background": true,
            "provider": {
                "type": "process",
                "path": "vegeta",
                "arguments": "-cpus 2 attack -targets=data/scenario.txt -workers=2 -connections=1 -rate=3 -timeout=3s -duration=30s -output=result.bin"
            }
        },
        {
            "type": "action",
            "name": "terminate-one-function",
            "provider": {
                "type": "python",
                "module": "chaosk8s.pod.actions",
                "func": "terminate_pods",
                "arguments": {
                    "ns": "openfaas-fn",
                    "label_selector": "faas_function=astre",
                    "rand": true
                }
            },
            "pauses": {
                "before": 5
            }
        },
        {
            "type": "probe",
            "name": "fetch-openfaas-gateway-logs",
            "provider": {
                "type": "python",
                "module": "chaosk8s.pod.probes",
                "func": "read_pod_logs",
                "arguments": {
                    "label_selector": "app=gateway",
                    "last": "35s",
                    "ns": "openfaas"
                }
            }
        },
        {
            "type": "probe",
            "name": "query-total-function-invocation",
            "provider": {
                "type": "python",
                "module": "chaosprometheus.probes",
                "func": "query_interval",
                "secrets": ["global"],
                "arguments": {
                    "query": "gateway_function_invocation_total{function_name='astre'}",
                    "start": "1 minute ago",
                    "end": "now",
                    "step": 1
                }
            }
        }
    ],
    "rollbacks": []
}
```

The equivalent YAML serialization:

```yaml
---
version: 1.0.0
title: Are our users impacted by the loss of a function?
description: While users query the Astre function, they should not be impacted if
  one instance goes down.
contributions:
  reliability: high
  availability: high
  performance: medium
  security: none
tags:
- kubernetes
- openfaas
- cloudnative
configuration:
  prometheus_base_url: http://demo.foo.bar
secrets:
  global:
    auth: Basic XYZ
controls:
- name: tracing
  provider:
    type: python
    module: chaostracing.control
steady-state-hypothesis:
  title: Function is available
  probes:
  - type: probe
    name: function-must-exist
    tolerance: 200
    provider:
      type: http
      secrets:
      - faas
      url: http://demo.foo.bar/system/function/astre
      headers:
        Authorization: "${auth}"
  - type: probe
    name: function-must-respond
    tolerance: 200
    provider:
      type: http
      timeout:
      - 3
      - 5
      secrets:
      - global
      url: http://demo.foo.bar/function/astre
      method: POST
      headers:
        Content-Type: application/json
        Authorization: "${auth}"
      arguments:
        city: Paris
method:
- type: action
  name: simulate-user-traffic
  background: true
  provider:
    type: process
    path: vegeta
    arguments: "-cpus 2 attack -targets=data/scenario.txt -workers=2 -connections=1
      -rate=3 -timeout=3s -duration=30s -output=result.bin"
- type: action
  name: terminate-one-function
  provider:
    type: python
    module: chaosk8s.pod.actions
    func: terminate_pods
    arguments:
      ns: openfaas-fn
      label_selector: faas_function=astre
      rand: true
  pauses:
    before: 5
- type: probe
  name: fetch-openfaas-gateway-logs
  provider:
    type: python
    module: chaosk8s.pod.probes
    func: read_pod_logs
    arguments:
      label_selector: app=gateway
      last: 35s
      ns: openfaas
- type: probe
  name: query-total-function-invocation
  provider:
    type: python
    module: chaosprometheus.probes
    func: query_interval
    secrets:
    - global
    arguments:
      query: gateway_function_invocation_total{function_name='astre'}
      start: 1 minute ago
      end: now
      step: 1
rollbacks: []
```
