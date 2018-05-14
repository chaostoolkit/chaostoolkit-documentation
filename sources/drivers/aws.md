# Extension `chaosaws`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.4.2 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-aws |


[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-aws.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-aws)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-aws.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-aws
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "name": "stop-an-ec2-instance",
    "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "stop_instance",
        "arguments": {
            "instance_id": "i-123456"
        }
    }
},
{
    "name": "create-a-new-policy",
    "provider": {
        "type": "python",
        "module": "chaosaws.iam.actions",
        "func": "create_policy",
        "arguments": {
            "name": "mypolicy",
            "path": "user/Jane",
            "policy": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "s3:ListAllMyBuckets",
                            "s3:GetBucketLocation"
                        ],
                        "Resource": "arn:aws:s3:::*"
                    }
                ]
            }
        }
    }
}
```

Or select one at random from an AZ:


```json
{
    "name": "stop-an-ec2-instance-in-az-at-random",
    "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "stop_instance",
        "arguments": {
            "az": "us-west-1"
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

### Credentials

This extension uses the [boto3][] library under the hood. This library expects
that you have properly [configured][creds] your environment to connect and
authenticate with the AWS services.

[boto3]: https://boto3.readthedocs.io
[creds]: https://boto3.readthedocs.io/en/latest/guide/configuration.html

Generally speaking, there are two ways of doing this:

* you have [configured][creds] the environment where you will run the
  experiment from (any of the [user-wide credential sources][sources] would
  do). You may also provide a profile name to [assume a role][role].

    ```json
    {
        "configuration": {
            "aws_profile_name": "dev"
        }
    }
    ```

* you explicitely pass the correct environment variables to the experiment
  definition as follows:

    ```json
    {
        "secrets": {
            "aws": {
                "aws_access_key_id": "your key",
                "aws_secret_access_key": "access key",
                "aws_session_token": "token",
            }
        }
    }
    ```

  Note that the token is optional.
  Then, use it as follows:

    ```json
    {
        "name": "stop-an-ec2-instance",
        "provider": {
            "type": "python",
            "module": "chaosaws.ec2.actions",
            "func": "stop_instance",
            "secrets": ["aws"],
            "arguments": {
                "instance_id": "i-123456"
            }
        }
    }
    ```

[sources]: https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials
[role]: https://boto3.readthedocs.io/en/latest/guide/configuration.html#aws-config-file

### Other AWS settings

In additon to the authentication credentials, you can configure the region
against which you want to use. At the top level of the experiment, add:

```json
{
    "configuration": {
        "aws_region": "us-east-1"
    }
}
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
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```

### Add new AWS API Support

Once you have setup your environment, you can start adding new
[AWS API support][awsapi] by adding new actions, probes and entire sub-packages
for those.

[awsapi]: https://boto3.readthedocs.io/en/latest/reference/services/index.html

#### Services supported by boto

This package relies on [boto3][] to wrap the API calls into a fluent Python
API. Some newer AWS services are not yet available in boto3, in that case,
you should read the next section.

[boto3]: https://boto3.readthedocs.io/en/latest/reference/services/index.html

Let's say you want to support a new action in the EC2 sub-package.

Start by creating a new function in `ec2/actions.py`:

```python
from chaoslib.types import Configuration, Secrets

from chaosaws import aws_client
from chaosaws.types import AWSResponse

def reboot_instance(instance_id: str, dry_run: bool=False,
                    configuration: Configuration=None,
                    secrets: Secrets=None) -> AWSResponse:
    """
    Reboot a given EC2 instance.
    """
    client = aws_client('ec2', configuration, secrets)
    return client.reboot_instances(InstanceIds=[instance_id], DryRun=dry_run)
```

As you can see, the actual code is straightforward. You first create a
[EC2 client][ec2client] and simply call the appropriate method on that client
with the expected arguments. We return the action as-is so that it can be
logged by the chaostoolkit, or even be used as part of a steady-state
hypothesis probe (if this was a probe, not action that is).

You could decide to make more than one AWS API call but, it is better to keep
it simple so that composition is easier from the experiment. Nonetheless,
you may also compose those directly into a single action as well for specific
use-cases.

Please refer to the Chaos Toolkit documentation to learn more about the
[configuration][] and [secrets][] objects.

[ec2client]: https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#client
[configuration]: http://chaostoolkit.org/reference/api/experiment/#configuration
[secrets]: http://chaostoolkit.org/reference/api/experiment/#secrets

Once you have implemented that action, you must create at least one unit test
for it in the `tests/ec2/test_ec2_actions.py` test module. For example:

```python
from chaosaws.ec2.actions import reboot_instancex

@patch('chaosaws.ec2.actions.aws_client', autospec=True)
def test_reboot_instance(aws_client):
    client = MagicMock()
    aws_client.return_value = client
    inst_id = "i-1234567890abcdef0"
    response = reboot_instance(inst_id)
    client.reboot_instances.assert_called_with(
        InstanceIds=[inst_id], DryRun=False)
```

By using the [built-in Python module to mock objects][pymock], we can mock the
EC2 client and assert we edo indeed call the appropriate method with the right
arguments. You are encouraged to write more than a single test for various
conditions.

[pymock]: https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock

Finally, should you choose to add support for a new AWS API resource altogether,
you should create the according sub-package.

#### Services not supported by boto (new AWS features)

If the support you want to provide is for a new AWS service that [boto][] does
not support yet, this requires direct call to the API endpoint via the
[requests][] package. For instance, as of April 2018, [AWS EKS][eks] is not
yet available in boto3, so let see how we can still use it.

[eks]: https://aws.amazon.com/eks/

Note: at this stage, the EKS API isn't publicly documented so let's just
assume it defines a "Terminate Worker Noder" API.

```python
from chaoslib.types import Configuration, Secrets

from chaosaws import signed_api_call
from chaosaws.types import AWSResponse

def terminate_worker_node(worker_node_id: str,
                          configuration: Configuration=None,
                          secrets: Secrets=None) -> AWSResponse:
    """
    Terminate a EKS worker node.
    """
    params = {
        "DryRun": True,
        "WorkerNodeId.1": worker_node_id
    }
    response = signed_api_call(
        'eks', path='/2018-01-01/worker/terminate',
        method='POST', params=params,
        configuration=configuration, secrets=secrets)
    return response.json()
```

Here is an example on existing API call (as a more concrete snippet):

```python
from chaoslib.types import Configuration, Secrets

from chaosaws import signed_api_call

def stop_instance(instance_id: str, configuration: Configuration=None,
                  secrets: Secrets=None) -> str:
    response = signed_api_call(
        'ec2',
        configuration=configuration,
        secrets=secrets,
        params={
            "Action": "StopInstances",
            "InstanceId.1": instance_id,
            "Version": "2013-06-15"
        }
    )

    # this API returns XML, not JSON
    return response.text
```

When using the `signed_api_call`, you are responsible for the right way of
passing the parameters. Basically, look at the AWS documentation for each
API call.

**WARNING:** It should be noted that, whenever boto3 implements an API, this
package should be updated accordingly, as boto3 is much more versatile and
solid.

#### Make your new sub-package discoverable

Finally, if you have created a new sub-package entirely, you need to make its
capability discoverable by the chaos toolkit. Simply amend the `discover`
function in the `chaosaws/__init__.py`. For example, assuming a new `eks`
sub-package, with actions and probes:

```python
    activities.extend(discover_actions("chaosaws.eks.actions"))
    activities.extend(discover_probes("chaosaws.eks.probes"))
```



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

You may provide an instance id explicitely or, if you only specify the AZ,
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


Deregister a given ECS container. Becareful that tasks handled by this
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


Stop a given ECS task instance

**Signature:**

```python
def stop_task(cluster: str,
              task_id: str,
              reason: str = 'Chaos Testing',
              configuration: Dict[str, Dict[str, str]] = None,
              secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **task_id**      | string |  | Yes |
| **reason**      | string | "Chaos Testing" | No |


**Usage:**

```json
{
  "name": "stop-task",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "stop_task",
    "arguments": {
      "cluster": "",
      "task_id": ""
    }
  }
}
```

```yaml
name: stop-task
provider:
  arguments:
    cluster: ''
    task_id: ''
  func: stop_task
  module: chaosaws.ecs.actions
  type: python
type: action

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


