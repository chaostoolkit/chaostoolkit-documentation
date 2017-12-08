# Extending the Chaos Toolkit

The ChaosToolkit does not implement probes and actions natively. Instead,
it [supports][api] three extension mechanisms:

[api]: /api/experiment
[pyfuncapi]: /api/experiment#python-provider
[httpapi]: /api/experiment#http-provider
[procapi]: /api/experiment#process-provider

* [Python function][pyfuncapi]
* [Process][procapi]
* [HTTP][httpapi]

You can extend your actions and probes by implementing them in one of these
extension providers.

The Python function runs in the same process as the `chaostoolkit` itself.

The HTTP and Process providers do not need to be packaged per se and can be
declared inlined in your experiment. However, until the specification
supports for importing probes and actions, this means you must copy them from
one experiment to the other. In that case, wrapping them into a Python package
and exposing them via a Python function is a good practice.

    