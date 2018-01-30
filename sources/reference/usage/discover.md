# The `chaos discover` command

You use the `chaos discover` command to specify a Chaos Toolkit integration extension and,
if supported by the integration, to then explore your target environment in order 
to build a `discovery report` that can be used by the [`chaos init`](init.md) command to help 
you bootstrap your own chaos engineering experiments.

You can see the options available to you by executing:

```
(chaostk) $ chaos discover --help
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/ibkerDuO6HbxjrBT5QyOpqQ8g.js" id="asciicast-ibkerDuO6HbxjrBT5QyOpqQ8g" async></script></div>

A tutorial on how to use the `chaos discover` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Discovering capabilities and experiments 

To execute discover all you need to do is specify the Chaos Toolkit integration 
extension that you'd like to use, for example to use Kubernetes:

```
(chaostk) $ chaos discover chaostoolkit-kubernetes
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/fhUEl9Pd9kU9sI4Dc9yPO47JY.js" id="asciicast-fhUEl9Pd9kU9sI4Dc9yPO47JY" async></script></div>

The `chaos discover` command will produce a report saved in `./discovery.json` by default, 
although you can specify where this report is produced by supplying the 
`--discovery-report-path` option.

## Discovery without System Information

To not probe the target system during the discovery process you can supply the 
`--no-system-info` option.

## Discovery without Installation of an Integration Extension

If you already have the integration extension installed and available you can 
speed up the discovery process by specifying the `--no-install` option.
