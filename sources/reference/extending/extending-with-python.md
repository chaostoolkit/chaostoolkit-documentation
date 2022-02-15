# Extending Chaos Toolkit with Python

## Create your new Chaos Toolkit extension project

All Chaos Toolkit extensions follow the same structure and you can benefit from
a [project template][tpl]. You can create a repository using that template
from the GitHub UI or using the [gh][ghcli].

[tpl]: https://github.com/chaostoolkit/chaostoolkit-extension-template
[ghcli]: https://cli.github.com/manual/

```console
$ gh repo create mytest --private -p chaostoolkit/chaostoolkit-extension-template
```

## Where to put your code

There are two extension points for a Chaos Toolkit Python extension, and they
are captured in two files: `actions.py` and `probes.py`.

It is conventional to use the `actions.py` module as the place where you expose
the actions that you would like to conduct as part of your Chaos Toolkit
experimental method against the environment you want to inject failure into.

It's also conventional to use the `probes.py` module as the place where you can
integrate with your system's existing
[observability](https://www.infoq.com/articles/charity-majors-observability-failure)
so that those values can be used either for an experiment's
[Steady State Hypothesis][hypothesis], or as
[simple additional data-gathering probes][simple-probe] that can be declared
throughout an experiment's method.

[hypothesis]: ../api/experiment.md#steady-state-probe-tolerance
[simple-probe]: ../api/experiment.md#probe

## Running `Discover` on a New Extension

Chaos Toolkit extensions often implement functionality that assists in 
discovering what a system, and the extension against that system, supports. This
is executed using the `chaos discover` command.

When writing your own implementation of discovery you will often want to test 
the new functionality locally. To do this you should first execute from your 
extension workspace:

`$ python setup.py develop`

Then you can exercise your discovery functionality using the `--no-install` flag
 on the `chaos discover` command, for example:

`chaos discover --no-install ext-name`

## Log From Your Extension

You can write to the Chaos Toolkit log by using the [logzero][] package.

[logzero]: https://logzero.readthedocs.io/en/latest/

```python
from logzero import logger

logger.info("Hello!")
```

Make sure to add `logzero` as an entry of the `requirements.txt` file of your
extension.
