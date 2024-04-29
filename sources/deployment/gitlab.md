# Run Chaos Toolkit with Gitlab Component

Chaos Toolkit provides a ready to run component for Gitlab that makes it easy
to run experiments on Gitlab CICD.

## Overview

The component can be found at on the [Gitlab CI/CD Catalog][ghmp].

[ghmp]: https://gitlab.com/explore/catalog/cdoyle27/chaostoolkit-ci-component

The way it works is a follows:

* Create a sub-directory in the repository, with your experiments.
* Add the component using an `include` block to a Gilab CI file and select a strategy to trigger it.
  Whether it's on a push event, manually triggered or scheduled

Here is an example of a simple workflow:

```yaml
include:
  - component: gitlab.com/cdoyle27/chaostoolkit-ci-component/chaostoolkit@0.1.0
    inputs:
    experiment-file: "experiment.yaml"
```

The component has a set of arguments allowing you to tune the environment
used to run the experiment. Let's see a few them below.

## Configure the Component

### Change the Python version

By default, the component runs using Python 3.11. You can change this by
setting `python-version` to another version.

### Enable higher verbosity

The component runs with the normal verbosity level of the Chaos Toolkit by
default. You can adjust this to make it more verbose by setting
`verbose: "true"`.

### Set the working directory

It is a good practice to run the experiment from a specific directory in
the repository. To do so you simply set the `working-dir` argument to
whichever path matches your structure. The component will move into that
directory upon running the experiment.

### Set the experiment file path

By default the component will look for an experiment file named `experiment.json`
in the working directory. You will likely give it a different name, for instance
because all your experiments are part of the same directory. Set this name
with the `experiment-file` argument.

### Manage dependencies

The component offers two inclusive approaches to manage the Chaos Toolkit
dependencies.

### Automated dependencies management

As a matter of convenience, the component provides the `install-dependencies` 
argument allowing you to select a set of well-known extensions to be installed.

* `aws`
* `gcp`
* `k8s`
* `otel`
* `slack`

So if your experiment targets Google Cloud and relies on Slack and Open 
Telemetry, you can set `install-dependencies: gcp;slack;otel`.

### Extra dependencies management

Your experiment will often require more dependencies to be installed. You can
do so by adding a `requirements.txt` file into the working directory and set
the `dependencies-file`. For instance: `dependencies-file: requirements.txt`.

The file must follow the [requirements][rq] format but its name can be anything.

[rq]: https://pip.pypa.io/en/stable/reference/requirements-file-format/

### Enable local binaries

Experiments often rely on binaries found in the `PATH` to be present. You
can do so by adding these binaries in a `bin` directory either at the top
of the repository or inside the working directory. Both locations will be
automatically added to the `PATH` and therefore available to the experiment.

For instance, when running against AWS EKS, this is where you would put the
[aws-iam-authenticator][awsiamauth] binary.

[awsiamauth]: https://github.com/kubernetes-sigs/aws-iam-authenticator

### Passing environment variables & secrets

The component performs as expected when it comes to environment variables. You
simply declare them on the job and they are available to the experiment. This works by setting the job
name or using the jobs default name `chaostoolkit` if no job name is provided. This allows users to 
overide or set variables.

Same goes for secrets. For instance:


```yaml
include:
  - component: gitlab.com/cdoyle27/chaostoolkit-ci-component/chaostoolkit@0.1.0
    inputs:
        experiment-file: "experiment.yaml"
        working-dir: "example_experiment"
        dependencies-file: "requirements.txt"

chaostoolkit:
  variables:
    new_file_name: "../README_ENV_MOVED.md"
```

### Upload execution results

The component will upload the results of the Chaos Toolkit execution
as part of the job artifacts. The uploaded files are the `chaostoolkit.log`
and `journal.json` files. Both files are aggregated into a compressed
archive. You can set the name of that archive with the `result-artifact-name` 
argument.
