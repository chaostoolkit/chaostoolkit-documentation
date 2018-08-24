# Extension `chaosaws`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.5.2 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-aws |

N/A

## Exported Activities



### ec2



***

#### `describe_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ec2.probes |
| **Name**              | describe_instances |
| **Return**              | mapping |


Describe instances following the specified filters.

Please refer to http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_instances
for details on said filters.

**Signature:**

```python
def describe_instances(
        filters: List[Dict[str, Any]],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filters**      | list |  | Yes |


**Usage:**

```json
{
  "name": "describe-instances",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.ec2.probes",
    "func": "describe_instances",
    "arguments": {
      "filters": []
    }
  }
}
```

```yaml
name: describe-instances
provider:
  arguments:
    filters: []
  func: describe_instances
  module: chaosaws.ec2.probes
  type: python
type: probe

```



***

#### `stop_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | stop_instance |
| **Return**              | mapping |


Stop a single EC2 instance.

You may provide an instance id explicitly or, if you only specify the AZ,
a random instance will be selected.

**Signature:**

```python
def stop_instance(instance_id: str = None,
                  az: str = None,
                  force: bool = False,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **az**      | string | null | No |
| **force**      | boolean | false | No |


**Usage:**

```json
{
  "name": "stop-instance",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ec2.actions",
    "func": "stop_instance"
  }
}
```

```yaml
name: stop-instance
provider:
  func: stop_instance
  module: chaosaws.ec2.actions
  type: python
type: action

```



***

#### `stop_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | stop_instances |
| **Return**              | mapping |


Stop the given EC2 instances or, if none is provided, all instances
of the given availability zone.

**Signature:**

```python
def stop_instances(
        instance_ids: List[str] = None,
        az: str = None,
        force: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **force**      | boolean | false | No |


**Usage:**

```json
{
  "name": "stop-instances",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ec2.actions",
    "func": "stop_instances"
  }
}
```

```yaml
name: stop-instances
provider:
  func: stop_instances
  module: chaosaws.ec2.actions
  type: python
type: action

```




### ecs



***

#### `are_all_desired_tasks_running`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ecs.probes |
| **Name**              | are_all_desired_tasks_running |
| **Return**              | boolean |


Checks to make sure desired and running tasks counts are equal

**Signature:**

```python
def are_all_desired_tasks_running(
        cluster: str,
        service: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |


**Usage:**

```json
{
  "name": "are-all-desired-tasks-running",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.probes",
    "func": "are_all_desired_tasks_running",
    "arguments": {
      "cluster": "",
      "service": ""
    }
  }
}
```

```yaml
name: are-all-desired-tasks-running
provider:
  arguments:
    cluster: ''
    service: ''
  func: are_all_desired_tasks_running
  module: chaosaws.ecs.probes
  type: python
type: probe

```



***

#### `delete_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | delete_cluster |
| **Return**              | mapping |


Delete a given ECS cluster

**Signature:**

```python
def delete_cluster(
        cluster: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |


**Usage:**

```json
{
  "name": "delete-cluster",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "delete_cluster",
    "arguments": {
      "cluster": ""
    }
  }
}
```

```yaml
name: delete-cluster
provider:
  arguments:
    cluster: ''
  func: delete_cluster
  module: chaosaws.ecs.actions
  type: python
type: action

```



***

#### `delete_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | delete_service |
| **Return**              | mapping |


Update a given ECS service by updating it to set the desired count of tasks
to 0 then delete it. If not provided, a random one will be picked up
regarding `service_pattern`, if provided, so that only service names
matching the pattern would be be used. This should be a valid regex.

You can specify a cluster by its ARN identifier or, if not provided, the
default cluster will be picked up.

**Signature:**

```python
def delete_service(
        service: str = None,
        cluster: str = None,
        service_pattern: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **service**      | string | null | No |
| **cluster**      | string | null | No |
| **service_pattern**      | string | null | No |


**Usage:**

```json
{
  "name": "delete-service",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "delete_service"
  }
}
```

```yaml
name: delete-service
provider:
  func: delete_service
  module: chaosaws.ecs.actions
  type: python
type: action

```



***

#### `deregister_container_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | deregister_container_instance |
| **Return**              | mapping |


Deregister a given ECS container. Be careful that tasks handled by this
instance will remain orphan.

**Signature:**

```python
def deregister_container_instance(
        cluster: str,
        instance_id: str,
        force: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **instance_id**      | string |  | Yes |
| **force**      | boolean | false | No |


**Usage:**

```json
{
  "name": "deregister-container-instance",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "deregister_container_instance",
    "arguments": {
      "cluster": "",
      "instance_id": ""
    }
  }
}
```

```yaml
name: deregister-container-instance
provider:
  arguments:
    cluster: ''
    instance_id: ''
  func: deregister_container_instance
  module: chaosaws.ecs.actions
  type: python
type: action

```



***

#### `service_is_deploying`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ecs.probes |
| **Name**              | service_is_deploying |
| **Return**              | boolean |


Checks to make sure there is not an in progress deployment

**Signature:**

```python
def service_is_deploying(cluster: str,
                         service: str,
                         configuration: Dict[str, Dict[str, str]] = None,
                         secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |


**Usage:**

```json
{
  "name": "service-is-deploying",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.probes",
    "func": "service_is_deploying",
    "arguments": {
      "cluster": "",
      "service": ""
    }
  }
}
```

```yaml
name: service-is-deploying
provider:
  arguments:
    cluster: ''
    service: ''
  func: service_is_deploying
  module: chaosaws.ecs.probes
  type: python
type: probe

```



***

#### `stop_task`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | stop_task |
| **Return**              | mapping |


Stop a given ECS task instance. If no task_id provided, a random task of
the given service is stopped.

You can specify a cluster by its ARN identifier or, if not provided, the
default cluster will be picked up.

**Signature:**

```python
def stop_task(cluster: str = None,
              task_id: str = None,
              service: str = None,
              reason: str = 'Chaos Testing',
              configuration: Dict[str, Dict[str, str]] = None,
              secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string | null | No |
| **task_id**      | string | null | No |
| **service**      | string | null | No |
| **reason**      | string | "Chaos Testing" | No |


**Usage:**

```json
{
  "name": "stop-task",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "stop_task"
  }
}
```

```yaml
name: stop-task
provider:
  func: stop_task
  module: chaosaws.ecs.actions
  type: python
type: action

```




### eks



***

#### `create_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.eks.actions |
| **Name**              | create_cluster |
| **Return**              | mapping |


Create a new EKS cluster.

**Signature:**

```python
def create_cluster(
        name: str,
        role_arn: str,
        vpc_config: Dict[str, Any],
        version: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **role_arn**      | string |  | Yes |
| **vpc_config**      | mapping |  | Yes |
| **version**      | string | null | No |


**Usage:**

```json
{
  "name": "create-cluster",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.eks.actions",
    "func": "create_cluster",
    "arguments": {
      "name": "",
      "role_arn": "",
      "vpc_config": {}
    }
  }
}
```

```yaml
name: create-cluster
provider:
  arguments:
    name: ''
    role_arn: ''
    vpc_config: {}
  func: create_cluster
  module: chaosaws.eks.actions
  type: python
type: action

```



***

#### `delete_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.eks.actions |
| **Name**              | delete_cluster |
| **Return**              | mapping |


Delete the given EKS cluster.

**Signature:**

```python
def delete_cluster(
        name: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |


**Usage:**

```json
{
  "name": "delete-cluster",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.eks.actions",
    "func": "delete_cluster"
  }
}
```

```yaml
name: delete-cluster
provider:
  func: delete_cluster
  module: chaosaws.eks.actions
  type: python
type: action

```



***

#### `describe_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.eks.probes |
| **Name**              | describe_cluster |
| **Return**              | mapping |


Describe an EKS cluster.

**Signature:**

```python
def describe_cluster(
        name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |


**Usage:**

```json
{
  "name": "describe-cluster",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.eks.probes",
    "func": "describe_cluster",
    "arguments": {
      "name": ""
    }
  }
}
```

```yaml
name: describe-cluster
provider:
  arguments:
    name: ''
  func: describe_cluster
  module: chaosaws.eks.probes
  type: python
type: probe

```



***

#### `list_clusters`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.eks.probes |
| **Name**              | list_clusters |
| **Return**              | mapping |


List EKS clusters available to the authenticated account.

**Signature:**

```python
def list_clusters(configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |


**Usage:**

```json
{
  "name": "list-clusters",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.eks.probes",
    "func": "list_clusters"
  }
}
```

```yaml
name: list-clusters
provider:
  func: list_clusters
  module: chaosaws.eks.probes
  type: python
type: probe

```




### iam



***

#### `attach_role_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.iam.actions |
| **Name**              | attach_role_policy |
| **Return**              | mapping |


Attach a role to a policy.

**Signature:**

```python
def attach_role_policy(
        arn: str,
        role_name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **arn**      | string |  | Yes |
| **role_name**      | string |  | Yes |


**Usage:**

```json
{
  "name": "attach-role-policy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.iam.actions",
    "func": "attach_role_policy",
    "arguments": {
      "arn": "",
      "role_name": ""
    }
  }
}
```

```yaml
name: attach-role-policy
provider:
  arguments:
    arn: ''
    role_name: ''
  func: attach_role_policy
  module: chaosaws.iam.actions
  type: python
type: action

```



***

#### `create_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.iam.actions |
| **Name**              | create_policy |
| **Return**              | mapping |


Create a new IAM policy

**Signature:**

```python
def create_policy(name: str,
                  policy: Dict[str, Any],
                  path: str = '/',
                  description: str = '',
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **policy**      | mapping |  | Yes |
| **path**      | string | "/" | No |
| **description**      | string | "" | No |


**Usage:**

```json
{
  "name": "create-policy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.iam.actions",
    "func": "create_policy",
    "arguments": {
      "name": "",
      "policy": {}
    }
  }
}
```

```yaml
name: create-policy
provider:
  arguments:
    name: ''
    policy: {}
  func: create_policy
  module: chaosaws.iam.actions
  type: python
type: action

```



***

#### `detach_role_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.iam.actions |
| **Name**              | detach_role_policy |
| **Return**              | mapping |


Detach a role from a policy.

**Signature:**

```python
def detach_role_policy(
        arn: str,
        role_name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **arn**      | string |  | Yes |
| **role_name**      | string |  | Yes |


**Usage:**

```json
{
  "name": "detach-role-policy",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.iam.actions",
    "func": "detach_role_policy",
    "arguments": {
      "arn": "",
      "role_name": ""
    }
  }
}
```

```yaml
name: detach-role-policy
provider:
  arguments:
    arn: ''
    role_name: ''
  func: detach_role_policy
  module: chaosaws.iam.actions
  type: python
type: action

```



***

#### `get_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.iam.probes |
| **Name**              | get_policy |
| **Return**              | boolean |


Get a policy by its ARN

**Signature:**

```python
def get_policy(arn: str,
               configuration: Dict[str, Dict[str, str]] = None,
               secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **arn**      | string |  | Yes |


**Usage:**

```json
{
  "name": "get-policy",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosaws.iam.probes",
    "func": "get_policy",
    "arguments": {
      "arn": ""
    }
  }
}
```

```yaml
name: get-policy
provider:
  arguments:
    arn: ''
  func: get_policy
  module: chaosaws.iam.probes
  type: python
type: probe

```


