# Learn all about Steady-State Hypothesis Tolerances

A Chaos Engineering experiment starts and ends with a steady-state hypothesis.

The objective is initially to act as a validation gateway whereby, if the
steady-state is not met before we execute the method, then the experiment
bails out. What can you learn from an unknown state already?

Then, once the method has been applied, the goal is understand if the system
coped with the turbulence or if it deviated, implying a weakness may have
been uncovered.

To achieve this, the Chaos Toolkit experiment expects you use probes to query
your system's state during the steady-state hypothesis. The validation of the
probes' output is performed by what we call tolerances.

## Let's get started with a basic example

Let's take the simple experimant below:

```json
{
  "version": "1.0.0",
  "title": "Our default language is English",
  "description": "We find the expected English language in the file",
  "steady-state-hypothesis": {
    "title": "Our hypothesis is that lang file is in English",
    "probes": [
      {
        "type": "probe",
        "name": "lookup-lang-file",
        "tolerance": true,
        "provider": {
          "type": "python",
          "module": "os.path",
          "func": "exists",
          "arguments": {
              "path": "default.locale.txt"
          }
        }
      },
      {
        "type": "probe",
        "name": "lookup-text-in-lang-file",
        "tolerance": 0,
        "provider": {
          "type": "process",
          "path": "grep",
          "arguments": "welcome=hello default.locale.txt"
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "switch-language-to-french",
      "provider": {
        "type": "process",
        "path": "sed",
        "arguments": "-i s/hello/bonjour/ default.locale.txt"
      }
    }
  ],
  "rollbacks": [
    {
        "type": "action",
        "name": "switch-language-back-to-english",
        "provider": {
          "type": "process",
          "path": "sed",
          "arguments": "-i s/bonjour/hello/ default.locale.txt"
        }
      }
  ]
}
```

This experiment looks for the welcome message in the default locale file and
expected `"hello"`.

Here is an example of it running:

```
$  chaos run experiment.json 
[2019-06-25 21:37:59 INFO] Validating the experiment's syntax
[2019-06-25 21:37:59 INFO] Experiment looks valid
[2019-06-25 21:37:59 INFO] Running experiment: Our default language is English
[2019-06-25 21:37:59 INFO] Steady state hypothesis: Our hypothesis is that lang file is in English
[2019-06-25 21:37:59 INFO] Probe: lookup-lang-file
[2019-06-25 21:37:59 INFO] Probe: lookup-text-in-lang-file
[2019-06-25 21:37:59 INFO] Steady state hypothesis is met!
[2019-06-25 21:37:59 INFO] Action: switch-language-to-french
[2019-06-25 21:37:59 INFO] Steady state hypothesis: Our hypothesis is that lang file is in English
[2019-06-25 21:37:59 INFO] Probe: lookup-lang-file
[2019-06-25 21:37:59 INFO] Probe: lookup-text-in-lang-file
[2019-06-25 21:37:59 INFO] Steady state hypothesis is met!
[2019-06-25 21:37:59 INFO] Let's rollback...
[2019-06-25 21:37:59 INFO] Rollback: switch-language-back-to-english
[2019-06-25 21:37:59 INFO] Action: switch-language-back-to-english
[2019-06-25 21:37:59 INFO] Experiment ended with status: completed
```

In this experiment, we have two probes checking two basic facets of our system.
First, we ensure the locale file exists and then we validate the file contains
our expected value.

Let's now analyse the two tolerances we used.

First, we use a Python provider which calls the [os.path.exists(path)][ope]
standard library function. This function returns a boolean and that is what the
tolerance checks for.

[ope]: https://docs.python.org/3/library/os.path.html#os.path.exists

The second probe calls a process which sets its exit code to `0` when the
command succeeds. Again, this is the value that the tolerance validates.

Now that we know the basics, let's move on to see what are the supported
tolerances.

## Built-in supported tolerances

The [experiment specification][spec] describes the supported tolerances but
let's review them more pragmatically here.

[spec]: https://docs.chaostoolkit.org/reference/api/experiment/#steady-state-probe-tolerance

Chaos Toolkit aims at being easy for simple tasks whenever it can. In this case,
for the general use-cases, we support the following tolerances:

* `boolean`: set the tolerance property to `true` | `false`
* `integer`: set the tolerance property to any integer (negative or positive)
* `string`: set the tolerance property to a string
* `list`: set the tolerance property to a sequence of values that can be
  compared to the output by value

In these three cases, the probe's output must equal the given tolerance.

On top of this native types, we support also more advance cases such as:

* `range`: set the tolerance property to:
   ```json
   {
       "type": "range",
       "range": [6.4, 7.5]
   }
   ```
   The `range` is an inclusive min-max range made of numerical values. This is
   handy when validating a gauge for instance.

* `regex`: set the tolerance property to:
   ```json
   {
       "type": "regex",
       "pattern": "^welcome=hello$"
   }
   ```
    The `pattern` must be a valid regular expression, for now supported by the
    [Python engine][re]. This is useful when looking for a value in a rawstring.

[re]: https://docs.python.org/3/library/re.html#module-re

* `jsonpath`: set the tolerance property to:
   ```json
   {
       "type": "jsonpath",
       "path": "..."
   }
   ```
    The `path` must be a valid JSONPath supported by the [jsonpath2][] library.
    This is handy when looking for a value in a mapping output.
    
[jsonpath2]: https://jsonpath2.readthedocs.io/en/latest/exampleusage.html

* `probe`: set the tolerance property to:
   ```json
   {
       "type": "probe",
       "provider": {
           "type": "python",
           ...
       }
   }
   ```
   In that case the tolerance is run as yet another probe which must return
   a boolean. The probe must accept an argument called `value` that is set
   to the output of the steady-state probe. In essence, a probe validating the
   output of another probe. This is advanced stuff only used when the builtin
   probes won't cut it.

## Common scenarios

Let's now review how to apply these tolerances to most common scenarios.

### Validate the return code of a boolean Python probe

In this case, the simple `boolean` tolerance will do.

For instance:

```json
{
    "type": "probe",
    "name": "lookup-lang-file",
    "tolerance": true,
    "provider": {
        "type": "python",
        "module": "os.path",
        "func": "exists",
        "arguments": {
            "path": "default.locale.txt"
        }
    }
}
```

### Validate the exit code of a process

In this case, the simple `integer` tolerance will do. Indeed, the Chaos Toolkit
will look by default to the exit code of the process for validation.

In the above example:

```json
{
    "type": "probe",
    "name": "lookup-text-in-lang-file",
    "tolerance": 0,
    "provider": {
        "type": "process",
        "path": "grep",
        "arguments": "welcome=hello default.locale.txt"
    }
}
```

Assuming, we would be expecting an error, which commonly translates to an
exit code `1`, we would switch to `"tolerance": 1`.

### Validate the status code of a HTTP probe

In this case, the simple `integer` tolerance will do. Indeed, the Chaos Toolkit
will look by default to the status code of the HTTP response for validation.

For instance:

```json
{
    "type": "probe",
    "name": "resource-must-exist",
    "tolerance": 200,
    "provider": {
        "type": "http",
        "url": "https://example.com/api/v1/entity"
    }
}
```

## Specific scenarios

### Validate the stdout/stderr of a process

Assuming you want to validate the actual standard output of a process, you
need to got a regular expression approach, as follows:

```json
{
    "type": "probe",
    "name": "lookup-text-in-lang-file",
    "tolerance": {
        "type": "regex",
        "pattern": "welcome=hello",
        "target": "stdout"
    },
    "provider": {
        "type": "process",
        "path": "cat",
        "arguments": "default.locale.txt"
    }
}
```

The important extra property to set here is `target` which tells the Chaos
Toolkit where to locate the value to apply the pattern against. The reason we
set `stdout` here is because a process probe returns an object made of three
properties: `"status"`, `"stdout"` and `"stderr"`.

### Validate the JSON body of a HTTP probe

In this case, use a `jsonpath` tolerance. 

For instance, let's assume you receive the following JSON payload:

```json
{
    "foo": [{"baz": "hello"}, {"baz": "bonjour"}]
}
```

```json
{
    "type": "probe",
    "name": "resource-must-exist",
    "tolerance": {
        "type": "jsonpath",
        "path": "$.foo.*[?(@.baz)].baz",
        "expect": ["hello", "bonjour"],
        "target": "body"
    },
    "provider": {
        "type": "http",
        "url": "https://example.com/api/v1/entities"
    }
}
```

The `expect` property tells the Chaos Toolkit what are the values to match
against once the JSON Path has been applied against the `body` of the response
of the HTTP probe's output.

You mays also validate against a number of extracted values instead:


```json
{
    "type": "probe",
    "name": "resource-must-exist",
    "tolerance": {
        "type": "jsonpath",
        "path": "$.foo.*[?(@.baz)].baz",
        "count": 2,
        "target": "body"
    },
    "provider": {
        "type": "http",
        "url": "https://example.com/api/v1/entities"
    }
}
```


### Validate the output of a Python probe returning a mapping

In this case, use a `jsonpath` tolerance.

For instance, let's assume you receive the following payload:

```json
{
    "foo": [{"baz": "hello"}, {"baz": "bonjour"}]
}
```

```json
{
    "type": "probe",
    "name": "resource-must-exist",
    "tolerance": {
        "type": "jsonpath",
        "path": "$.foo.*[?(@.baz)].baz",
        "expect": ["hello", "bonjour"]
    },
    "provider": {
        "type": "python",
        "module": "...",
        "func": "..."
    }
}
```

The `expect` property tells the Chaos Toolkit what are the values to match
against once the JSON Path has been applied against the probe's output.

You mays also validate against a number of extracted values instead:

```json
{
    "type": "probe",
    "name": "resource-must-exist",
    "tolerance": {
        "type": "jsonpath",
        "path": "$.foo.*[?(@.baz)].baz",
        "count": 2
    },
    "provider": {
        "type": "python",
        "module": "...",
        "func": "..."
    }
}
```

## Advanced Scenarios

The last case you may be reviewing now is when the default tolerances cannot
support your use case. Then, you want to create your own tolerance by writing
a new probe that takes the output, of the tolerance under validation, as an
argument. Usually, this tolerance probe is implemented in Python to have more
power but this isn't compulsory.

For instance, the following:

```json
{
    "type": "probe",
    "name": "lookup-text-in-lang-file",
    "tolerance": 0,
    "provider": {
        "type": "process",
        "path": "grep",
        "arguments": "welcome=hello default.locale.txt"
    }
}
```

could be written as follows:

```json
{
    "type": "probe",
    "name": "lookup-text-in-lang-file",
    "tolerance": {
        "type": "probe",
        "provider": {
            "type": "python",
            "module": "my.package",
            "func": "search_text",
            "arguments": {
                "path": "default.local.txt",
                "search_for": "welcome=hello"
            }
        }
    },
    "provider": {
        "type": "process",
        "path": "cat",
        "arguments": "default.locale.txt"
    }
}
```

In that case, implement the
`search_text(path: str, search_for: str, value: dict) -> bool` function in the
`my.package` Python module.


```python
import re


def search_text(path: str, search_for: str, value: dict) -> bool:
    with open(path) as f:
        content = f.read()
        return re.compile(search_for).match(value["stdout"]) is not None
```

As you can see, the `value` argument is not declared but must exist in the
signature of the function. It is injected by the Chaos Toolkit and is set to
the probe's output.


