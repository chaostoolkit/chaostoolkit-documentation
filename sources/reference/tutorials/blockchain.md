# Chaos Engineering experiments against a blockchain

!!! important "Credits"

    This article has been authored by
    [Yolanne Lee](http://linkedin.com/in/yolannelee) and you can find the
    original article code on Yolanne's
    [repository](https://github.com/yolannel/CTKBlockchain)


Blockchains are interesting concepts to test using chaos engineering principles.
This is because they operate based on user usage, taking advantage of a network
of participants and internal algorithms to create a distributed, decentralized
ledger.

This tutorial will _not_ focus on teaching core blockchain concepts. While the
setup may be done by simply pulling from my github repository, you may
alternatively invest some time reading through the great tutorial
[here](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)!

If you choose to proceed with the tutorial, you will need to ensure that your
HTTP requests match logically with those in this tutorial.

Ready? Great! Let's get started.

## Setup

First, clone the code using the command below in your command line. This fetches
an up-to-date version of all files required to run the experiment.

`$ git clone https://github.com/yolannel/CTKBlockchain`

Assuming you are running Python 3.6 or higher, you can install all required
dependencies via the following command in your command line. Please note that it
is highly recommended that you work inside of a virtual environment. A simple
explanation of virtual environments may be found
[here](https://docs.python.org/3/tutorial/venv.html); if you're running PyCharm
or another editor which has in-built venv support then check your project
settings!

`$ pip install -U -r requirements.txt`

Now you're all set up to dive into the experiments!

## Chaos Toolkit and Blockchain

### Looking forward

Blockchains are inherently user dependent which is why it presents a unique case
to test with Chaos Toolkit. This tutorial will guide you through the thought
process of creating two experiments:

1. Testing a simple transaction
2. Testing the consensus mechanism

We will follow the above order because the consensus mechanism naturally builds
off of the transaction model. If you require additional help at any point
regarding the CTK, you can view the
[documentation](https://docs.chaostoolkit.org/reference/api/experiment/).

You can consider an experiment as an **automator** for the process you'd
normally do to test your program: you preset a full task flow so that your
testing is repeatable and easy to run. The results of your experiment are also
automatically recorded, so you can continuously expose your system to stressors
and understand its strengths and weaknesses from reading the records which are
automatically recorded in your journal file.

### Transaction Experiment

We'll use this as an introduction to the CTK experiment as well. An experiment
is a single json file which tests a functionality of your program. It has
several components that _must_ be declared:

- `title`
  - This forces you to be organised with your experiments. The title should be
    clear for anyone reading it to understand what is being performed in the
    experiment.
- `description`
  - Similarly, a more detailed description which clarifies the experiment should
    be included. In my case, I use this property to describe the expected
    behaviour of the system so the tester knows right off the bat what is
    happening.
- `method`
  - This is where the majority of your work goes. More details are included
    below.

When we start to think about creating an experiment, we need to have a
well-defined goal of testing. For example, the blockchain should support making
a simple transaction which can be mined; before and after mining, the chain
should exist and be callable. No rollbacks should be supported since a
blockchain should be immutable.

This is the beginning of my experiment:

```json
{
    "title": "Can we make a new transaction?",
    "description": "The system should respond to a transaction request.",
    "tags": ["tx"],
    ...
```

The format of the json file is quite simple. Similarly to a dictionary, there is
a property, and a value assigned to the property. In the case of a property
which can take multiple values, such as `"tags"`, square brackets are put around
the values. Try adding an additional tag to the experiment by adding a comma
after the first value and adding a second tag!

Below, we see the ` "steady-state-hypothesis"`. We previously mentioned what the
blockchain should be capable of both before and after the experiment. The steady
state hypothesis tests for this condition - in this case, the condition is
simply that the chain should exist.

We also introduce a probe! This is the workhorse of any experiment. Probes are
able to carry out tests and listen for responses. They have the following
properties:

- `type`
  - REQUIRED. The type should always be set to `"probe"`
- `name`
  - REQUIRED. This is, again, for human readability. The name should describe
    what the probe does.
- `tolerance`
  - This takes a value or set of values that we can consider a 'good' response.
    Since my probe is an http request, the tolerance is set to the http status
    code corresponding to a successful call. You can see line 165 of
    blockchain.py that a successful chain GET request returns a status code
    of 200.
- `provider`
  - REQUIRED. This defines what type of probe is being asked for: `"python"`,
    `"http"` or `"process"`.
  - For a http probe, you must include an `"url"` property which is what you'd
    normally test with manually.
  - You may also include a `"timeout"` property which only considers a response
    successful (or within tolerance) if it is received within a certain
    timeframe. Units are in seconds.
- _Note that the probe is encapsulated within square brackets. You can define
  additional probes within the square brackets which are separated by commas._

```json
    "steady-state-hypothesis": {
        "title": "Chain exists",
        "probes": [
            {
                "type": "probe",
                "name": "chain-exists",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "timeout": 5,
                    "url": "http://127.0.0.1:5000/chain"
                }
            }
        ]
    },
```

Now we reach the main body of the json file, the method. The basic structure is
simply a list of probes and actions. Actions are very similar to probes, but
should introduce new information or a change to the system being tested rather
than simply checking its state.

As an example, checking that the chain exists is a probe but creating a new
transaction is an action.

We have to POST a request, which differs from the previous check-chain probe
which used a simple 'GET', so we define the `"method"` to be POST.

The `"header"` is a property which defines header names. These provide
information/context about the type of information being sent - in our case, the
content should be read as a json request so the header defines the content-type.

Certain arguments must be included (see line 173 in blockchain.py) in the json
for the request to be valid according to our blockchain.py file:

- `"sender"`
- `"recipient"`
- `"amount"`

We can include arguments in our action by simply including `"arguments"` and
listing them in name-value pairs.

```json
"method": [
        {
            "type": "action",
            "name": "make-new-transaction",
            "provider": {
                "type": "http",
                "timeout": 1,
                "url": "http://127.0.0.1:5000/transactions/new",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json"
                },
                "arguments": {
                    "sender": "me",
                    "recipient": "new-other-address",
                    "amount": 20
                }
            }
        },
        {
            "type": "probe",
            "name": "check-chain",
            "provider": {
                "type": "http",
                "url": "http://127.0.0.1:5000/mine"
            }
        },
        {
            "type": "action",
            "name": "mine-block",
            "provider": {
                "type": "http",
                "timeout": 3,
                "url": "http://127.0.0.1:5000/mine"
            }
        },
        {
            "type": "probe",
            "name": "check-chain",
            "provider": {
                "type": "http",
                "url": "http://127.0.0.1:5000/mine"
            }
        }
    ],
```

Finally, we reach the rollbacks! When designing an experiment, you should be
aware of the capabilities of your system and also what it _should_ be able to
do. For example, I could include code in my blockchain.py file that allows a
user to delete a transaction which hasn't been mined yet; however, this would
violate the operation of a blockchain because blockchains derive trust from
immutability (as mentioned before). So, you can see below that no rollbacks are
included because a user should not be able to delete changes nor does my
blockchain.py file include an option to.

```json
"rollbacks": [
    ]
}
```

#### Running the experiment

In your command line, you should create the blockchain before running the
experiment by running the blockchain.py file:

`$ python blockchain.py`

Then, you can run the experiment by using the command:

`$ chaos run testTransaction.json`

That's your first experiment!

### Consensus Experiment

While our blockchain is a very simple one, it should be able to demonstrate
arguably the key reason why we can call it 'decentralized' and 'distributed':
the consensus mechanism. As before, see the brilliant tutorial linked above if
you really want to get into the details!

On a topical level, the consensus mechanism is how you determine the global
truth. If one person posts a transaction on a block that was mined at the exact
same time, it could accidentally branch off of the original chain. Additionally,
there must be a verifiable task involved in mining that is unbiased and
sufficiently difficult, but still easy to check. Both of these requirements are
addressed by the consensus mechanism, which is the task required to mine a
block.

We will demo a simple Proof of Work, which essentially is an extremely difficult
computation to solve a math puzzle. We will then start a second chain as an
example of the branching that may occasionally occur; this blockchain resolves
itself by taking the longest chain.

We will not walk through the entire experiment this time, but the procedure
planned out is as follows.

1. Like before, we should ensure that the chain exist on two separate nodes.
2. Simulate activity.
3. Check the chains exist still.
4. Resolve the chains to identify the global truth.

Steps 1 and 3 should be familiar to you and I invite you to try coding them
yourself! Step 2 brings an opportunity to show another use case for CTK. So far
we have used the http provider, but we may also use a python provider.

```json
{
    "type": "action",
    "name": "simulate activity",
    "provider": {
        "type": "python",
        "module": "os",
            "func": "system",
            "arguments": {
                "command": "python -c \"import activity; activity.run(100)\""
            }
    }
}
```

- To make this experiment os-agnostic, we use python to run a python file
  through the os.system.
- `module`
  - This should be a Python module - in our case, we use the os module since it
    comes with the core Python libraries.
- `func`
  - This should be a function in the specified module that can be run.
- `arguments`
  - If a function takes arguments, check the documentation so you know how the
    arguments are titled and you can list them in the standard JSON format.
    Here, the argument is a command and the input is
    `'"python -c \"import activity; activity.run(100)\""`

The `activity.py` file run by simulate activity randomly posts transactions from
either of the two nodes and occasionally mines a block. For reference, the
approximate probability of posting a transaction to any of the two chains is 75%
and accordingly, the probability of mining from either of the two chains is 25%.

Finally, we want to resolve the chains. This is an http request which we've
learned earlier, and I again invite you to try your hand at it!

#### Running the experiment

In your command line, you should create the blockchain and start both nodes
(here we use 127.0.0.1:5000 and 127.0.0.1:5001) before running the experiment:

`$ python blockchain.py --port 5000`

.. and on a new terminal,

`$ python blockchain.py --port 5001`

Then, you can run the experiment by using the command:

`$ chaos run testConsensus.json`

You've completed the tutorial!

## Some key takeaways

- The http provider makes it simple to test user requests that are very common
  in web applications
- The Python provider is a very powerful tool that can run 'on its own' or other
  Python files
- The CTK at the core of it tests your system on what could possibly happen
  - This means it is _context specific_ - walking through this tutorial, you
    have seen how the experiments should be tailored to how the system should
    work, like how there are no rollback options.
- On an even more abstracted level, the CTK is an automation tool - note how the
  consensus test essentially automates a lot of usage and then checks. This
  actually makes it incredibly powerful even if you aren't specifically running
  a chaos experiment because there is a set process that you create which is
  replicable. Think of experiments as blueprints for what you want to try!

### Thanks

Chaos Toolkit is an open source project
[hosted on Github](https://github.com/chaostoolkit). If you have any issues then
raise them on the Github, and if you'd like to contribute, start
[here](https://docs.chaostoolkit.org/reference/contributing/)!

The
[blockchain tutorial](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
linked in the beginning is completely external to this tutorial and all credits
go to Daniel van Flymen.
