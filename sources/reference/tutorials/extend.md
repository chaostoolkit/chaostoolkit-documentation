# Learn the basic of extending the Chaos Toolkit

The Chaos Toolkit comes with a rich catalog of extensions. Sometimes however,
this library is not enough. So, how do you go about extending the Chaos Toolkit?

It turns out there are a variety of ways.

## Generate a binary and execute it from the experiment

The Chaos Toolkit is written in Python 3, but you may not have the Python
skills or willingness to develop it. One quick solution is to write your own
small binary (say you are a rust or golang shop) and call it as a `process`
action. Keep in mind that the binary may be used as a probe in the steady-state
so ensure its returned value is easily processed via regex or jsonpath
tolerance types. At the very least, the process should signal through its
exit code if it completed normally (with 0).

## Call a HTTP endpoint

Sometimes, you have HTTP endpoints that are used internally for specific
operational tasks. They are internals and crafted for your unique needs. This
can be enough to create the bespoke condition for your probes and actions to
call via a `http` provider.

## Create a simple Python function

While extending with a piece of Python code may sound more work, it does not
have to be. Indeed, you can create a simple Python module and have a set of
functions that are called from your experiment directly. THe trick is to
ensure the module can be found in the [PYTHONPATH][].

[PYTHONPATH]: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH

Let's see an example:

Assuming a Python module called `kettle.py`:

```python
from chaoslib.types import Configuration, Secrets

__all__ = ["put_on"]


def put_on(temperature: int = 90, configuration: Configuration = None,
           secrets: Secrets = None) -> None:
    """
    Sets the kettle to the expected temperature (celcius) and put it on.

    Will return when the kettle has reached it.
    """
    # do something here
    pass
```

If `kettle.py` lives next to `experiment.json` then the action could be:


```json
{
    "name": "put-kettle-on",
    "type": "action",
    "provider": {
        "type": "python",
        "module": "kettle",
        "func": "put_on",
        "arguments": {
            "temperature": 80
        }
    }
}
```

You could finally make it available as follows:

```console
$ ls
kettle.py experiment.json
$ export PYTHONPATH=`pwd`
$ chaos run nexperiment.json
```
