# Extending the Chaos Toolkit

The Chaos Toolkit is designed to be extended with new probes and actions so that
you can work with any failure injection and system observability systems that you choose. The toolkit has a growing number of open source extensions for just this purpose, but the intention is that you may also want to extend the Chaos Toolkit for your own unique, possible closed, systems as well.

The ChaosToolkit currently [supports][api] three extension approaches:

[api]: ../api/experiment.md
[pyfuncapi]: ../api/experiment.md#python-provider
[httpapi]: ../api/experiment.md#http-provider
[procapi]: ../api/experiment.md#process-provider

* [Python function][pyfuncapi]: see [this page](extending-with-python.md) for more information on creating Python extensions
* [Process][procapi]
* [HTTP][httpapi]

You can extend your actions and probes by implementing them using one of these
approaches.

!!! tip
    The Chaos Toolkit maintains a set of [open-source extensions][ext] ready to
    be integrated into your Chaos experiments.

[ext]: https://github.com/search?utf8=%E2%9C%93&q=topic%3Achaostoolkit-extension&type=Repositories