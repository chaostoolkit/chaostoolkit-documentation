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
[concepts]: ../concepts.md

This project is implemented in Python 3.

## chaostoolkit-documentation

The [chaostoolkit-documentation][chaosdoc] is the documentation source and
renderer of the Chaos Toolkit. Namely, that project generates the website you
are currently reading.

[chaosdoc]: https://github.com/chaostoolkit/chaostoolkit-documentation

This project is implemented in Python 3 by generating HTML from Markdown
documents.

## chaostoolkit-kubernetes

The [chaostoolkit-kubernetes][chaosk8s] project is the Kubernetes extension.

[chaosk8s]: https://github.com/chaostoolkit/chaostoolkit-kubernetes

This project is implemented in Python 3.

## chaostoolkit-addons

The [chaostoolkit-addons][chaosaddons] project is a set of addons for Chaos
Toolkit: useful controls, probes, actions and tolerances.

[chaosaddons]: https://github.com/chaostoolkit/chaostoolkit-addons

This project is implemented in Python 3.

## chaostoolkit-reporting

The [chaostoolkit-reporting][chaosreporting] project is a plugin for Chaos
Toolkit to create PDF/HTMl reports from executions.

[chaosreporting]: https://github.com/chaostoolkit/chaostoolkit-reporting

This project is implemented in Python 3.

## chaostoolkit-bundler

The [chaostoolkit-bundler][chaosbundler] project is a binary package of
Chaos Toolkit and its most common extensions. In case you want a drop in
Chaos Toolkit for your system.

[chaosbundler]: https://github.com/chaostoolkit/chaostoolkit-bundler

This project is implemented in Python 3.
