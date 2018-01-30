Chaos Engineering is about building experiments that you and your team can then learn from as you decide what weaknesses to guard against in your production systems. You can then execute those automated experiments as continuously as possible to discover and explore further weaknesses if they arise over time in your system.

To enable and speed up the exploration and implementation of these learning loops through Chaos Engineering the Chaos Toolkit implements a specific workflow through a set of commands that can be run using the Chaos Toolkit's CLI:

* [`discover`](usage/discover.md) - Used to discover the capabilities of your target systems and the levels within those systems
* [`init`](usage/init.md) - Takes what has been discovered and then helps you initialise a new [experiment definition](concepts.md).
* [`run`](usage/run.md) - Takes an experiment definition and executes it.
* [`report`](usage/report.md) - Takes the output from an experiment's execution and produces a report for every stakeholder interested in the experiment's outcome.

This workflow and all of the above commands can be explored in the Chaos Toolkit's freely available online tutorials.

