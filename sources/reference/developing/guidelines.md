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

* Python 3.6+ installed.
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
[contribute](../contributing.md), you will need to have an account there.

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
* [chaostoolkit-addons](https://github.com/chaostoolkit/chaostoolkit-addons)

In addition, there are a
[bunch of incubating projects](https://github.com/chaostoolkit-incubator).

## Creating an Extension

Please review the various [approaches](../extending/approaches.md) to extend
the toolkit.

## Creating a Notification Plugin

The Chaos Toolkit triggers events while it runs. Those events may be forwarded
to any endpoint that you care for through HTTP or, when you need more control,
a full Python project.

There is no template for such a project yet but it is very close to an
extension project except it doesn't have probes and actions. You can therefore
start by cloning the [extension template project][ext] and start from there.

[ext]: https://github.com/chaostoolkit/chaostoolkit-extension-template

Instead, it should define a function in a module. That function takes two
parameters:

* the notification channel settings (coming from the
  [Chaos Toolkit settings file](../usage/cli.md#create-the-settings-file)) as a dictionary
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
import logzero

def notify(settings: Dict[str, Any], event: EventPayload):
    if event["name"] == RunFlowEvent.RunStarted.value:
        logzero.info("Event phase " + event["phase"])
        logzero.info("Event timestamp " + event["ts"])
        logzero.info("Event payload " + event["payload"])
        logzero.info("Event error " + event.get("error", "N/A"))
```

`logzero` is a third-party package that the Chaos Toolkit uses to log when
it runs.
