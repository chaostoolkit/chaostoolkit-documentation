# Run Chaos Toolkit with GitHub Actions

Chaos Toolkit provides a ready to run action for GitHub that makes it easy
to run experiments on GitHub.

## Overview

The action can be found at on the [GitHub marketplace][ghmp].

[ghmp]: https://github.com/marketplace/actions/chaos-toolkit-run-workflow

The way it works is a follows:

* Create a sub-directory in the repository, with your experiments.
* Add the action to a GitHub Workflow and select a strategy to trigger it.
  Whether it's on a push event, manually triggered or scheduled

Here is an example of a simple workflow:

```yaml
name: Inject latency into one of our service

on:
  workflow_dispatch:

jobs:
  run-chaostoolkit-experiment:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v4
    - uses: chaostoolkit/run-action@v0
      with:
        experiment-file: "./slow-down-traffic-from-cloudrun-service.json"
        working-dir: "experiments"
        install-dependencies: gcp;slack;otel
        dependencies-file: requirements.txt
```

The action has a set of arguments allowing you to tune the environment
used to run the experiment. Let's see a few them below.

## Configure the Action

### Change the Python version

By default, the action runs using Python 3.11. You can change this by
setting `python-version` to another version.

### Enable higher verbosity

The action runs with the normal verbosity level of the Chaos Toolkit by
default. You can adjust this to make it more verbose by setting
`verbose: "true"`.

### Set the working directory

It is a good practice to run the experiment from a specific directory in
the repository. To do so you simply set the `working-dir` argument to
whichever path matches your structure. The action will move into that
directory upon running the experiment.

### Set the experiment file path

By default the action will look for an experiment file named `experiment.json`
in the working directory. You will likely give it a different name, for instance
because all your experiments are part of the same directory. Set this name
with the `experiment-file` argument.

### Manage dependencies

The action offers two inclusive approaches to manage the Chaos Toolkit
dependencies.

### Automated dependencies management

As a matter of convenience, the action provides the `install-dependencies` 
argument allowing you to select a set of well-known extensions to be installed.

* `aws`
* `gcp`
* `k8s`
* `otel`
* `slack`

So if your experiment targets Google Cloud and relies on Slack and Open 
Telemetry, you can set `install-dependencies: gcp;slack;otel`.

### Extra dependencies management

Your experiment will often requires more dependencies to be installed. You can
do so by adding a `requirements.txt` file into the working directory and set
the `dependencies-file`. For instance: `dependencies-file: requirements.txt`.

The file must follow the [requirements][rq] format but its name can be anything.

[rq]: https://pip.pypa.io/en/stable/reference/requirements-file-format/

### Enable local binaries

Experiments often rely on binaries found in the `PATH` to be present. You
can do so by adding these binaries in a `bin` directory either at the top
of the repository or inside the working directory. Both locations will be
automatically added to the `PATH` and therefore available to the experiment.

For instance, when running against AWS EKS, this is where you would put the
[aws-iam-authenticator][awsiamauth] binary.

[awsiamauth]: https://github.com/kubernetes-sigs/aws-iam-authenticator

### Passing environment variables & secrets

The action performs as expected when it comes to environment variables. You
simply declare them on the action and they are available to the experiment.

Same goes for secrets. For instance:


```yaml
name: Inject latency into one of our service

on:
  workflow_dispatch:

jobs:
  run-chaostoolkit-experiment:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v4
    - uses: chaostoolkit/run-action@v0
      with:
        experiment-file: "./slow-down-traffic-from-cloudrun-service.json"
        working-dir: "experiments"
        install-dependencies: gcp;slack;otel
        dependencies-file: requirements.txt
      env:
        MY_ENV: hello
        TOKEN: ${{ secrets.TOKEN }}
```

### Schedule an experiment repeatedly

The action lends itself very well for experiments running automatically
at regular intervals. To do so, you simply need to use the [schedule][sched]
faility provided by GitHub.

For instance, running the experiment every Monday morning at 9am looks like
this:

```yaml
name: Inject latency into one of our service

on:
  schedule:
    - cron:  "0 9 * * 1"

jobs:
  run-chaostoolkit-experiment:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v4
    - uses: chaostoolkit/run-action@v0
      with:
        experiment-file: "./slow-down-traffic-from-cloudrun-service.json"
        working-dir: "experiments"
        install-dependencies: gcp;slack;otel
        dependencies-file: requirements.txt
```

### Upload execution results

The action allows you to upload the results of the Chaos Toolkit execution
as part of the job artifacts. The uploaded files are the `chaostoolkit.log`
and `journal.json` files. Both files are aggregated into a compressed
archive. You can set the name of that archive with the `result-artifact-name` 
argument.

If you prefer not to upload the results, set the
`upload-results-as-artifacts` argument to `"false"`.

