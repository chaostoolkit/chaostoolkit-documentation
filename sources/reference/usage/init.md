# The `chaos init` command

You use the `chaos init` command to take a `discovery report`, usually created 
by the [`chaos discover`](discover.md) command, to then create an experiment based upon 
what has been discovered about the integration extension and, if applicable, 
the target environment.

You can see the options available to you by executing:

```
(chaostk) $ chaos init --help
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/cXD9XCvCXBQEJQsq9MahdRwlE.js" id="asciicast-cXD9XCvCXBQEJQsq9MahdRwlE" async></script></div>

A tutorial on how to use the `chaos init` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Initialise a new experiment 

To initialise a new experiment based on what has been [discovered](discover.md) 
you simply need to execute the `chaos init` command:

```
(chaostk) $ chaos init
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/UrLqTuAGyyLoLZrC5c2IAkT50.js" id="asciicast-UrLqTuAGyyLoLZrC5c2IAkT50" async></script></div>

By default, the `chaos init` command will look for a `./discovery.json` 
file and use that as the basis of a new experiment's initialisation.

You can specify another file to be used by suppling the 
`--discovery-report-path` option.

In addition the default output from the `init` command will be a new 
Chaos Toolkit experiment definition in a `./experiment.json` file. If you would 
prefer a different filename then this can be specified using the 
`--experiment-path` option.
