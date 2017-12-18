# Extending the Chaos Toolkit

The Chaos Toolkit is designed to be extended with new probes and actions so that
you can work with any failure injection and system observability systems that you choose. The toolkit has a growing number of open source extensions for just this purpose, but the intention is that you may also want to extend the Chaos Toolkit for your own unique, possible closed, systems as well.

The ChaosToolkit currently [supports][api] three extension approaches:

[api]: /api/experiment
[pyfuncapi]: /api/experiment#python-provider
[httpapi]: /api/experiment#http-provider
[procapi]: /api/experiment#process-provider

* [Python function][pyfuncapi]
* [Process][procapi]
* [HTTP][httpapi]

You can extend your actions and probes by implementing them using one of these
approaches.
