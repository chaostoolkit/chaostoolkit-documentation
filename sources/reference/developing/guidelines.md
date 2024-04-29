# Developer Guidelines

Contributors to the Chaos Toolkit are always welcome. This guide describes the
general elements you probably need to know to get started. Once past those
elements, you should dive into the code of each project and come discuss
on our [Slack][slack].

[slack]: https://join.slack.com/t/chaostoolkit/shared_invite/zt-22c5isqi9-3YjYzucVTNFFVIG~Kzns8g

## Overview

### Programming Environment

The programming environment really is up to you. However, since the Chaos
Toolkit is implemented in Python so make sure to have the right tooling for it.

The most basics are:

* Python 3.8+ installed.
* A virtual environment so you can deploy the dependencies in a specific
  environment

If you're not familiar with Python, you will find a few helpful books online,
such [The Hitchhiker’s Guide to Python][hitchhiker].

[hitchhiker]: http://docs.python-guide.org/en/latest/

Historically, Chaos Toolkit used [pip][pip] to manage its projects from a Python
dependencies and packages perspectives. However, we have now migrated
to [PDM][pdm] which provides a better all-in-one experience.

[pip]: https://pip.pypa.io/en/stable/
[pdm]: https://pdm-project.org/en/latest/

### GitHub

The Chaos Toolkit projects are hosted on [GitHub][gh]. If you wish to
[contribute](../contributing.md), you will need to have an account there.

The general workflow is to fork the project you wish to contribute to, make your
changes in a dedicated branch, rebase against the original master and finally
submit a pull-request to the project with a clear description of the what and
why.

[gh]: https://github.com/chaostoolkit/

### Code Contributions Good Practices

Whether you contribute documentation or code, you should try follow the
high-level rules here:

* One PR per functional change. Try to keep your PR focused

* A PR should always have the following:
  * [Signed][signoff] commits (as per the [DCO][dco]) to notify the project you
    are allowed to submit this code change:

    ```bash
    git commit --signoff -m "...." -a
    ```

  * A `CHANGELOG` entry. Do not set the version or date on the entry
  * Tests wherever possible to control non-regression down the road and help
    with maintainance
  * Linted code. If the project uses [pdm][], you can run `pdm run format`
    and `pdm run lint` usually
  * Code must have the appropriate typing annotation

* What to look for in a contribution:
  * Try to draw inspiration from other modules in the same extension or from
    other extensions. Respect the style as much as possible and use the linter
    to ensure you follow it
  * If you had an entirely new module containing actions/probes, make sure
    to make it discoverable by adding it to the `__init__.py` module of the
    extension package. It usually already has existing entries.
  * Make actions/probes not too complex, better to have more specific actions
    sometimes. Otherwise, this increases the risk of breaking compatibility
    when they change
  * Be conservative in changes you make to existing actions/probes. We thrive
    for backward compatibility
  * Keep simple types for actions/probes arguments: string, integer, floats...
  * Raise a Chaos Toolkit exception when you want to notify the user about
    a particular error/edge case that will prevent the function from working
    correctly
  * Use the `logger` as much as needed, it helps figuring out what is going on.
    However think of who will read these messages in the future, likely not
    yourself
  * The returned value of an action/probe must be JSON serializable by the
    Python [json][] module
  * Try to respect a width of 80 characters for code and documentation, this
    should be covered by the code formatter


[signoff]: https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---signoff
[dco]: https://developercertificate.org/
[json]: https://docs.python.org/3/library/json.html#module-json

Here is a typical action:

```python
import logging
from typing import Any, Dict


from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

__all__ = ["change_the_system"]

logger = logging.getLogger("chaostoolkit")


def change_the_system(
    address: str,
    value: int,
    configuration: Configuration = None,
    secrets: Secrets = None
) -> Dict[str, Any]:
    """
    Change the system in funny ways and return the information about
    what changed
    """
    if value < 0:
        logger.debug(f"change_the_system got {value}")
        raise ActivityFailed("value cannot be negative")

    # do something to your system with the given arguments

    return {}
```

Since we have just added this action in a new module, we'll also make the
module discoverable as follows:

```python
activities.extend(discover_actions("extension.actions"))
```

This is done in the top-level `__init__.py` module of the extension in the
`discover` function. Usually, it already contains this function and you can
simply add the line above.

A typical CHANGELOG entry for this new action would be:

```markdown
## [Unreleased][]

[Unreleased]: https://github.com/....

### Added

* The `extension.actions.change_the_system` action to change the system. Use
  it like this:

  ```json
  "method": [
    {
      "name": "do-something",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "extension.actions",
        "func": "change_the_system",
        "arguments": {
          "address": "192.56.67.78",
          "value": 56
        }
      }
    }
  ]
  ```

```