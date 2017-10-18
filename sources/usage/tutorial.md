## Create your first Experiment

This walkthrough will drive you the basics of writing your very first
experiment.

### Define your hypothesis

Before you start writing code, you need to define your hypthesis. What is it
you are trying to confirm or infirm?

There are various ways to come up with an hypothesis:

* a real scenario that you and your team did not fully get a chance to learn
  from while in emergency mode. Retrospective sessions in agile teams may be
  a great starting point
* [impact mapping][impactmapping] is another strategy to let the team bubble
  up relevant scenarios
* your existing disaster recovery playbooks could be turned into experiments
  that are actively applied against the system


[impactmapping]: https://www.impactmapping.org/

However you come up with your hypothesis, make sure you can analyse the 
result so keep its scope and objective simple and comprehensible.

### Get the requirements

Often, an experiment involves fairly specific access to observe or interact
with the system. Make sure you can gather the right permissions and people on
board.

### A first experiment: a missing file

Let's say we have a service that polls a local file every second to see if new
content was added for processing. Development made the assumption the file
would always be there and did not write a failure code path.

Our hypothesis is that the service should not break but simply try again until
the file comes back. 

Our experiment should try that hypothesis to see where our system stands.

Below is the code of our service as it is now:

```python
{!snippets/tutorials/simple_microservice_before.py!}
```

The code is simple for the purpose of this tutorial. As you can see, we declare
a simple function that reads a file and returns its content when called.

A background thread function writes the current data to that file every 10
seconds.

Notice how we do not check the file exists before reading it soo it is likely
this can fail.

Run this service from another terminal as follows:

```sh
$ python service.py
```

!!! tip

    The [code of this tutorial][tut01] can be found along side this
    documentation.

[tut01]: https://github.com/chaostoolkit/chaostoolkit-documentation/tree/master/sources/shared/snippets/tutorials/

#### Declare your experiment

Below is the experiment for our hypothesis:

```json
{!snippets/tutorials/experiment.json!}
```

Thi experiment shows the bricks of encoding your experiment with Chaos Toolkit.
Once you have provided various metadata, you tell the chaos Toolkit the
activitites it ought to play for us.

Usually we start with a probe that tells us the steady state of our system. In
this case, we simply ensure the exchange file exists. That tells us the
service has its expectation met.

Next, we create the conditions of our hypothesis by pretending our file does not
exist any longer by renaming it.

Finally, we query our service over HTTP and expect a response that does not
indicate the service is unexpectedly broken.

An experiment is made of any numbering of those activities - probes and actions.
Note that an action can also have its own probes for a specific inspection
before and after the action was applied.

The steady probe and the action are implemented by using Python functions while
the last probe performs a HTTP call on your behalf. Please review the
[documentation][extension] for other supported implementations.

[extension]: ../technology/extend.md

#### Run your experiment

To run the experiment, use the `chaostoolkit` CLI as follows:

```sh
(chaostk) $ chaos --change-dir sources/shared/snippets/tutorials run experiment.json
[2017-10-18 15:37:40 WARNING] Moving to sources/shared/snippets/tutorials
[2017-10-18 15:37:40 INFO] Experiment: Does our service tolerate the loss of its exchange file?
[2017-10-18 15:37:40 INFO] Step: Is the file currently where it ought to be?
[2017-10-18 15:37:40 INFO]   Steady State: Looking for data file
[2017-10-18 15:37:40 INFO]   => succeeded with 'True'
[2017-10-18 15:37:40 INFO] Step: Next, we pretend that configuration is gone
[2017-10-18 15:37:40 INFO]   Action: Move the configuration to a different name
[2017-10-18 15:37:40 INFO]   => succeeded with 'None'
[2017-10-18 15:37:40 INFO] Step: Our service should either respond or tell us it is not available
[2017-10-18 15:37:40 INFO]   Steady State: Calling our service
[2017-10-18 15:37:40 ERROR]    => failed: A server error occurred.  Please contact the administrator.
[2017-10-18 15:37:40 INFO] Experiment is now complete
```

Notice the error towards the end, it tells us the service failed with an
unexpected error.

At this stage, you need to pause and analyse the results of this experiment
to decide what to do next.

#### Fix your service

When we ran our service, it broke because the file was not found when read.
Fixing it can take various aspects, we could ensure the file can never be
removed through permissions or locking. Or we could also tolerate such 
failure but let the service return a more appropriate error message in that
case.

This is how we are going to fix it in this tutorial:

```python
{!snippets/tutorials/simple_microservice_after.py!}
```

The service looks very similar but notice how we check the file indeed exists
before reading it. When it does not exist, we return a more useful 
[503 Service Unavailable][503] error that a consumer could interpret as
"try again later".

Note, that we understand a race condition may happen between the time we
checked for the path and the time we read content at that location. We keep
it easy for the benefit of this tutorial.


#### Run your experiment again

Let's run again our experiment now that we have fixed and restart our service:

```sh
(chaostk) $ chaos --change-dir sources/shared/snippets/tutorials run experiment.json
[2017-10-18 15:38:51 WARNING] Moving to sources/shared/snippets/tutorials
[2017-10-18 15:38:51 INFO] Experiment: Does our service tolerate the loss of its exchange file?
[2017-10-18 15:38:51 INFO] Step: Is the file currently where it ought to be?
[2017-10-18 15:38:51 INFO]   Steady State: Looking for data file
[2017-10-18 15:38:51 INFO]   => succeeded with 'True'
[2017-10-18 15:38:51 INFO] Step: Next, we pretend that configuration is gone
[2017-10-18 15:38:51 INFO]   Action: Move the configuration to a different name
[2017-10-18 15:38:51 INFO]   => succeeded with 'None'
[2017-10-18 15:38:51 INFO] Step: Our service should either respond or tell us it is not available
[2017-10-18 15:38:51 INFO]   Steady State: Calling our service
[2017-10-18 15:38:51 INFO]   => succeeded with 'Exchange file is not ready'
[2017-10-18 15:38:51 INFO] Experiment is now complete
```

Notice the error towards the end, it tells us the service failed still but now
we get the error we designed our service for.

#### Go further

In this tutorial, you first approached the Chaos Toolkit to apply experiments
against your system to confirm or infirm your initial hypothesis.

The example is basic on purpose but shows the simplicity of exercising
the [chaos engineering principles][principles] to learn and adapt your system.

The Chaos Toolkit does not limit itself to local use-cases like this one and
offers the possibility to interact with any system through remote API calls.

Please [join us][join] on the Chaos Toolkit community to continue your
exploration.

[principles]: http://principlesofchaos.org/
[join]: https://join.chaostoolkit.org/

