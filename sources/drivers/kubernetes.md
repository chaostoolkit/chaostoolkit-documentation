# Extension `chaosk8s`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.16.1 |
| **Repository**        | https://github.com/chaostoolkit/chaostoolkit-kubernetes |


[![Build Status](https://travis-ci.org/chaostoolkit/chaostoolkit-kubernetes.svg?branch=master)](https://travis-ci.org/chaostoolkit/chaostoolkit-kubernetes)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-kubernetes.svg)](https://www.python.org/)

This project contains activities, such as probes and actions, you can call from
your experiment through the Chaos Toolkit.

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-kubernetes
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "name": "all-our-microservices-should-be-healthy",
    "provider": {
        "type": "python",
        "module": "chaosk8s.probes",
        "func": "microservice_available_and_healthy",
        "arguments": {
            "name": "myapp",
            "ns": "myns"
        }
    }
},
{
    "type": "action",
    "name": "terminate-db-pod",
    "provider": {
        "type": "python",
        "module": "chaosk8s.pod.actions",
        "func": "terminate_pods",
        "arguments": {
            "label_selector": "app=my-app",
            "name_pattern": "my-app-[0-9]$",
            "rand": true,
            "ns": "default"
        }
    },
    "pauses": {
        "after": 5
    }
}
```

That's it! Notice how the action gives you the way to kill one pod randomly.

Please explore the code to see existing probes and actions.

### Discovery

You may use the Chaos Toolkit to discover the capabilities of this extension:

```
$ chaos discover chaostoolkit-kubernetes --no-install
```

## Configuration

This extension to the Chaos Toolkit can use the Kubernetes configuration 
found at the usual place in your HOME directory under `~/.kube/`, or, when
run from a Pod in a Kubernetes cluster, it will use the local service account.
In that case, make sure to set the `CHAOSTOOLKIT_IN_POD` environment variable
to `"true"`.

You can also pass the credentials via secrets as follows:

```json
{
    "secrets": {
        "kubernetes": {
            "KUBERNETES_HOST": "http://somehost",
            "KUBERNETES_API_KEY": {
                "type": "env",
                "key": "SOME_ENV_VAR"
            }
        }
    }
}
```

Then in your probe or action:

```json
{
    "name": "all-our-microservices-should-be-healthy",
    "provider": {
        "type": "python",
        "module": "chaosk8s.probes",
        "func": "microservice_available_and_healthy",
        "secrets": ["kubernetes"],
        "arguments": {
            "name": "myapp",
            "ns": "myns"
        }
    }
}
```

You may specify the Kubernetes context you want to use as follows:

```json
{
    "secrets": {
        "kubernetes": {
            "KUBERNETES_CONTEXT": "minikube"
        }
    }
}
```

Or via the environment:

```
$ export KUBERNETES_CONTEXT=minikube
```

In the same spirit, you can specify where to find your Kubernetes configuration
with:

```
$ export KUBECONFIG=some/path/config
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please fork this project, make your changes following the
usual [PEP 8][pep8] code style, add appropriate tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

## Exported Activities



### actions



***

#### `kill_microservice`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.actions |
| **Name**              | kill_microservice |
| **Return**              | None |


Kill a microservice by `name` in the namespace `ns`.

The microservice is killed by deleting the deployment for it without
a graceful period to trigger an abrupt termination.

The selected resources are matched by the given `label_selector`.

**Signature:**

```python
def kill_microservice(name: str,
                      ns: str = 'default',
                      label_selector: str = 'name in ({name})',
                      secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | "name in ({name})" | No |


**Usage:**

```json
{
  "name": "kill-microservice",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.actions",
    "func": "kill_microservice",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: kill-microservice
provider:
  arguments:
    name: ''
  func: kill_microservice
  module: chaosk8s.actions
  type: python
type: action

```



***

#### `remove_service_endpoint`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.actions |
| **Name**              | remove_service_endpoint |
| **Return**              | None |


Remove the service endpoint that sits in front of microservices (pods).

**Signature:**

```python
def remove_service_endpoint(name: str,
                            ns: str = 'default',
                            secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "remove-service-endpoint",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.actions",
    "func": "remove_service_endpoint",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: remove-service-endpoint
provider:
  arguments:
    name: ''
  func: remove_service_endpoint
  module: chaosk8s.actions
  type: python
type: action

```



***

#### `scale_microservice`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.actions |
| **Name**              | scale_microservice |
| **Return**              | None |


Scale a deployment up or down. The `name` is the name of the deployment.

**Signature:**

```python
def scale_microservice(name: str,
                       replicas: int,
                       ns: str = 'default',
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **replicas**      | integer |  | Yes |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "scale-microservice",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.actions",
    "func": "scale_microservice",
    "arguments": {
      "name": "",
      "replicas": 0
    }
  }
}
```

```yaml
name: scale-microservice
provider:
  arguments:
    name: ''
    replicas: 0
  func: scale_microservice
  module: chaosk8s.actions
  type: python
type: action

```



***

#### `start_microservice`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.actions |
| **Name**              | start_microservice |
| **Return**              | None |


Start a microservice described by the deployment config, which must be the
path to the JSON or YAML representation of the deployment.

**Signature:**

```python
def start_microservice(spec_path: str,
                       ns: str = 'default',
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **spec_path**      | string |  | Yes |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "start-microservice",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.actions",
    "func": "start_microservice",
    "arguments": {
      "spec_path": ""
    }
  }
}
```

```yaml
name: start-microservice
provider:
  arguments:
    spec_path: ''
  func: start_microservice
  module: chaosk8s.actions
  type: python
type: action

```




### node



***

#### `cordon_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.node.actions |
| **Name**              | cordon_node |
| **Return**              | None |


Cordon nodes matching the given label or name, so that no pods
are scheduled on them any longer.

**Signature:**

```python
def cordon_node(name: str = None,
                label_selector: str = None,
                secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **label_selector**      | string | null | No |


**Usage:**

```json
{
  "name": "cordon-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.node.actions",
    "func": "cordon_node"
  }
}
```

```yaml
name: cordon-node
provider:
  func: cordon_node
  module: chaosk8s.node.actions
  type: python
type: action

```



***

#### `create_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.node.actions |
| **Name**              | create_node |
| **Return**              | kubernetes.client.models.v1_node.V1Node |


Create one new node in the cluster.

Due to the way things work on certain cloud providers, you won't be able
to use this meaningfully on them. For instance on GCE, this will likely
fail.

See also: https://github.com/kubernetes/community/blob/master/contributors/devel/api-conventions.md#idempotency

**Signature:**

```python
def create_node(meta: Dict[str, Any] = None,
                spec: Dict[str, Any] = None,
                secrets: Dict[str, Dict[str, str]] = None
                ) -> kubernetes.client.models.v1_node.V1Node:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **meta**      | mapping | null | No |
| **spec**      | mapping | null | No |


**Usage:**

```json
{
  "name": "create-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.node.actions",
    "func": "create_node"
  }
}
```

```yaml
name: create-node
provider:
  func: create_node
  module: chaosk8s.node.actions
  type: python
type: action

```



***

#### `delete_nodes`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.node.actions |
| **Name**              | delete_nodes |
| **Return**              | None |


Delete nodes gracefully. Select the appropriate nodes by label.

Nodes are not drained beforehand so we can see how cluster behaves. Nodes
cannot be restarted, they are really deleted. Please be careful when using
this action.

On certain cloud providers, you also need to delete the underneath VM
instance as well afterwards. This is the case on GCE for instance.

If `all` is set to `True`, all nodes will be terminated.
If `rand` is set to `True`, one random node will be terminated.
If ̀`count` is set to a positive number, only a upto `count` nodes
(randomly picked) will be terminated. Otherwise, the first retrieved node
will be terminated.

**Signature:**

```python
def delete_nodes(label_selector: str = None,
                 all: bool = False,
                 rand: bool = False,
                 count: int = None,
                 grace_period_seconds: int = None,
                 secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string | null | No |
| **all**      | boolean | false | No |
| **rand**      | boolean | false | No |
| **count**      | integer | null | No |
| **grace_period_seconds**      | integer | null | No |


**Usage:**

```json
{
  "name": "delete-nodes",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.node.actions",
    "func": "delete_nodes"
  }
}
```

```yaml
name: delete-nodes
provider:
  func: delete_nodes
  module: chaosk8s.node.actions
  type: python
type: action

```



***

#### `drain_nodes`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.node.actions |
| **Name**              | drain_nodes |
| **Return**              | boolean |


Drain nodes matching the given label or name, so that no pods are scheduled
on them any longer and running pods are evicted.

It does a similar job to `kubectl drain --ignore-daemonsets` or
`kubectl drain --delete-local-data --ignore-daemonsets` if
`delete_pods_with_local_storage` is set to `True`. There is no
equivalent to the `kubectl drain --force` flag.

You probably want to call `uncordon` from in your experiment's rollbacks.

**Signature:**

```python
def drain_nodes(name: str = None,
                label_selector: str = None,
                delete_pods_with_local_storage: bool = False,
                timeout: int = 120,
                secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **label_selector**      | string | null | No |
| **delete_pods_with_local_storage**      | boolean | false | No |
| **timeout**      | integer | 120 | No |


**Usage:**

```json
{
  "name": "drain-nodes",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.node.actions",
    "func": "drain_nodes"
  }
}
```

```yaml
name: drain-nodes
provider:
  func: drain_nodes
  module: chaosk8s.node.actions
  type: python
type: action

```



***

#### `uncordon_node`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.node.actions |
| **Name**              | uncordon_node |
| **Return**              | None |


Uncordon nodes matching the given label name, so that pods can be
scheduled on them again.

**Signature:**

```python
def uncordon_node(name: str = None,
                  label_selector: str = None,
                  secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **label_selector**      | string | null | No |


**Usage:**

```json
{
  "name": "uncordon-node",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.node.actions",
    "func": "uncordon_node"
  }
}
```

```yaml
name: uncordon-node
provider:
  func: uncordon_node
  module: chaosk8s.node.actions
  type: python
type: action

```




### pod



***

#### `count_pods`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | count_pods |
| **Return**              | integer |


Count the number of pods matching the given selector in a given `phase`, if
one is given.

**Signature:**

```python
def count_pods(label_selector: str,
               phase: str = None,
               ns: str = 'default',
               secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string |  | Yes |
| **phase**      | string | null | No |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "count-pods",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.probes",
    "func": "count_pods",
    "arguments": {
      "label_selector": ""
    }
  }
}
```

```yaml
name: count-pods
provider:
  arguments:
    label_selector: ''
  func: count_pods
  module: chaosk8s.pod.probes
  type: python
type: probe

```



***

#### `pods_in_phase`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | pods_in_phase |
| **Return**              | boolean |


Lookup a pod by `label_selector` in the namespace `ns`.

Raises :exc:`chaoslib.exceptions.FailedActivity` when the state is not
as expected.

**Signature:**

```python
def pods_in_phase(label_selector: str,
                  phase: str = 'Running',
                  ns: str = 'default',
                  secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string |  | Yes |
| **phase**      | string | "Running" | No |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "pods-in-phase",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.probes",
    "func": "pods_in_phase",
    "arguments": {
      "label_selector": ""
    }
  }
}
```

```yaml
name: pods-in-phase
provider:
  arguments:
    label_selector: ''
  func: pods_in_phase
  module: chaosk8s.pod.probes
  type: python
type: probe

```



***

#### `pods_not_in_phase`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | pods_not_in_phase |
| **Return**              | boolean |


Lookup a pod by `label_selector` in the namespace `ns`.

Raises :exc:`chaoslib.exceptions.FailedActivity` when the pod is in the
given phase and should not have.

**Signature:**

```python
def pods_not_in_phase(label_selector: str,
                      phase: str = 'Running',
                      ns: str = 'default',
                      secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string |  | Yes |
| **phase**      | string | "Running" | No |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "pods-not-in-phase",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.probes",
    "func": "pods_not_in_phase",
    "arguments": {
      "label_selector": ""
    }
  }
}
```

```yaml
name: pods-not-in-phase
provider:
  arguments:
    label_selector: ''
  func: pods_not_in_phase
  module: chaosk8s.pod.probes
  type: python
type: probe

```



***

#### `read_pod_logs`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | read_pod_logs |
| **Return**              | mapping |


Fetch logs for all the pods with the label `"name"` set to `name` and
return a dictionary with the keys being the pod's name and the values
the logs of said pod. If `name` is not provided, use only the
`label_selector` instead.

When your pod has several containers, you should also set `container_name`
to clarify which container you want to read logs from.

If you provide `last`, this returns the logs of the last N seconds
until now. This can set to a fluent delta such as `10 minutes`.

You may also set `from_previous` to `True` to capture the logs of a
previous pod's incarnation, if any.

**Signature:**

```python
def read_pod_logs(name: str = None,
                  last: Union[str, NoneType] = None,
                  ns: str = 'default',
                  from_previous: bool = False,
                  label_selector: str = 'name in ({name})',
                  container_name: str = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, str]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **last**      | object | null | No |
| **ns**      | string | "default" | No |
| **from_previous**      | boolean | false | No |
| **label_selector**      | string | "name in ({name})" | No |
| **container_name**      | string | null | No |


**Usage:**

```json
{
  "name": "read-pod-logs",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.probes",
    "func": "read_pod_logs"
  }
}
```

```yaml
name: read-pod-logs
provider:
  func: read_pod_logs
  module: chaosk8s.pod.probes
  type: python
type: probe

```



***

#### `terminate_pods`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.pod.actions |
| **Name**              | terminate_pods |
| **Return**              | None |


Terminate a pod gracefully. Select the appropriate pods by label and/or
name patterns. Whenever a pattern is provided for the name, all pods
retrieved will be filtered out if their name do not match the given
pattern.

If neither `label_selector` nor `name_pattern` are provided, all pods
in the namespace will be terminated.

If `all` is set to `True`, all matching pods will be terminated.
If `rand` is set to `True`, one random pod will be terminated.
Otherwise, the first retrieved pod will be terminated.

**Signature:**

```python
def terminate_pods(label_selector: str = None,
                   name_pattern: str = None,
                   all: bool = False,
                   rand: bool = False,
                   ns: str = 'default',
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string | null | No |
| **name_pattern**      | string | null | No |
| **all**      | boolean | false | No |
| **rand**      | boolean | false | No |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "terminate-pods",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.actions",
    "func": "terminate_pods"
  }
}
```

```yaml
name: terminate-pods
provider:
  func: terminate_pods
  module: chaosk8s.pod.actions
  type: python
type: action

```




### probes



***

#### `all_microservices_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | all_microservices_healthy |
| **Return**              | Tuple[Dict[str, Any], Dict[str, Any]] |


Check all microservices in the system are running and available.

Raises :exc:`chaoslib.exceptions.FailedActivity` when the state is not
as expected.

**Signature:**

```python
def all_microservices_healthy(ns: str = 'default',
                              secrets: Dict[str, Dict[str, str]] = None
                              ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **ns**      | string | "default" | No |


**Usage:**

```json
{
  "name": "all-microservices-healthy",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "all_microservices_healthy"
  }
}
```

```yaml
name: all-microservices-healthy
provider:
  func: all_microservices_healthy
  module: chaosk8s.probes
  type: python
type: probe

```



***

#### `deployment_is_not_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | deployment_is_not_fully_available |
| **Return**              | None |


Wait until the deployment gets into an intermediate state where not all
expected replicas are available. Once this state is reached, return `True`.
If the state is not reached after `timeout` seconds, a
:exc:`chaoslib.exceptions.FailedActivity` exception is raised.

**Signature:**

```python
def deployment_is_not_fully_available(
        name: str,
        ns: str = 'default',
        label_selector: str = 'name in ({name})',
        timeout: int = 30,
        secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | "name in ({name})" | No |
| **timeout**      | integer | 30 | No |


**Usage:**

```json
{
  "name": "deployment-is-not-fully-available",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "deployment_is_not_fully_available",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: deployment-is-not-fully-available
provider:
  arguments:
    name: ''
  func: deployment_is_not_fully_available
  module: chaosk8s.probes
  type: python
type: probe

```



***

#### `microservice_available_and_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | microservice_available_and_healthy |
| **Return**              | Union[bool, NoneType] |


Lookup a deployment by `name` in the namespace `ns`.

The selected resources are matched by the given `label_selector`.

Raises :exc:`chaoslib.exceptions.FailedActivity` when the state is not
as expected.

**Signature:**

```python
def microservice_available_and_healthy(
        name: str,
        ns: str = 'default',
        label_selector: str = 'name in ({name})',
        secrets: Dict[str, Dict[str, str]] = None) -> Union[bool, NoneType]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | "name in ({name})" | No |


**Usage:**

```json
{
  "name": "microservice-available-and-healthy",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "microservice_available_and_healthy",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: microservice-available-and-healthy
provider:
  arguments:
    name: ''
  func: microservice_available_and_healthy
  module: chaosk8s.probes
  type: python
type: probe

```



***

#### `microservice_is_not_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | microservice_is_not_available |
| **Return**              | boolean |


Lookup pods with a `name` label set to the given `name` in the specified
`ns`.

Raises :exc:`chaoslib.exceptions.FailedActivity` when one of the pods
with the specified `name` is in the `"Running"` phase.

**Signature:**

```python
def microservice_is_not_available(
        name: str,
        ns: str = 'default',
        label_selector: str = 'name in ({name})',
        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | "name in ({name})" | No |


**Usage:**

```json
{
  "name": "microservice-is-not-available",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "microservice_is_not_available",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: microservice-is-not-available
provider:
  arguments:
    name: ''
  func: microservice_is_not_available
  module: chaosk8s.probes
  type: python
type: probe

```



***

#### `read_microservices_logs`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | read_microservices_logs |
| **Return**              | mapping |


Fetch logs for all the pods with the label `"name"` set to `name` and
return a dictionary with the keys being the pod's name and the values
the logs of said pod. If `name` is not provided, use only the
`label_selector` instead.

When your pod has several containers, you should also set `container_name`
to clarify which container you want to read logs from.

If you provide `last`, this returns the logs of the last N seconds
until now. This can set to a fluent delta such as `10 minutes`.

You may also set `from_previous` to `True` to capture the logs of a
previous pod's incarnation, if any.

**Signature:**

```python
def read_microservices_logs(
        name: str = None,
        last: Union[str, NoneType] = None,
        ns: str = 'default',
        from_previous: bool = False,
        label_selector: str = 'name in ({name})',
        container_name: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, str]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **last**      | object | null | No |
| **ns**      | string | "default" | No |
| **from_previous**      | boolean | false | No |
| **label_selector**      | string | "name in ({name})" | No |
| **container_name**      | string | null | No |


**Usage:**

```json
{
  "name": "read-microservices-logs",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "read_microservices_logs"
  }
}
```

```yaml
name: read-microservices-logs
provider:
  func: read_microservices_logs
  module: chaosk8s.probes
  type: python
type: probe

```



***

#### `service_endpoint_is_initialized`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | service_endpoint_is_initialized |
| **Return**              | None |


Lookup a service endpoint by its name and raises :exc:`FailedProbe` when
the service was not found or not initialized.

**Signature:**

```python
def service_endpoint_is_initialized(name: str,
                                    ns: str = 'default',
                                    label_selector: str = 'name in ({name})',
                                    secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | "name in ({name})" | No |


**Usage:**

```json
{
  "name": "service-endpoint-is-initialized",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosk8s.probes",
    "func": "service_endpoint_is_initialized",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: service-endpoint-is-initialized
provider:
  arguments:
    name: ''
  func: service_endpoint_is_initialized
  module: chaosk8s.probes
  type: python
type: probe

```


