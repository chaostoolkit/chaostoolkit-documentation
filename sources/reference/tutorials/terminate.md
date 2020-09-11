# Learn all about terminating an experiment

Chaos Engineering is a powerful tool that may lead to undesirable side effects
in your system. Sometimes, it is expected that an operator, or an automated
service, terminates an experiment much earlier to prevent further difficulties.

In this tutorial, we are going to review all facets of terminating a Chaos
Toolkit experiment.

## Let's start with the default behavior

When an experiment runs to its end it means that, even if a deviation was
found, the Chaos Toolkit should leave nothing hanging around, such as zombie
processes. Also, if rollbacks were declared and requested to be applied, they
will be played. In other words, if your experiment is properly constructed, 
you should not have to do anything else.

Chaos Toolkit makes no promises that your system will be back to its normal
however. The discovery you make along the way usually resolves in impacts
that cannot be anticipated.

This means that when an experiment finishes, your system may well be in a
very strange state but it does not mean Chaos Toolkit failed at doing its job.
In fact, it's quite the exact nature of the beast: Chaos Engineering is making
those pain points very clear to all.

Experiments can be interrupted. In that case, Chaos Toolkit tries its best
to abide by the runtime condition that you set. For instance, if you decided
to always play the rollbacks, Chaos Toolkit will execute them. The default
behavior is not to play them however for the simple reason that if you
interrupted an experiment, you may well want to investigate the system and if
rollbacks were executed, you may lose some important traces or state.

The diagram below shows the flow used by Chaos Toolkit when running
and terminating an experiment:


![](./static/images/ctk.flow.svg)

### Digging into the interruption's flow

When the Chaos Toolkit receives a signal, it starts the
termination flow of the experiment:

* When this happens during the first pass of
  the steady-state hypothesis block, this means the experiment finishes before
  its method is applied. In that case, rollbacks do not need to be played in any
  case.
* When the signal is caught during the method, remaining activities are not
  executed and the current running experiment is completed. Rollbacks are played
  if the strategy requested they are played. Otherwise, they are ignored.
  If an activity is running in the background, the experiment will wait until
  it finishes.
* When the signal is caught during the rollbacks, remaining actions are not
  played and the experiment finishes.

### Reacting to signals, aka being a good citizen

The Chaos Toolkit knows it makes operators confident it will act appropriately
upon receiving a variety of [signals][]. It supports therefore the following
signals:

[signals]: https://en.wikipedia.org/wiki/Signal_(IPC)

* `SIGINT` 
  Mostly received when the operator hits Ctrl-C. This triggers the
  interruption flow.

* `SIGTERM`
  This signal is often used by other processes to indicate the Chaos Toolkit
  process ought to terminate. For instance, this is the signal sent to
  Kubernetes pods (with a graceful period before the harsher SIGKILL)

* `SIGUSR1`/`SIGUSR2` (Unix only)
  These two signals are rarely sent by operators but are used so that experiment
  extension author can programmatically terminate the experiment without
  having to wait for any blocking operation. 

In all cases, the termination flow is triggered. The only different one is
`SIGUSR2` which will always ignore rollbacks and will not wait for background
activities to terminate normally. In other words, `SIGUSR2` is the only way you
can terminate harshly an experiment.

Otherwise, there are no visible difference between `SIGINT`, `SIGTERM` and
`SIGUSR1`.

