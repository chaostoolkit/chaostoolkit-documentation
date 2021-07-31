# The `chaos run` command

You use the `chaos run` command to execute your declarative chaos engineering 
experiments. To see the options that can be passed to the `chaos run` command, 
execute:

```
(chaostk) $ chaos run --help
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/qxx1haDxBduTCmJzn1ASTWkDe.js" id="asciicast-qxx1haDxBduTCmJzn1ASTWkDe" async></script></div>

A tutorial on how to use the `chaos run` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Executing an Experiment Plan

To execute an experiment plan you simply pass it to the `chaos run` command:

```
(chaostk) $ chaos run experiment.json
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/RVci6wzv7hHH1ZEOtoM7rsZVT.js" id="asciicast-RVci6wzv7hHH1ZEOtoM7rsZVT" async></script></div>

`chaostoolkit` will log all the steps it follows from your plan in a journal by 
default called `chaos-report.json`. You can specify the name of this journal 
output file using the `--report-path` option.

## Rehearsing an experiment execution

To test that you have a valid experiment you can pass the `--dry` option.

## Run an experiment without validation

You can run an experiment and skip the experiment's validation using the 
`--no-validation` option.

## Run an experiment with different steady state strategies
By default, the steady state will be tested before and after an experiment runs. However, you can specify a different strategy through the `--hypothesis-strategy` parameter. The options are:

* `default` 
* `before-method-only`
* `after-method-only`
* `during-method-only`
* `continuously`

For example:
```
chaos run ./experiment.json --hypothesis-strategy continuously
```

## Run an experiment with different rollback strategies

In Chaos Toolkit, rollbacks are always played unless one of the two followings
is true:

* the steady-state hypothesis deviates before the method
* a control interrupted the execution
* the `chaos` command receives a `SIGINT` or `SIGTERM` signal

The Chaos Toolkit provides a mechanism (since v1.5.0) that gives the operator
a chance to change that behavior.

### Always run rollbacks

Ensure rollbacks are always applied

```
(chaostk) $ chaos run --rollback-strategy=always experiment.json
```

### Run rollbacks only on deviation

Run the rollbacks only if your experiment deviated.


```
(chaostk) $ chaos run --rollback-strategy=deviated experiment.json
```

### Never run rollbacks strategy

Never run any rollbacks, for instance when you want to explore the system
after a successful experiment without undoing what the experiment changed:

```
(chaostk) $ chaos run --rollback-strategy=never experiment.json
```

## Override configuration and secrets at runtime

While configuration and secrets are declared in the experiment itself, you
may sometimes need to override the values at runtime. This can be achieved
through the `--var KEY[:TYPE]=VALUE` or `--var-file filepath.json|yaml|.env`
flags.

The `--var KEY[:TYPE]=VALUE` can only override configuration values to prevent
laking secrets on the command line. The `KEY` is the final key used in the
experiment, for instance:


```json
{
    "configuration": {
        "message": "hello world"
    }
}
```

or


```json
{
    "configuration": {
        "message": {
            "type": "env",
            "key": "MY_MESSAGE"
        }
    }
}
```

In both cases, the override key is `message`.

If you specify the `TYPE` it must be one of `str, int, float, bytes` with
`str` the default so not required. Chaos Toolkit will try to convert the given
`VALUE` to the specified type and fail if it cannot.


The `--var-file filepath.json|yaml|.env` gives you the opportunity to override
the configuration and secrets blocks. the format of the json and yaml files
are as follows:

```json
{
    "configuration": {
        "KEY": VALUE
    },
    "secrets": {
        "scope": {
            "KEY": VALUE
        }
    }
}
```

```yaml
---
configuration:
  KEY: VALUE
secrets:
  scope:
    KEY: VALUE
```

The `secrets` block follows the same format as the experiment so the `scope`
is the scope given in the experiment. For example:


```json
{
    "configuration": {
        "service_name": "ec2"
    },
    "secrets": {
        "aws": {
            "api_token": "1234",
            "something": "whatever"
        }
    }
}
```

would turn as the following var file:

```json
{
    "secrets": {
        "aws": {
            "api_token": "56787"
        }
    }
}
```

We are not overridding the `configuration` section and only part of the
`secrets` section.

Finally, should you keep your variables in a .env file, it will only be able
to override the configuration.