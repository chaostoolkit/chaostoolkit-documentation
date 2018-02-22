# Extending Chaos Toolkit with Python

To create your own extension to the Chaos Toolkit using Python, a [template Python Chaos Toolkit extension project][template-project] is available as a good starting point.

## Create your new Chaos Toolkit extension project

To use the Python template extension project, simply download the latest release of [the baseline project][template-project] from GitHub, place this in your own new project, and make the following amendments:

* Edit the name of the project to the name of your unique extension:
    * Rename the package directory (`chaosext` in the template)
    * Rename the imports in the tests from `chaosext` to the name of your extension's package
    * Make the same change across the `README.md`, the`CHANGELOG.md`, `pytest.ini` and `setup.py`
* Remove `ci.bash` and `.travis.yml` as these are artifacts from the CI build system for the template only.

[template-project]: https://github.com/chaostoolkit/chaostoolkit-extension-template

## Where to put your code

There are two extension points for a Chaos Toolkit Python extension, and they are captured in two files: `actions.py` and `probes.py`.

It is conventional to use the `actions.py` module as the place where you expose the actions that you would like to conduct as part of your Chaos Toolkit experimental method against the environment you want to inject failure into.

It's also conventional to use the `probes.py` module as the place where you can integrate with your system's existing [observability](https://www.infoq.com/articles/charity-majors-observability-failure) so that those values can be used either for an experiment's [Steady State Hypothesis][hypothesis], or as [simple additional data-gathering probes][simple-probe] that can be declared throughout an experiment's method.

[hypothesis]: ../api/experiment.md#steady-state-probe-tolerance
[simple-probe]: ../api/experiment.md#probe

