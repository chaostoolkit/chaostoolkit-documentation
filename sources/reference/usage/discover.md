# The `chaos discover` command

You use the `chaos discover` command to specify a Chaos Toolkit integration extension and,
if supported by the integration, to then explore your target environment in order 
to build a `discovery report` that can be used by the [`chaos init`](init.md) command to help 
you bootstrap your own chaos engineering experiments.

You can see the options available to you by executing:

```
chaos discover --help
```
```
Usage: chaos discover [OPTIONS] PACKAGE

  Discover capabilities and experiments.

Options:
  --no-system-info       Do not discover system information.
  --no-install           Assume package already in PYTHONPATH.
  --discovery-path TEXT  Path where to save the the discovery outcome.
                         [default: ./discovery.json]
  --help                 Show this message and exit.
```

A tutorial on how to use the `chaos discover` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Discovering capabilities and experiments 

To execute `discover` all you need to do is specify the Chaos Toolkit integration
extension that you'd like to use, for example to use Kubernetes:

```
chaos discover chaostoolkit-kubernetes
```
```
[2021-07-30 11:43:38 INFO] Attempting to download and install package 'chaostoolkit-kubernetes'
[2021-07-30 11:43:45 INFO] Package downloaded and installed in current environment
[2021-07-30 11:43:45 INFO] Discovering capabilities from chaostoolkit-kubernetes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.actions
[2021-07-30 11:43:45 INFO] Searching for probes in chaosk8s.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.deployment.actions
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.deployment.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.node.actions
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.node.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.pod.actions
[2021-07-30 11:43:45 INFO] Searching for probes in chaosk8s.pod.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.replicaset.actions
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.service.actions
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.service.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.statefulset.actions
[2021-07-30 11:43:45 INFO] Searching for probes in chaosk8s.statefulset.probes
[2021-07-30 11:43:45 INFO] Searching for actions in chaosk8s.crd.actions
[2021-07-30 11:43:45 INFO] Searching for probes in chaosk8s.crd.probes
[2021-07-30 11:43:45 INFO] Discovery outcome saved in ./discovery.json
```

The `chaos discover` command will produce a report saved in `./discovery.json` by default, 
although you can specify where this report is produced by supplying the 
`--discovery-report-path` option.

## Discovery without System Information

To not probe the target system during the discovery process you can supply the 
`--no-system-info` option.

## Discovery without Installation of an Integration Extension

If you already have the integration extension installed and available you can 
speed up the discovery process by specifying the `--no-install` option.
