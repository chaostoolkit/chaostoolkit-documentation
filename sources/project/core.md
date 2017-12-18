# Core Projects

The Chaos Toolkit is made of several projects that work together to provide its
service.

## chaostoolkit

The [chaostoolkit][] project is the command-line interface (CLI), in other words
the command executed by users to run their experiments.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

That project tries to remain as shallow as possible, only providing the user
interface commands by gluing other projects together.

This project is implemented in Python 3.

## chaostoolkit-lib

The [chaostoolkit-lib][chaoslib] project is the core library which implements
the [core concepts][concepts] of the Chaos Toolkit.

[chaoslib]: https://github.com/chaostoolkit/chaostoolkit-lib
[concepts]: ../overview/concepts.md

This project is implemented in Python 3.

## chaostoolkit-documentation

The [chaostoolkit-documehtation][chaosdoc] is the documentation source and
renderer of the Chaos Toolkit. Namely, that project generates the website you
are currently reading.

[chaosdoc]: https://github.com/chaostoolkit/chaostoolkit-documentation

This project is implemented in Python 3 by generating HTML from Markdown
documents.