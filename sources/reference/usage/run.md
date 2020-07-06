# The `chaos run` command

You use the `chaos run` command to execute your declarative chaos engineering 
experiments. To see the options that can be passed to the `chaos run` command, 
execute:

```
(chaostk) $ chaos run --help
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/e5TV7CnAEB4KmS4kNfEjGmADF.js" id="asciicast-e5TV7CnAEB4KmS4kNfEjGmADF" async></script></div>

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
