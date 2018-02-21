# How to Investigate Issues

When your experiment fails to work as you would expect, you should start
looking at the `chaostoolkit.log` file written to by the `chaos` command.

This file contains a lot of traces from the Chaos Toolkit core but also any
extensions that used the toolkit's logger.

As new logs are appended to that file, it may grow big. Do not hesitate to
wipe it out from time to time.

Please, do make sure to visit our [Slack][slack] or [GitHub][gh] when you have
a question around how the toolkit does things. The community will be pleased
to help you out.

[slack]: https://join.chaostoolkit.org/
[gh]: https://github.com/chaostoolkit