# Extension `chaosansible`

|                       |               |
| --------------------- | ------------- |
| **Version**           | IN_PROGESS |
| **Repository**        | https://github.com/Mickael-Roger/chaostoolkit-ansible |



[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-ansible.svg)](https://www.python.org/)


This project is a collection of [actions][] and [probes][], gathered as an extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[ansible]: https://www.ansible.com

***Please NOTE*** This extension is in the _early_ stages of development. Please feel free to create an issue in case of needed enhancement or misfunctioning.

---

<h1 align="center">
    <img src="docs/images/ansible.png" alt="Ansible Icon" width="470" height="200">
</h1>

---

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python environment where [chaostoolkit][] already lives.

```
pip install -U chaostoolkit-ansible
```

## Principles

This chaos toolkit driver provides you an easy way to execute probe and/or actions using ansible modules. By using it, you can execute tasks, gather facts, ... on remote systems

## Usage

### Basic

#### Probes 

To use the probes from this package, add the following to your experiment file:

In JSON:
```json
"steady-state-hypothesis": {
    "title": "Tests",
    "probes": [
        {
            "type": "probe",
            "name": "test-current-directory",
            "tolerance": {
              "type": "jsonpath",
              "path": "$.*.task",
              "expect": "/home/me"
            },
            "provider": {
                "type": "python",
                "module": "chaosansible.probes",
                "func": "chaosansible_probe",
                "arguments": {
                    "host_list": ["myserver1", "myserver2"],
                    "facts": "yes",
                    "ansible": {
                        "module": "shell",
                        "args": "pwd"
                    }
                }
            }
        }
    ]
}
```

In YAML:
```yaml
---
steady-state-hypothesis:
  title: The current working directory must be /home/me
  probes:
  - type: probe
    name: test-current-directory
    tolerance:
      type: jsonpath
      target: "$.*.task"
      pattern: /home/me
    provider:
      type: python
      module: chaosansible.probes
      func: chaosansible_probe
      arguments:
        host_list: ["myserver1", "myserver2"]
        facts: True
        ansible:
          module: shell
          args: pwd
```

That's it!

Probes can be gathered by using the stdout of an ansible task or through the ansible gather_facts module. Each time chaostoolkit-ansible runs, it returns a json that can be used in tolerance (using jsonpath, regex, ...)

This json is always formatted the same way (Example for a two targets host_list):

```json
{
  "target1": {
    "fact": " -> JSON result of the ansible gather_facts",
    "task": " -> String result containing the stdout value of the task result - Empty when ansible task do not return stdout"
  },
  "target2": {
    "fact": "...",
    "task": "..."
  }
}
```

#### Actions

To use the actions from this package, add the following to your experiment file:

In JSON:

```json
"method": [
    {
        "type": "action",
        "name": "delete-etc-hosts-file",
        "provider": {
            "type": "python",
            "module": "chaosansible.actions",
            "func": "chaosansible_run",
            "arguments": {
                "host_list": ["server1", "server2"],
                "become": true,
                "ansible": {
                    "module": "file",
                    "args": {
                        "path": "/etc/hosts",
                        "state": "absent"
                    }
                }
            }
        }
    }
]
```

In YAML:
```yaml
---
method:
- type: action
  name: delete-etc-hosts-file
  provider:
    type: python
    module: chaosansible.actions
    func: chaosansible_run
    arguments:
        host_list: ["server1", "server2"]
        become: True
        ansible:
          module: file
          args: 
            path: /etc/hosts
            state: absent
```


## Detailled usage

### Configuration block

The configuration block can be used to specify specific parameters to use. This block can be omit unless you really need to change default ansible parameters to run your experiment

Configuration variables that can be used by this driver are:

- **ansible_module_path**: Path of your ansible library
- **ansible_become_user**: Privileged user used when you call privilege escalation (root by default)
- **ansible_ssh_private_key**: Your ssh private key used to connect to targets (~/.ssh/id_rsa by default)
- **ansible_user**: User on target host used by ansible (current username by default)
- **become_ask_pass**: Password to escalate privileged when sudo needs one

In case you need to change one/or many default configuration(s), you can specify your value using the configuration block

***Please feel free to ask, if you need access to other ansible configuration parameters***

In JSON:

```json
"configuration": {
    "ansible_ssh_private_key": "/home/me/.ssh/mykey"
}
```

In YAML:
```yaml
configuration:
  ansible_ssh_private_key: "/home/me/.ssh/mykey"
```



### Arguments

chaosansible_run and chaosansible_probes use arguments (Most argument are classical ansible parameters):

| Argument | Type | Required | Default value | Description |
| --- | --- | --- | --- | --- |
| host_list | Array |  | localhost | List of host to use |
| facts | bool |  | false | Gather_facts |
| become | bool |  | false | Escalate privilege to run task |
| run_once | bool |  | false | Run the task only once on one target |
| num_target | str |  | all | "all" or "x" where x is an integer. Run the task to only x target among the host_list. Ideal to create random event |
| ansible | dict |  | {} | Execute ansible task. Cf ansible dict format. If ansible is not set, no task except ansible gather_facts (if facts set to True) |


Ansible dict format:

Classic ansible task are in the form:
```yaml
name: task name
ansible-module-name:
  module-parameter1: value1
  module-parameter2: value2
```

This is translate into chaos experiment file like this:
In JSON
```json
  "ansible": {
      "module": "ansible-module-name",
      "args": {
        "module-parameter1": "value1",
        "module-parameter2": "value2"
      }
  }
```

In YAML
```yaml
  ansible:
    module: ansible-module-name
    args:
      module-parameter1: value1
      module-parameter2: value2
```

Example with the ansible mount module (Umount a filesystem): 

In JSON
```json
  "ansible": {
      "module": "mount",
      "args": {
        "path": "/data",
        "state": "unmounted"
      }
  }
```

In YAML
```yaml
  ansible:
    module: mount
    args:
      path: /data
      state: unmounted
```

## Example of usage

### Delete /etc/hosts file on 2 random servers out of 5

In JSON
```json
"method": [
    {
        "type": "action",
        "name": "delete-etc-hosts-file",
        "provider": {
            "type": "python",
            "module": "chaosansible.actions",
            "func": "chaosansible_run",
            "arguments": {
                "host_list": ["server1","server2","server3","server4","server5"],
                "num_target": "2",
                "become": true,
                "ansible": {
                    "module": "file",
                    "args": {
                        "path": "/etc/hosts",
                        "state": "absent"
                    }
                }
            }
        }
    }
]
```

In YAML
```yaml
method:
- type: action
  name: delete-etc-hosts-file
  provider:
    type: python
    module: chaosansible.actions
    func: chaosansible_run
    arguments:
        host_list: ["server1","server2","server3","server4","server5"]
        become: True
        num_target: "2"
        ansible:
          module: file
          args: 
            path: /etc/hosts
            state: absent
```


### Run 100% cpu load on 3 server out of 5

In JSON
```json
"method": [
    {
        "type": "action",
        "name": "delete-etc-hosts-file",
        "provider": {
            "type": "python",
            "module": "chaosansible.actions",
            "func": "chaosansible_run",
            "arguments": {
                "host_list": ["server1","server2","server3","server4","server5"],
                "num_target": "3",
                "ansible": {
                    "module": "shell",
                    "args": {
                        "cmd": "stress-ng --cpu 0 --cpu-method matrixprod -t 60s",
                    }
                }
            }
        }
    }
]
```

In YAML
```yaml
method:
- type: action
  name: delete-etc-hosts-file
  provider:
    type: python
    module: chaosansible.actions
    func: chaosansible_run
    arguments:
        host_list: ["server1","server2","server3","server4","server5"]
        become: True
        num_target: "3"
        ansible:
          module: shell
          args: 
            cmd: stress-ng --cpu 0 --cpu-method matrixprod -t 60s
```


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
pytest
```





## Exported Activities



### actions



***

#### `chaosansible_run`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosansible.actions |
| **Name**              | chaosansible_run |
| **Return**              | None |


Run a task through ansible and eventually gather facts from host

**Signature:**

```python
def chaosansible_run(host_list: list = 'localhost',
                     configuration: Dict[str, Dict[str, str]] = None,
                     facts: bool = False,
                     become: bool = False,
                     run_once: bool = False,
                     ansible: dict = {},
                     num_target: str = 'all',
                     secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **host_list**      | list | "localhost" | No |
| **facts**      | boolean | false | No |
| **become**      | boolean | false | No |
| **run_once**      | boolean | false | No |
| **ansible**      | mapping | {} | No |
| **num_target**      | string | "all" | No |




**Usage:**

```json
{
  "name": "chaosansible-run",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosansible.actions",
    "func": "chaosansible_run"
  }
}
```

```yaml
name: chaosansible-run
provider:
  func: chaosansible_run
  module: chaosansible.actions
  type: python
type: action

```




### probes



***

#### `chaosansible_probe`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosansible.probes |
| **Name**              | chaosansible_probe |
| **Return**              | None |


Run a task through ansible and eventually gather facts from host

**Signature:**

```python
def chaosansible_probe(host_list: list = 'localhost',
                       configuration: Dict[str, Dict[str, str]] = None,
                       facts: bool = False,
                       become: bool = False,
                       run_once: bool = False,
                       ansible: dict = {},
                       num_target: str = 'all',
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **host_list**      | list | "localhost" | No |
| **facts**      | boolean | false | No |
| **become**      | boolean | false | No |
| **run_once**      | boolean | false | No |
| **ansible**      | mapping | {} | No |
| **num_target**      | string | "all" | No |




**Usage:**

```json
{
  "name": "chaosansible-probe",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosansible.probes",
    "func": "chaosansible_probe"
  }
}
```

```yaml
name: chaosansible-probe
provider:
  func: chaosansible_probe
  module: chaosansible.probes
  type: python
type: probe

```



