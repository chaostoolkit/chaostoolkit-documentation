# The `chaos run` command

You use the `chaos run` command to execute your declarative chaos engineering 
experiments. To see the options that can be passed to the `chaos run` command, 
execute:

```
(chaostk) $ chaos run --help
```

A tutorial on how to use the `chaos run` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Executing an Experiment Plan

To execute an experiment plan you simply pass it to the `chaos run` command:

```
(chaostk) $ chaos run my-plan.json
```

`chaostoolkit` will log all the steps it follows from your plan in a journal by 
default called `chaos-report.json`. You can specify the name of this journal 
output file using the `--report-path` option.

## Rehearsing an experiment execution

To test that you have a valid experiment you can pass the `--dry` option.

## Run an experiment without validation

You can run an experiment and skip the experiment's validation using the 
`--no-validation` option.
