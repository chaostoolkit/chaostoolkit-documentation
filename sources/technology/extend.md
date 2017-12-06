## Extend

### Overview

Experiments are declared in JSON-encoded files. Probes and actions describe
what should be executed by the Chaos Toolkit.

The ChaosToolkit does not implement probes and actions natively. Instead,
it supports three extension mechanisms:

* Python function
* Process
* HTTP

In the future, other providers will likely be added such as [FaaS][faas].

[faas]:https://en.wikipedia.org/wiki/Function_as_a_service

### Python function

You can implement a probe or action as a Python function. In that case, you
can use any Python package your activity needs. The structure for a Python
function is as follows:

```json
{
    "provider": {
        "type": "python",
        "module": "os.path",
        "func": "exists",
        "arguments": {
            "path": "/some/path"
        }
    }
}
```

The `type="python"` entry informs the Chaos Toolkit this is a Python function
activity. The `module` should be found in the Python path of the Chaos Toolkit
process (its virtual environment usually). Make sure the `func` belongs to
a package that has been installed prior to running the command the toolkit will
not attempt to fetch it.

The `arguments` object is a mapping of keys to string values that will be 
passed as-is to the function arguments. If they do not match, the Chaos Toolkit
will raise an error.

### Process

The Chaos Toolkit can run external processes, found in the PATH. The structure
for a process is as follows:

```json
{
    "provider": {
        "type": "process",
        "path": "/sbin/ip",
        "arguments": {
            "-a": null
        }
    }
}
```

The `type="process"` entry informs the Chaos Toolkit this is a process activity.
The `path` indicates the executable to run. Either an absolute path or a command
to be found in the PATH. The user running the Chaos Toolkit must have the 
permissions to execute the command.

The `arguments` object is a mapping of keys to string values that will be 
passed as-is to the process as arguments.

You can provide a `timeout` to interrupt the command at some point, in that case
the activity will be considered failed.

### HTTP

The Chaos Toolkit can call HTTP endpoints.The structure for a HTTP call is as
follows:

```json
{
    "provider": {
        "type": "http",
        "url": "http://httpbin.org/post",
        "method": "POST",
        "headers": {
            "accept": "application/json"
        },
        "arguments": {
            "name": "john" 
        }
    }
}
```

The `type="http"` entry informs the Chaos Toolkit this is a HTTP activity.
The `url` is the only required key and indicates the endpoint to talk to. You
can pass `headers` as well and specify the HTTP `method` to be used.

The `arguments` object is a mapping of keys to string values that will be 
passed as-is to the process as arguments.

You can provide a `timeout` to interrupt the command at some point, in that case
the activity will be considered failed.

Let's now remember, 