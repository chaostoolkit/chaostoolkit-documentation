# The `chaos init` command

You use the `chaos init` command to take a `discovery report`, usually created 
by the [`chaos discover`](discover.md) command, to then create an experiment based upon 
what has been discovered about the integration extension and, if applicable, 
the target environment.

You can see the options available to you by executing:

```
chaos init --help
```
```
Usage: chaos init [OPTIONS]

  Initialize a new experiment from discovered capabilities.

Options:
  --discovery-path PATH   Path to the discovery outcome.  [default:
                          ./discovery.json]
  --experiment-path PATH  Path where to save the experiment (.yaml or .json)
                          [default: ./experiment.json]
  --help                  Show this message and exit.
```

A tutorial on how to use the `chaos init` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Initialise a new experiment 

To initialise a new experiment based on what has been [discovered](discover.md) 
you simply need to execute the `chaos init` command:

```
chaos init
```

<div class="screen-reader-text">
The following is a capture of the output after running chaos init and following the interactive prompts:

[2018-01-30 15:54:50 INFO] Let's build a new experiment
Experiment's title: My new experiment
Add an activity to your method
Activity (0 to escape): 1
Kill a microservice by `name` in the namespace `ns`.

The microservice is killed by deleting the deployment for it without
a graceful period to trigger an abrupt termination.

The selected resources are matched by the given `label_selector`.
Do you want to use this action? [y/N]: y
Argument's value for 'name':
Argument's value for 'ns' [default]:
Argument's value for 'label_selector' [name in ({name})]: app=webapp-app
Do you want to select another activity? [y/N]: N
[2018-01-30 15:55:21 INFO] Experiment created and saved in './experiment.json'
</div>

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/UrLqTuAGyyLoLZrC5c2IAkT50.js" id="asciicast-UrLqTuAGyyLoLZrC5c2IAkT50" async></script></div>

By default, the `chaos init` command will look for a `./discovery.json` 
file and use that as the basis of a new experiment's initialisation.

You can specify another file to be used by suppling the 
`--discovery-report-path` option.

In addition the default output from the `init` command will be a new 
Chaos Toolkit experiment definition in a `./experiment.json` file. If you would 
prefer a different filename then this can be specified using the 
`--experiment-path` option.
