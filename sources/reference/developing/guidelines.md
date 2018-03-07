# Developer Guidelines

Contributors to the Chaos Toolkit are always welcome. This guide describes the
general elements you probably need to know to get started. Once past those
elements, you should dive into the code of each project and come discuss
on our [Slack][slack].

[slack]: https://join.chaostoolkit.org/

## Overview

### Programming Environment

The programming environment really is up to you. However, since the Chaos
Toolkit is implemented in Python so make sure to have the right tooling for it.

The most basics are:

* Python 3.5+ installed. Right now, we officially support 3.5 and 3.6 but there
  should not be harm in using 3.7 as long as it can gracefully degrade down to
  3.5
* A virtual environment so you can deploy the dependencies in a specific
  environment

If you're not familiar with Python, you will find a few helpful books online,
such [The Hitchhiker’s Guide to Python][hitchhiker].

[hitchhiker]: http://docs.python-guide.org/en/latest/

#### The Ultimate Trick

Whenever you code on one of the projects, you should run the following command
so that the project you are hacking on is part of your virtual environment
without being installed:

```console
(chaostk) $ cd <project-name>
(chaostk) $ python setup.py develop
```

Sometimes, your virtual env may be borked and not point to your development
directory. In that case, make sure to remove any previously installed version
of the project:

```console
(chaostk) $ pip uninstall <project-name>
```

Then make sure your virtual environment point at your local directory with:

```console
(chaostk) $ pip freeze
```

### GitHub

The Chaos Toolkit projects are hosted on [GitHub][gh]. If you wish to
[contribute](../../contributing.md), you will need to have an account there.

The general workflow is to fork the project you wish to contribute to, make your
changes in a dedicated branch, rebase against the original master and finally
submit a pull-request to the project with a clear description of the what and
why.

[gh]: https://github.com/chaostoolkit/

### Chaos Toolkit Projects At A Glance

The Chaos Toolkit is made of several projects. The core ones are:

* [chaostoolkit](https://github.com/chaostoolkit/chaostoolkit): the CLI
* [chaostoolkit-lib](https://github.com/chaostoolkit/chaostoolkit-lib): the core
  library that propels the CLI

Basically, those projects represent the Chaos Toolkit itself. However, the
toolkit is naked without extensions. The currently core extensions are:

* [chaostoolkit-kubernetes](https://github.com/chaostoolkit/chaostoolkit-kubernetes)

In addition, there are a
[bunch of incubating projects](https://github.com/chaostoolkit-incubator).

## Creating an Extension

One of the most common task you could do is add a new extension for your need.
Extensions provide activities that experiments use to perform actions or read
the system's state (via probes).

An extension is a full fledged Python project. To make it simpler to get
started the Chaos Toolkit provides a [template project][ext] that you can start
from.

[ext]: https://github.com/chaostoolkit/chaostoolkit-extension-template

To get going, clone this project and rename the followings:

* the directory containing the source
* anywhere you find an occurence of the template name (`chaostext`) with your
  extension name

Please, mirror existing extensions in the way they are designed and organized.

### Running `Discover` on a New Extension

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

## Creating a notification plugin

The Chaos Toolkit triggers events while it runs. Those events may be forwarded
to any endpoint that you care for through HTTP or, when you need more control,
a full Python project.

There is no template for such a project yet but it is very close to an
extension project except it doesn't have probes and actions. You can therefore
start by cloning the [extension template project][ext] and start from there.

Instead, it should define a function in a module. That function takes two
parameters:

* the notification channel settings (coming from the
  [Chaos Toolkit settings file](../usage/settings.md)) as a dictionary
* the event payload as a Python dictionary which is documented
  [here](https://github.com/chaostoolkit/chaostoolkit-lib/blob/master/chaoslib/notification.py#L97)

The event has a `payload` key which is the content associated to the event. It
can be one of:

* `None` when there was no payload ()
* a string
* an [experiment](../api/experiment.md) dictionary
* an [journal](../api/journal.md) dictionary

Three kind of events can be triggered: `started`, `completed` and `failed` for
each phase of the flow. Those events are defined
[here](https://github.com/chaostoolkit/chaostoolkit-lib/blob/master/chaoslib/notification.py#L21).

A typical notification callback function will look like this:

```python
from typing import Any, Dict

from chaoslib.notification import RunFlowEvent
from chaoslib.types import EventPayload


def notify(settings: Dict[str, Any], event: EventPayload):
    if event["name"] == RunFlowEvent.RunStarted.value:
        print("Event phase " + event["phase"])
        print("Event timestamp " + event["ts"])
        print("Event payload " + event["payload"])
        print("Event error " + event.get("error", "N/A"))
```

## Log From Your Extension or Plugin

You can write to the Chaos Toolkit log by using the [logzero][] package.

[logzero]: https://logzero.readthedocs.io/en/latest/

```python
from logzero import logger

logger.info("Hello!")
```
