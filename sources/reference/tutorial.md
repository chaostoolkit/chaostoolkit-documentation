# Getting Started with the Chaos Toolkit

When you practice chaos engineering, you are discovering how your system
reacts following certain conditions you inject. By doing this in a controlled
fashion, you may learn how to change the system accordingly.

This tutorial will quickly give you a tour of the basic elements of an
experiment.

!!! tip
    You will find many more in-depth labs on
    [GitHub](https://github.com/chaosiq/chaostoolkit-demos).

[katacoda]: https://katacoda.com/chaostoolkit

## Get Ready

Before you can run the experiment against your system, you will need to have
it setup.

### Get the Code

You can fetch the code as follows:

```console
git clone https://github.com/chaostoolkit/chaostoolkit-documentation-code
```

This particular tutorial is under `tutorials/a-simple-walkthrough`.

### Third-party binaries

The experiment will use the following binaries, make sure you have them in your
PATH:

* openssl
* pkill

### Install the Application dependencies

Our application is made of a simple set of two microservices that converse
with each other over HTTPS.

!!! tip
    It's recommended that you use a 
    [Python virtual environment](/reference/usage/install/#create-a-virtual-environment)
    to keep your project dependencies isolated from any other projects.

As you should already run Python 3 for the toolkit itself, we assume you are set
accordingly, please install only the application dependencies:

```console
pip install -U -r requirements.txt
```

### Install the Chaos Toolkit

You must install the Chaos Toolkit and its dependencies for the purpose of this
tutorial. While we suggest you go through the [install][] section, it boils
down to:

[install]: usage/install.md

```console
pip install -U chaostoolkit
```

## Your First Experiment

### Explore a Potential Weakness

So, looking at our application, what could we consider as of interest to
discover through an experiment? Well, we are using HTTPS between the two
services in our application, what if the certificate expired?

!!! tip
    In such a simple setup, we appreciate that things will likely break and, in
    general there is no point to run an experiment when you already know the
    outcome. However, let's humor ourselves for the sake of learning the
    basics behind the Chaos Toolkit.

We can intuit things will fall apart if the sunset service cannot talk the
astre service but, should the chain be part of much more complex graph of
services, it could be difficult to fully understand all the branches that
would be affected nor how badly. So, it may still be useful to experiment by
injecting an expired certificate.

### Define the Steady State Hypothesis

You can only learn if you know where you start from and what a good baseline
for your application is.

Here we assume two things:

* the services are running
* we can call the sunset service to retrieve the sunset time for a given city

During our experiment, we will vary the conditions of the system and expect the
state to remain valid.

### Changing the Conditions

In this tutorial, we are going to set an expired certificate and restart the
services. We will then call our application and see how it responds.

### Declare an Experiment to Observe the Weakness

At this stage, we can create an experiment that tells how the system behaves
when a certificate expires.

```json
{!code/tutorials/a-simple-walkthrough/experiment.json!}

```

#### The Various Sections of an Experiment

Let's now go through the experiment blocks.

The steady state hypothesis declares the various probes that will be applied
as part of the hypothesis check.

The hypothesis is played twice. The first time before we do anything else to
ensure the system is indeed in a normal state, here we check the services are
running by looking up their PID files and we call the sunset service which
should respond OK. The second time the hypothesis is applied is after the
conditions were changed in the system, to validate it is still in a normal
state.

The method is the block which changes the conditions of our system/application.
Here, we swap the valid certificate for an expired one and restart the services
by sending them a SIGHUP signal.

Finally, the rollback section (which is optional) tries to remediate to the
changes we made, in this case by swapping back to the valid certificate.

#### Different Kinds of Activities

It is interesting to notice that the hypothesis uses probes while rollbacks are
made of actions only. The method may use both. The reason is that the
hypothesis is only about querying the system while rollbacks act on it. Finally,
it is often useful to query the system while we change the conditions, for
future analysis.

Probes and Actions are activities that do not differ in the way they work, it's
only their goal that differs.

You can create activities that make HTTP calls, execute processes or perform
more complex operations through extensions (often implemented in Python). This
tutorial showcases a bit of all of those.

#### Tolerances in the Hypothesis

Hypothesis probes expect a `tolerance` property which tells the Chaos Toolkit
how to validate a certain aspect of the state. In our example, tolerances are
rather simple. We check file exists and that a HTTP request returns a status
code of `200`. Richer tolerances can be created by using regex or jsonpath.

## Run the Experiment

### Start the Experiment without the Application

To run the experiment, simply execute the following command:

```console
chaos run experiment.json
```

```
[2018-05-14 18:38:04 INFO] Validating the experiment's syntax
[2018-05-14 18:38:04 INFO] Experiment looks valid
[2018-05-14 18:38:04 INFO] Running experiment: What is the impact of an expired certificate on our application chain?
[2018-05-14 18:38:04 INFO] Steady state hypothesis: Application responds
[2018-05-14 18:38:04 INFO] Probe: the-astre-service-must-be-running
[2018-05-14 18:38:04 CRITICAL] Steady state probe 'the-astre-service-must-be-running' is not in the given tolerance so failing this experiment
[2018-05-14 18:38:04 INFO] Let's rollback...
[2018-05-14 18:38:04 INFO] Rollback: swap-to-vald-cert
[2018-05-14 18:38:04 INFO] Action: swap-to-vald-cert
[2018-05-14 18:38:04 INFO] Rollback: None
[2018-05-14 18:38:04 INFO] Action: restart-astre-service-to-pick-up-certificate
[2018-05-14 18:38:04 INFO] Rollback: None
[2018-05-14 18:38:04 INFO] Action: restart-sunset-service-to-pick-up-certificate
[2018-05-14 18:38:04 INFO] Pausing after activity for 1s...
[2018-05-14 18:38:05 INFO] Experiment ended with status: failed
```

Because we ran this command before we even started our application, our
steady-state hypothesis failed and bailed the experiment immediately.

Note that the rollbacks will run anyway. They are only bypassed when you
send a SIGINT or SIGTERM signal to the `chaos` process because the toolkit
assumes you may want to review your system.

### Start the Application

You may now run the application.

First, copy the valid certificate as follows:

```console
cp valid-cert.pem cert.pem
```

Next, start the services, in one terminal:

```console
python3 astre.py
```

```
[14/May/2018:16:11:09] ENGINE Listening for SIGTERM.
[14/May/2018:16:11:09] ENGINE Listening for SIGHUP.
[14/May/2018:16:11:09] ENGINE Listening for SIGUSR1.
[14/May/2018:16:11:09] ENGINE Bus STARTING
[14/May/2018:16:11:09] ENGINE Serving on https://127.0.0.1:8444
[14/May/2018:16:11:09] ENGINE Bus STARTE
```
Then, in another terminal:

```console
python3 sunset.py
```

```
[14/May/2018:16:13:58] ENGINE Listening for SIGTERM.
[14/May/2018:16:13:58] ENGINE Listening for SIGHUP.
[14/May/2018:16:13:58] ENGINE Listening for SIGUSR1.
[14/May/2018:16:13:58] ENGINE Bus STARTING
[14/May/2018:16:13:58] ENGINE Serving on https://127.0.0.1:8443
[14/May/2018:16:13:58] ENGINE Bus STARTED
```

Now you may perform a simple call:

```console
curl -k https://localhost:8443/city/Paris
The sunset will occur at 2018-05-14T21:23:09+02:00 in Paris
```

What happens is that the sunset service performs a call to the astre service
for the data and simply render them to you, as plain text. Both services are
chained together over HTTPS.

### Run the Experiment

Now your application is running, execute the experiment once again:

```console
chaos run experiment.json
```

```
[2018-05-14 18:41:09 INFO] Validating the experiment's syntax
[2018-05-14 18:41:09 INFO] Experiment looks valid
[2018-05-14 18:41:09 INFO] Running experiment: What is the impact of an expired certificate on our application chain?
[2018-05-14 18:41:09 INFO] Steady state hypothesis: Application responds
[2018-05-14 18:41:09 INFO] Probe: the-astre-service-must-be-running
[2018-05-14 18:41:09 INFO] Probe: the-sunset-service-must-be-running
[2018-05-14 18:41:09 INFO] Probe: we-can-request-sunset
[2018-05-14 18:41:09 INFO] Steady state hypothesis is met!
[2018-05-14 18:41:09 INFO] Action: swap-to-expired-cert
[2018-05-14 18:41:09 INFO] Probe: read-tls-cert-expiry-date
[2018-05-14 18:41:09 INFO] Action: restart-astre-service-to-pick-up-certificate
[2018-05-14 18:41:09 INFO] Action: restart-sunset-service-to-pick-up-certificate
[2018-05-14 18:41:09 INFO] Pausing after activity for 1s...
[2018-05-14 18:41:10 INFO] Steady state hypothesis: Application responds
[2018-05-14 18:41:10 INFO] Probe: the-astre-service-must-be-running
[2018-05-14 18:41:10 INFO] Probe: the-sunset-service-must-be-running
[2018-05-14 18:41:10 INFO] Probe: we-can-request-sunset
[2018-05-14 18:41:10 CRITICAL] Steady state probe 'we-can-request-sunset' is not in the given tolerance so failing this experiment
[2018-05-14 18:41:10 INFO] Let's rollback...
[2018-05-14 18:41:10 INFO] Rollback: swap-to-vald-cert
[2018-05-14 18:41:10 INFO] Action: swap-to-vald-cert
[2018-05-14 18:41:10 INFO] Rollback: None
[2018-05-14 18:41:10 INFO] Action: restart-astre-service-to-pick-up-certificate
[2018-05-14 18:41:10 INFO] Rollback: None
[2018-05-14 18:41:10 INFO] Action: restart-sunset-service-to-pick-up-certificate
[2018-05-14 18:41:10 INFO] Pausing after activity for 1s...
[2018-05-14 18:41:11 INFO] Experiment ended with status: failed
```

Each activity is run in the order it appears in the experiment. Notice now how
the hypothesis is not met after we swapped the certificates. But, we learn
something interesting, even if expected, using an expired certificate does not
prevent our services to even start.

## Report on your Findings

### Review the Journal of the Run

You may now review the journal generated by the run:

```console
cat journal.json
```

It contains the activities runs and the output of each of them.

### Generate a Report

You can generate a PDF (or HTML, markdown...) report from the journal if you
install the [chaostoolkit-reporting][reporting] plugin first:

[reporting]: https://github.com/chaostoolkit/chaostoolkit-reporting

```console
chaos report --export-format=pdf journal.json report.pdf
```

### Learnings and Responses

In this experiment, we proved what we guessed initially, that an expired
certificate will create trouble and break the application for our users. What
could be the responses?

* Use a circuit-breaker to provide a more meaningful, and controlled, answer
  to the caller
* Prevent the service to start when the certificate it uses is expired
* Put some monitoring in place on our certificates and trigger an alert when
  they get close to their end date
* Move to Let's Encrypt and renew our certs automatically

For each of these potential responses, you could create an experiment should they
unearth potential new questions.

## Next?

An experiment is never the end game. The flow should be continuous and you
should create and run experiments regularly.
