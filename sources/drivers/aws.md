# Extension `chaosaws`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.21.3 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-aws |



[![Build Status](https://github.com/chaostoolkit-incubator/chaostoolkit-aws/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/chaostoolkit-incubator/chaostoolkit-aws/actions/workflows/build-and-test.yaml)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-aws.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.6+

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

#### Use default profile from `~/.aws/credentials` or `~/.aws/config`

This is the most basic case, assuming your `default` profile is properly
[configured][default] in `~/.aws/credentials` (or `~/.aws/config`),
then you do not need to pass any specific credentials to the experiment.

[default]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#shared-credentials-file

#### Use a non-default profile from `~/.aws/credentials` or `~/.aws/config`

Assuming you have configure a profile in your `~/.aws/credentials`
(or `~/.aws/config`) file, you may declare it in your experiment as follows:

```json
{
    "configuration": {
        "aws_profile_name": "dev"
    }
}
```

Your `~/.aws/credentials` should look like this:

```
[dev]
aws_access_key_id = XYZ
aws_secret_access_key = UIOPIY
```

Or, your `~/.aws/config` should look like this:

```
[profile dev]
output = json
aws_access_key_id = XYZ
aws_secret_access_key = UIOPIY
```

#### Assume an ARN role from a non-default profile

Assuming you have configure a profile in your `~/.aws/config` file with
a specific [ARN role][role] you want to assume during the run:

[role]: https://boto3.readthedocs.io/en/latest/guide/configuration.html#aws-config-file

```json
{
    "configuration": {
        "aws_profile_name": "dev"
    }
}
```

Your `~/.aws/config` should look like this:

```
[default]
output = json

[profile dev]
role_arn = arn:aws:iam::XXXXXXX:role/role-name
source_profile = default
```

#### Assume an ARN role from within the experiment

You mays also assume a role by declaring the role ARN in the experiment
directly. In that case, the profile has no impact if you also set it.

```json
    "configuration": {
        "aws_assume_role_arn": "arn:aws:iam::XXXXXXX:role/role-name",
        "aws_assume_role_session_name": "my-chaos"
    }
```

The `aws_assume_role_session_name` key is optional and will be set to
`"ChaosToolkit"` when not provided.

When this approach is used, the extension performs a [assume role][assumerole]
call against the [AWS STS][sts] service to fetch credentials dynamically.

[assumerole]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role
[sts]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html

#### Pass credentials explicitely

You can pass the credentials as a secret to the experiment definition as
follows:

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

### Setting the region

In additon to the authentication credentials, you must configure the region
against which you want to use.

You can either declare it at the top level of the experiment, add:

```json
{
    "configuration": {
        "aws_region": "us-east-1"
    }
}
```

or

```json
{
    "configuration": {
        "aws_region": {
            "type": "env",
            "key": "AWS_REGION"
        }
    }
}
```

But you can also simply set either `AWS_REGION` or `AWS_DEFAULT_REGION` in
your terminal session without declaring anything in the experiment.

If none of these are set, your experiment will likely fail.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, write unit tests to cover the proposed changes,
implement the changes, ensure they meet the formatting standards set out by `black`,
`flake8`, and `isort`, and then raise a PR to the repository for review.

Please refer to the [formatting](#formatting-and-linting) section for more information
on the formatting standards.

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
$ make install-dev
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Tests

To run the tests for the project execute the following:

```console
$ make tests
```

### Formatting and Linting

We use a combination of [`black`][black], [`flake8`][flake8], and [`isort`][isort] to both
lint and format this repositories code.

[black]: https://github.com/psf/black
[flake8]: https://github.com/PyCQA/flake8
[isort]: https://github.com/PyCQA/isort

Before raising a Pull Request, we recommend you run formatting against your code with:

```console
$ make format
```

This will automatically format any code that doesn't adhere to the formatting standards.

As some things are not picked up by the formatting, we also recommend you run:

```console
$ make lint
```

To ensure that any unused import statements/strings that are too long, etc. are also picked up.

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
EC2 client and assert that we do indeed call the appropriate method with the right
arguments. You are encouraged to write more than a single test for various
conditions.

[pymock]: https://docs.python.org/3/library/unittest.mock.html#module-unittest.mock

Finally, should you choose to add support for a new AWS API resource altogether,
you should create the according sub-package.

#### Services not supported by boto (new AWS features)

If the support you want to provide is for a new AWS service that [boto][] does
not support yet, this requires direct call to the API endpoint via the
[requests][] package. Say we have a new service, not yet supported by boto3

[eks]: https://aws.amazon.com/eks/
[boto]: https://boto3.readthedocs.io/en/latest/index.html
[requests]: http://docs.python-requests.org/en/master/

```python
from chaoslib.types import Configuration, Secrets

from chaosaws import signed_api_call
from chaosaws.types import AWSResponse

def terminate_worker_node(worker_node_id: str,
                          configuration: Configuration=None,
                          secrets: Secrets=None) -> AWSResponse:
    """
    Terminate a worker node.
    """
    params = {
        "DryRun": True,
        "WorkerNodeId.1": worker_node_id
    }
    response = signed_api_call(
        'some-new-service-name', path='/2018-01-01/worker/terminate',
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




## Exported Controls



### upload




This module exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment Loading**       | False | False |
| **Experiment**               | False | True |
| **Steady-state Hypothesis**  | False | False |
| **Method**                   | False | False |
| **Rollback**                 | False | False |
| **Activities**               | False | False |

In addition, the controls may define the followings:

|            Level             |             Enabled             |
| -----------------------------| ------------------------------ |
| **Validate Control**       | False |
| **Configure Control**       | False |
| **Cleanup Control**       | False |

To use this control module, please add the following section to your experiment:

=== "JSON"
    ```json

    {
      "controls": [
        {
          "name": "chaosaws",
          "provider": {
            "type": "python",
            "module": "chaosaws.s3.controls.upload"
          }
        }
      ]
    }

    ```
=== "YAML"
    ```yaml

    controls:
    - name: chaosaws
      provider:
        module: chaosaws.s3.controls.upload
        type: python
    

    ```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.




## Exported Activities



### asg



***

#### `attach_volume`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | attach_volume |
| **Return**              | list |


Attaches ebs volumes that have been previously detached by CTK

:
    One of:
   asg_names: list: one or more asg names
   tags: list: key/value pairs to identify asgs by

`tags` are expected as a list of dictionary objects:
    [
   {'Key': 'TagKey1', 'Value': 'TagValue1'},
   {'Key': 'TagKey2', 'Value': 'TagValue2'},
   ...
    ]

**Signature:**

```python
def attach_volume(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "attach-volume",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "attach_volume"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: attach-volume
    provider:
      func: attach_volume
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `change_subnets`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | change_subnets |
| **Return**              | None |


Adds/removes subnets on autoscaling groups

:
    One of:
   asg_names: a list of one or more asg names
   tags: a list of key/value pair to identify asg(s) by

    subnets: a list of subnet IDs to associate to the ASG

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def change_subnets(subnets: List[str],
                   asg_names: List[str] = None,
                   tags: List[dict] = None,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **subnets**      | list |  | Yes |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "change-subnets",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "change_subnets",
        "arguments": {
          "subnets": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: change-subnets
    provider:
      arguments:
        subnets: []
      func: change_subnets
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `describe_auto_scaling_groups`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | describe_auto_scaling_groups |
| **Return**              | mapping |


Returns AWS descriptions for provided ASG(s)

Params:
    OneOf:
   - asg_names: a list of asg names to describe
   - tags: a list of key/value pairs to collect ASG(s)

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def describe_auto_scaling_groups(
        asg_names: List[str] = None,
        tags: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-auto-scaling-groups",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "describe_auto_scaling_groups"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-auto-scaling-groups
    provider:
      func: describe_auto_scaling_groups
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `desired_equals_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | desired_equals_healthy |
| **Return**              | boolean |


If desired number matches the number of healthy instances
for each of the auto-scaling groups

Returns: bool

**Signature:**

```python
def desired_equals_healthy(asg_names: List[str],
                           configuration: Dict[str, Dict[str, str]] = None,
                           secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "desired-equals-healthy",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "desired_equals_healthy",
        "arguments": {
          "asg_names": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: desired-equals-healthy
    provider:
      arguments:
        asg_names: []
      func: desired_equals_healthy
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `desired_equals_healthy_tags`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | desired_equals_healthy_tags |
| **Return**              | boolean |


If desired number matches the number of healthy instances

for each of the auto-scaling groups matching tags provided

`tags` are  expected as:
[{
    'Key': 'KeyName',
    'Value': 'KeyValue'
},
...
]

Returns: bool

**Signature:**

```python
def desired_equals_healthy_tags(
        tags: List[Dict[str, str]],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tags**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "desired-equals-healthy-tags",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "desired_equals_healthy_tags",
        "arguments": {
          "tags": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: desired-equals-healthy-tags
    provider:
      arguments:
        tags: []
      func: desired_equals_healthy_tags
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `detach_random_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | detach_random_instances |
| **Return**              | mapping |


Detaches one or more random instances from an autoscaling group

:
    One of:
   asg_names: a list of one or more asg names
   tags: a list of key/value pair to identify asg(s) by

    One of:
   instance_count: integer value of number of instances to detach
   instance_percent: 1-100, percent of instances to detach

    decrement_capacity: boolean value to determine if the desired capacity
    of the autoscaling group should be decreased

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def detach_random_instances(
        asg_names: List[str] = None,
        tags: List[dict] = None,
        instance_count: int = None,
        instance_percent: int = None,
        decrement_capacity: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **instance_count**      | integer | null | No |
| **instance_percent**      | integer | null | No |
| **decrement_capacity**      | boolean | false | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "detach-random-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "detach_random_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: detach-random-instances
    provider:
      func: detach_random_instances
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `detach_random_volume`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | detach_random_volume |
| **Return**              | list |


Detaches a random (non root) ebs volume from ec2 instances
associated to an ASG

:
    One of:
   asg_names: a list of one or more asg names
   tags: a list of key/value pair to identify asg(s) by

    force: force detach volume (default: true)

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def detach_random_volume(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        force: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **force**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "detach-random-volume",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "detach_random_volume"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: detach-random-volume
    provider:
      func: detach_random_volume
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `has_subnets`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | has_subnets |
| **Return**              | boolean |


Determines if the provided autoscaling groups are in the provided subnets

:returns boolean

**Signature:**

```python
def has_subnets(subnets: List[str],
                asg_names: List[str] = None,
                tags: List[Dict[str, str]] = None,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **subnets**      | list |  | Yes |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "has-subnets",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "has_subnets",
        "arguments": {
          "subnets": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: has-subnets
    provider:
      arguments:
        subnets: []
      func: has_subnets
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `instance_count_by_health`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | instance_count_by_health |
| **Return**              | integer |


Reports the number of instances currently in the ASG by their health
status

Params:
    OneOf:
   - asg_names: a list of asg names to describe
   - tags: a list of key/value pairs to collect ASG(s)

    - count_healthy: boolean: true for healthy instance count,
false for unhealthy instance count

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def instance_count_by_health(asg_names: List[str] = None,
                             tags: List[Dict[str, str]] = None,
                             count_healthy: bool = True,
                             configuration: Dict[str, Dict[str, str]] = None,
                             secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **count_healthy**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "instance-count-by-health",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "instance_count_by_health"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: instance-count-by-health
    provider:
      func: instance_count_by_health
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `is_scaling_in_progress`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | is_scaling_in_progress |
| **Return**              | boolean |


Check if there is any scaling activity in progress for ASG matching tags

Returns: Boolean

**Signature:**

```python
def is_scaling_in_progress(tags: List[Dict[str, str]],
                           configuration: Dict[str, Dict[str, str]] = None,
                           secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tags**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "is-scaling-in-progress",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "is_scaling_in_progress",
        "arguments": {
          "tags": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: is-scaling-in-progress
    provider:
      arguments:
        tags: []
      func: is_scaling_in_progress
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `process_is_suspended`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | process_is_suspended |
| **Return**              | boolean |


Determines if one or more processes on an ASG are suspended.

:returns Boolean

**Signature:**

```python
def process_is_suspended(asg_names: List[str] = None,
                         tags: List[Dict[str, str]] = None,
                         process_names: List[str] = None,
                         configuration: Dict[str, Dict[str, str]] = None,
                         secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **process_names**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "process-is-suspended",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "process_is_suspended"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: process-is-suspended
    provider:
      func: process_is_suspended
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `resume_processes`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | resume_processes |
| **Return**              | mapping |


Resumes 1 or more suspended processes on a list of auto scaling groups.

If no process is specified, all suspended auto scaling
processes will be resumed.

For a list of valid processes that can be suspended, reference:
https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html

:
    One of:
   - asg_names: a list of one or more asg names to target
   - tags: a list of key/value pairs to identify the asgs by

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def resume_processes(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        process_names: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **process_names**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "resume-processes",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "resume_processes"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: resume-processes
    provider:
      func: resume_processes
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `stop_random_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | stop_random_instances |
| **Return**              | list |


Terminates one or more random healthy instances associated to an ALB

A healthy instance is considered one with a status of 'InService'

:
    - force: force stop the instances (default: False)

    One Of:
   - asg_names: a list of one or more asg names to target
   - tags: a list of key/value pairs to identify the asgs by

    One Of:
   - instance_count: the number of instances to terminate
   - instance_percent: the percentage of instances to terminate
   - az: the availability zone to terminate instances

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def stop_random_instances(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        instance_count: int = None,
        instance_percent: int = None,
        az: str = None,
        force: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **instance_count**      | integer | null | No |
| **instance_percent**      | integer | null | No |
| **az**      | string | null | No |
| **force**      | boolean | false | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "stop-random-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "stop_random_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: stop-random-instances
    provider:
      func: stop_random_instances
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `suspend_processes`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | suspend_processes |
| **Return**              | mapping |


Suspends 1 or more processes on a list of auto scaling groups.

If no process is specified, all running auto scaling
processes will be suspended.

For a list of valid processes that can be suspended, reference:
https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html

:
    One of:
   - asg_names: a list of one or more asg names to target
   - tags: a list of key/value pairs to identify the asgs by

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def suspend_processes(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        process_names: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **process_names**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "suspend-processes",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "suspend_processes"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: suspend-processes
    provider:
      func: suspend_processes
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `terminate_random_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.asg.actions |
| **Name**              | terminate_random_instances |
| **Return**              | list |


Terminates one or more random healthy instances associated to an ALB

A healthy instance is considered one with a status of 'InService'

:
   One Of:
  - asg_names: a list of one or more asg names to target
  - tags: a list of key/value pairs to identify the asgs by

   One Of:
  - instance_count: the number of instances to terminate
  - instance_percent: the percentage of instances to terminate
  - az: the availability zone to terminate instances

`tags` are expected as a list of dictionary objects:
[
    {'Key': 'TagKey1', 'Value': 'TagValue1'},
    {'Key': 'TagKey2', 'Value': 'TagValue2'},
    ...
]

**Signature:**

```python
def terminate_random_instances(
        asg_names: List[str] = None,
        tags: List[Dict[str, str]] = None,
        instance_count: int = None,
        instance_percent: int = None,
        az: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list | null | No |
| **tags**      | list | null | No |
| **instance_count**      | integer | null | No |
| **instance_percent**      | integer | null | No |
| **az**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "terminate-random-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.actions",
        "func": "terminate_random_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: terminate-random-instances
    provider:
      func: terminate_random_instances
      module: chaosaws.asg.actions
      type: python
    type: action
    

    ```



***

#### `wait_desired_equals_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | wait_desired_equals_healthy |
| **Return**              | integer |


Wait until desired number matches the number of healthy instances
for each of the auto-scaling groups

Returns: Integer (number of seconds it took to wait)
or sys.maxsize in case of timeout

**Signature:**

```python
def wait_desired_equals_healthy(
        asg_names: List[str],
        configuration: Dict[str, Dict[str, str]] = None,
        timeout: Union[int, float] = 300,
        secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **asg_names**      | list |  | Yes |
| **timeout**      | object | 300 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "wait-desired-equals-healthy",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "wait_desired_equals_healthy",
        "arguments": {
          "asg_names": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: wait-desired-equals-healthy
    provider:
      arguments:
        asg_names: []
      func: wait_desired_equals_healthy
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `wait_desired_equals_healthy_tags`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | wait_desired_equals_healthy_tags |
| **Return**              | integer |


Wait until desired number matches the number of healthy instances
for each of the auto-scaling groups matching tags provided

`tags` are  expected as:
[{
    'Key': 'KeyName',
    'Value': 'KeyValue'
},
...
]

Returns: Integer (number of seconds it took to wait)
or sys.maxsize in case of timeout

**Signature:**

```python
def wait_desired_equals_healthy_tags(
        tags: List[Dict[str, str]],
        timeout: Union[int, float] = 300,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tags**      | list |  | Yes |
| **timeout**      | object | 300 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "wait-desired-equals-healthy-tags",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "wait_desired_equals_healthy_tags",
        "arguments": {
          "tags": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: wait-desired-equals-healthy-tags
    provider:
      arguments:
        tags: []
      func: wait_desired_equals_healthy_tags
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```



***

#### `wait_desired_not_equals_healthy_tags`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.asg.probes |
| **Name**              | wait_desired_not_equals_healthy_tags |
| **Return**              | integer |


Wait until desired number doesn't match the number of healthy instances
for each of the auto-scaling groups matching tags provided

`tags` are  expected as:
[{
    'Key': 'KeyName',
    'Value': 'KeyValue'
},
...
]

Returns: Integer (number of seconds it took to wait)
or sys.maxsize in case of timeout

**Signature:**

```python
def wait_desired_not_equals_healthy_tags(
        tags: List[Dict[str, str]],
        timeout: Union[int, float] = 300,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tags**      | list |  | Yes |
| **timeout**      | object | 300 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "wait-desired-not-equals-healthy-tags",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.asg.probes",
        "func": "wait_desired_not_equals_healthy_tags",
        "arguments": {
          "tags": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: wait-desired-not-equals-healthy-tags
    provider:
      arguments:
        tags: []
      func: wait_desired_not_equals_healthy_tags
      module: chaosaws.asg.probes
      type: python
    type: probe
    

    ```




### awslambda



***

#### `delete_event_source_mapping`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | delete_event_source_mapping |
| **Return**              | mapping |


Delete an event source mapping

:param event_uuid: The identifier of the event source mapping
:param configuration: AWS configuration data
:param secrets: AWS secrets
:return: AWSResponse

**Signature:**

```python
def delete_event_source_mapping(
        event_uuid: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **event_uuid**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-event-source-mapping",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "delete_event_source_mapping",
        "arguments": {
          "event_uuid": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-event-source-mapping
    provider:
      arguments:
        event_uuid: ''
      func: delete_event_source_mapping
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `delete_function_concurrency`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | delete_function_concurrency |
| **Return**              | mapping |


Removes concurrency limit applied to the specified Lambda

**Signature:**

```python
def delete_function_concurrency(
        function_name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-function-concurrency",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "delete_function_concurrency",
        "arguments": {
          "function_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-function-concurrency
    provider:
      arguments:
        function_name: ''
      func: delete_function_concurrency
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `get_function_concurrency`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.awslambda.probes |
| **Name**              | get_function_concurrency |
| **Return**              | boolean |


Get configuration information of lambda by its function name

**Signature:**

```python
def get_function_concurrency(
        function_name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-function-concurrency",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.probes",
        "func": "get_function_concurrency",
        "arguments": {
          "function_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-function-concurrency
    provider:
      arguments:
        function_name: ''
      func: get_function_concurrency
      module: chaosaws.awslambda.probes
      type: python
    type: probe
    

    ```



***

#### `get_function_memory_size`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.awslambda.probes |
| **Name**              | get_function_memory_size |
| **Return**              | integer |


Get the configured memory size of a lambda function.

The returned memory size is specified in megabytes.

**Signature:**

```python
def get_function_memory_size(function_name: str,
                             qualifier: str = None,
                             configuration: Dict[str, Dict[str, str]] = None,
                             secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **qualifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-function-memory-size",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.probes",
        "func": "get_function_memory_size",
        "arguments": {
          "function_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-function-memory-size
    provider:
      arguments:
        function_name: ''
      func: get_function_memory_size
      module: chaosaws.awslambda.probes
      type: python
    type: probe
    

    ```



***

#### `get_function_timeout`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.awslambda.probes |
| **Name**              | get_function_timeout |
| **Return**              | integer |


Get the configured timeout of a lambda function.

The returned timeout is specified in number of seconds.

**Signature:**

```python
def get_function_timeout(function_name: str,
                         qualifier: str = None,
                         configuration: Dict[str, Dict[str, str]] = None,
                         secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **qualifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-function-timeout",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.probes",
        "func": "get_function_timeout",
        "arguments": {
          "function_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-function-timeout
    provider:
      arguments:
        function_name: ''
      func: get_function_timeout
      module: chaosaws.awslambda.probes
      type: python
    type: probe
    

    ```



***

#### `invoke_function`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | invoke_function |
| **Return**              | mapping |


Invokes Lambda.

More information about request arguments are available in the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke

**Signature:**

```python
def invoke_function(
        function_name: str,
        function_arguments: Dict[str, Any] = None,
        invocation_type: str = 'RequestResponse',
        client_context: Dict[str, Any] = None,
        qualifier: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **function_arguments**      | mapping | null | No |
| **invocation_type**      | string | "RequestResponse" | No |
| **client_context**      | mapping | null | No |
| **qualifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "invoke-function",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "invoke_function",
        "arguments": {
          "function_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: invoke-function
    provider:
      arguments:
        function_name: ''
      func: invoke_function
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `list_event_source_mapping`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.awslambda.probes |
| **Name**              | list_event_source_mapping |
| **Return**              | mapping |


List event source mappings for the provided lambda function or ARN of the
event source

:param source_arn: The ARN of the event source
:param function_name: The name of the lambda function
:param configuration: AWS configuration data
:param secrets: AWS secrets
:return: AWSResponse

**Signature:**

```python
def list_event_source_mapping(
        source_arn: str = None,
        function_name: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **source_arn**      | string | null | No |
| **function_name**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-event-source-mapping",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.probes",
        "func": "list_event_source_mapping"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-event-source-mapping
    provider:
      func: list_event_source_mapping
      module: chaosaws.awslambda.probes
      type: python
    type: probe
    

    ```



***

#### `put_function_concurrency`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | put_function_concurrency |
| **Return**              | mapping |


Throttles Lambda by setting reserved concurrency amount.

**Signature:**

```python
def put_function_concurrency(
        function_name: str,
        concurrent_executions: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **concurrent_executions**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-function-concurrency",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "put_function_concurrency",
        "arguments": {
          "function_name": "",
          "concurrent_executions": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-function-concurrency
    provider:
      arguments:
        concurrent_executions: 0
        function_name: ''
      func: put_function_concurrency
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `put_function_memory_size`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | put_function_memory_size |
| **Return**              | mapping |


Sets the function memory size.

Input memory_size argument is specified in megabytes.

**Signature:**

```python
def put_function_memory_size(
        function_name: str,
        memory_size: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **memory_size**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-function-memory-size",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "put_function_memory_size",
        "arguments": {
          "function_name": "",
          "memory_size": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-function-memory-size
    provider:
      arguments:
        function_name: ''
        memory_size: 0
      func: put_function_memory_size
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `put_function_timeout`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | put_function_timeout |
| **Return**              | mapping |


Sets the function timeout.

Input timeout argument is specified in seconds.

**Signature:**

```python
def put_function_timeout(
        function_name: str,
        timeout: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **timeout**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-function-timeout",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "put_function_timeout",
        "arguments": {
          "function_name": "",
          "timeout": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-function-timeout
    provider:
      arguments:
        function_name: ''
        timeout: 0
      func: put_function_timeout
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```



***

#### `toggle_event_source_mapping_state`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.awslambda.actions |
| **Name**              | toggle_event_source_mapping_state |
| **Return**              | mapping |


Toggle an event source mapping to be disabled or enabled

:param event_uuid: The identifier of the event source mapping
:param enabled: Boolean value: true to enable, false to disable
:param configuration: AWS configuration data
:param secrets: AWS secrets
:return: AWSResponse

**Signature:**

```python
def toggle_event_source_mapping_state(
        event_uuid: str,
        enabled: bool,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **event_uuid**      | string |  | Yes |
| **enabled**      | boolean |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "toggle-event-source-mapping-state",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.awslambda.actions",
        "func": "toggle_event_source_mapping_state",
        "arguments": {
          "event_uuid": "",
          "enabled": true
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: toggle-event-source-mapping-state
    provider:
      arguments:
        enabled: true
        event_uuid: ''
      func: toggle_event_source_mapping_state
      module: chaosaws.awslambda.actions
      type: python
    type: action
    

    ```




### cloudwatch



***

#### `delete_rule`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | delete_rule |
| **Return**              | mapping |


Deletes a CloudWatch rule.

All rule targets must be removed before deleting the rule.
Set input argument force to True to force all rule targets to be deleted.

**Signature:**

```python
def delete_rule(rule_name: str,
                force: bool = False,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **force**      | boolean | false | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-rule",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "delete_rule",
        "arguments": {
          "rule_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-rule
    provider:
      arguments:
        rule_name: ''
      func: delete_rule
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `disable_rule`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | disable_rule |
| **Return**              | mapping |


Disables a CloudWatch rule.

**Signature:**

```python
def disable_rule(rule_name: str,
                 configuration: Dict[str, Dict[str, str]] = None,
                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "disable-rule",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "disable_rule",
        "arguments": {
          "rule_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: disable-rule
    provider:
      arguments:
        rule_name: ''
      func: disable_rule
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `enable_rule`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | enable_rule |
| **Return**              | mapping |


Enables a CloudWatch rule.

**Signature:**

```python
def enable_rule(rule_name: str,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "enable-rule",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "enable_rule",
        "arguments": {
          "rule_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: enable-rule
    provider:
      arguments:
        rule_name: ''
      func: enable_rule
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `get_alarm_state_value`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.cloudwatch.probes |
| **Name**              | get_alarm_state_value |
| **Return**              | string |


Return the state value of an alarm.

The possbile alarm state values are described in the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_alarms

**Signature:**

```python
def get_alarm_state_value(alarm_name: str,
                          configuration: Dict[str, Dict[str, str]] = None,
                          secrets: Dict[str, Dict[str, str]] = None) -> str:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **alarm_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-alarm-state-value",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.probes",
        "func": "get_alarm_state_value",
        "arguments": {
          "alarm_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-alarm-state-value
    provider:
      arguments:
        alarm_name: ''
      func: get_alarm_state_value
      module: chaosaws.cloudwatch.probes
      type: python
    type: probe
    

    ```



***

#### `get_metric_data`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.cloudwatch.probes |
| **Name**              | get_metric_data |
| **Return**              | number |


Gets metric data for a given metric in a given time period. This method
allows for more data to be retrieved than get_metric_statistics

:params
    namespace: The AWS metric namespace
    metric_name: The name of the metric to pull data for
    One of:
   dimension_name, dimension_value: Required to search for ONE dimension
   dimensions: Required to search for dimensions combinations
   Are expected as a list of dictionary objects:
   [{‘Name’: ‘Dim1’, ‘Value’: ‘Val1’}, {‘Name’: ‘Dim2’, ‘Value’: ‘Val2’}, …]
    unit: The type of unit desired to be collected
    statistic: The type of data to return.
   One of: Average, Sum, Minimum, Maximum, SampleCount
    period: The window in which to pull datapoints for
    offset: The time (seconds) to offset the endtime (from now)
    duration: The time (seconds) to set the start time (from now)

**Signature:**

```python
def get_metric_data(namespace: str,
                    metric_name: str,
                    dimension_name: str = None,
                    dimension_value: str = None,
                    dimensions: List[Dict[str, str]] = None,
                    statistic: str = None,
                    duration: int = 300,
                    period: int = 60,
                    offset: int = 0,
                    unit: str = None,
                    configuration: Dict[str, Dict[str, str]] = None,
                    secrets: Dict[str, Dict[str, str]] = None) -> float:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **namespace**      | string |  | Yes |
| **metric_name**      | string |  | Yes |
| **dimension_name**      | string | null | No |
| **dimension_value**      | string | null | No |
| **dimensions**      | list | null | No |
| **statistic**      | string | null | No |
| **duration**      | integer | 300 | No |
| **period**      | integer | 60 | No |
| **offset**      | integer | 0 | No |
| **unit**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-metric-data",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.probes",
        "func": "get_metric_data",
        "arguments": {
          "namespace": "",
          "metric_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-metric-data
    provider:
      arguments:
        metric_name: ''
        namespace: ''
      func: get_metric_data
      module: chaosaws.cloudwatch.probes
      type: python
    type: probe
    

    ```



***

#### `get_metric_statistics`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.cloudwatch.probes |
| **Name**              | get_metric_statistics |
| **Return**              | None |


Get the value of a statistical calculation for a given metric.

The period for which the calculation will be performed is specified by a duration and
an offset from the current time. Both are specified in seconds.

Example: A duration of 60 seconds and an offset of 30 seconds will yield a
statistical value based on the time interval between 30 and 90 seconds in the past.

Is required one of:
    dimension_name, dimension_value: Required to search for ONE dimension
    dimensions: Required to search for dimensions combinations
    Are expected as a list of dictionary objects:
    [{‘Name’: ‘Dim1’, ‘Value’: ‘Val1’}, {‘Name’: ‘Dim2’, ‘Value’: ‘Val2’}, …]

More information about input parameters are available in the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics

**Signature:**

```python
def get_metric_statistics(namespace: str,
                          metric_name: str,
                          dimension_name: str = None,
                          dimension_value: str = None,
                          dimensions: List[Dict[str, str]] = None,
                          duration: int = 60,
                          offset: int = 0,
                          statistic: str = None,
                          extended_statistic: str = None,
                          unit: str = None,
                          configuration: Dict[str, Dict[str, str]] = None,
                          secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **namespace**      | string |  | Yes |
| **metric_name**      | string |  | Yes |
| **dimension_name**      | string | null | No |
| **dimension_value**      | string | null | No |
| **dimensions**      | list | null | No |
| **duration**      | integer | 60 | No |
| **offset**      | integer | 0 | No |
| **statistic**      | string | null | No |
| **extended_statistic**      | string | null | No |
| **unit**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-metric-statistics",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.probes",
        "func": "get_metric_statistics",
        "arguments": {
          "namespace": "",
          "metric_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-metric-statistics
    provider:
      arguments:
        metric_name: ''
        namespace: ''
      func: get_metric_statistics
      module: chaosaws.cloudwatch.probes
      type: python
    type: probe
    

    ```



***

#### `put_metric_data`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | put_metric_data |
| **Return**              | None |


Publish metric data points to CloudWatch

:param namespace: The metric namespace
:param metric_data: A list of metric data to submit
:param configuration: AWS authentication configuration
:param secrets: Additional authentication secrets
:return: None

example:
    namespace='MyCustomTestMetric',
    metric_data=[
   {
  'MetricName': 'MemoryUsagePercent',
  'Dimensions': [
 {'Name': 'InstanceId', 'Value': 'i-000000000000'},
 {'Name': 'Instance Name', 'Value': 'Test Instance'}
  ],
  'Timestamp': datetime(yyyy, mm, dd, HH, MM, SS),
  'Value': 55.55,
  'Unit': 'Percent',
  'StorageResolution': 60
   }
    ]

For additional information, consult: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data

**Signature:**

```python
def put_metric_data(namespace: str,
                    metric_data: List[Dict[str, Any]],
                    configuration: Dict[str, Dict[str, str]] = None,
                    secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **namespace**      | string |  | Yes |
| **metric_data**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-metric-data",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "put_metric_data",
        "arguments": {
          "namespace": "",
          "metric_data": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-metric-data
    provider:
      arguments:
        metric_data: []
        namespace: ''
      func: put_metric_data
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `put_rule`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | put_rule |
| **Return**              | mapping |


Creates or updates a CloudWatch event rule.

Please refer to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#CloudWatchEvents.Client.put_rule
for details on input arguments.

**Signature:**

```python
def put_rule(rule_name: str,
             schedule_expression: str = None,
             event_pattern: str = None,
             state: str = None,
             description: str = None,
             role_arn: str = None,
             configuration: Dict[str, Dict[str, str]] = None,
             secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **schedule_expression**      | string | null | No |
| **event_pattern**      | string | null | No |
| **state**      | string | null | No |
| **description**      | string | null | No |
| **role_arn**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-rule",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "put_rule",
        "arguments": {
          "rule_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-rule
    provider:
      arguments:
        rule_name: ''
      func: put_rule
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `put_rule_targets`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | put_rule_targets |
| **Return**              | mapping |


Creates or update CloudWatch event rule targets.

Please refer to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#CloudWatchEvents.Client.put_targets
for details on input arguments.

**Signature:**

```python
def put_rule_targets(
        rule_name: str,
        targets: List[Dict[str, Any]],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **targets**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-rule-targets",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "put_rule_targets",
        "arguments": {
          "rule_name": "",
          "targets": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-rule-targets
    provider:
      arguments:
        rule_name: ''
        targets: []
      func: put_rule_targets
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```



***

#### `remove_rule_targets`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.cloudwatch.actions |
| **Name**              | remove_rule_targets |
| **Return**              | mapping |


Removes CloudWatch rule targets. If no target ids are provided all targets will be removed.

**Signature:**

```python
def remove_rule_targets(
        rule_name: str,
        target_ids: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **target_ids**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "remove-rule-targets",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.cloudwatch.actions",
        "func": "remove_rule_targets",
        "arguments": {
          "rule_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-rule-targets
    provider:
      arguments:
        rule_name: ''
      func: remove_rule_targets
      module: chaosaws.cloudwatch.actions
      type: python
    type: action
    

    ```




### ec2



***

#### `attach_volume`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | attach_volume |
| **Return**              | list |


Attaches a previously detached EBS volume to its associated EC2 instance.

If neither 'instance_ids' or 'filters' are provided, all detached volumes
will be reattached to their respective instances

:
    One of:
   instance_ids: list: instance ids
   filters: list: key/value pairs to pull ec2 instances

**Signature:**

```python
def attach_volume(
        instance_ids: List[str] = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "attach-volume",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "attach_volume"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: attach-volume
    provider:
      func: attach_volume
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `count_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ec2.probes |
| **Name**              | count_instances |
| **Return**              | integer |


Return count of instances matching the specified filters.

Please refer to https://bit.ly/2Sv9lmU

for details on said filters.

**Signature:**

```python
def count_instances(filters: List[Dict[str, Any]],
                    configuration: Dict[str, Dict[str, str]] = None,
                    secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filters**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "count-instances",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.probes",
        "func": "count_instances",
        "arguments": {
          "filters": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: count-instances
    provider:
      arguments:
        filters: []
      func: count_instances
      module: chaosaws.ec2.probes
      type: python
    type: probe
    

    ```



***

#### `count_min_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ec2.probes |
| **Name**              | count_min_instances |
| **Return**              | boolean |


Returns whether minimum number of instances
available matching the specified filters.

**Signature:**

```python
def count_min_instances(filters: List[Dict[str, Any]],
                        min_count: int = 0,
                        configuration: Dict[str, Dict[str, str]] = None,
                        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filters**      | list |  | Yes |
| **min_count**      | integer | 0 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "count-min-instances",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.probes",
        "func": "count_min_instances",
        "arguments": {
          "filters": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: count-min-instances
    provider:
      arguments:
        filters: []
      func: count_min_instances
      module: chaosaws.ec2.probes
      type: python
    type: probe
    

    ```



***

#### `describe_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ec2.probes |
| **Name**              | describe_instances |
| **Return**              | mapping |


Describe instances following the specified filters.

Please refer to https://bit.ly/2Sv9lmU

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

=== "JSON"
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
=== "YAML"
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

#### `detach_random_volume`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | detach_random_volume |
| **Return**              | list |


Detaches a random ebs volume (non root) from one or more EC2 instances

:
    One of:
   instance_ids: a list of one or more ec2 instance ids
   filters: a list of key/value pairs to pull ec2 instances

    force: force detach volume (default: true)

Additional filters may be used to narrow the scope:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def detach_random_volume(
        instance_ids: List[str] = None,
        filters: List[Dict[str, Any]] = None,
        force: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |
| **force**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "detach-random-volume",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "detach_random_volume"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: detach-random-volume
    provider:
      func: detach_random_volume
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `instance_state`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ec2.probes |
| **Name**              | instance_state |
| **Return**              | boolean |


Determines if EC2 instances match desired state

For additional filter options, please refer to the documentation found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def instance_state(state: str,
                   instance_ids: List[str] = None,
                   filters: List[Dict[str, Any]] = None,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **state**      | string |  | Yes |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "instance-state",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.probes",
        "func": "instance_state",
        "arguments": {
          "state": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: instance-state
    provider:
      arguments:
        state: ''
      func: instance_state
      module: chaosaws.ec2.probes
      type: python
    type: probe
    

    ```



***

#### `restart_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | restart_instances |
| **Return**              | list |


Restarts one or more EC2 instances.

WARNING: If only an Availability Zone is provided, all instances in the
provided AZ will be restarted.

Additional filters may be used to narrow the scope:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def restart_instances(
        instance_ids: List[str] = None,
        az: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "restart-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "restart_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: restart-instances
    provider:
      func: restart_instances
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `start_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | start_instances |
| **Return**              | list |


Starts one or more EC2 instances.

WARNING: If only an Availability Zone is provided, all instances in the
provided AZ will be started.

Additional filters may be used to narrow the scope:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def start_instances(
        instance_ids: List[str] = None,
        az: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "start-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "start_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: start-instances
    provider:
      func: start_instances
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `stop_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | stop_instance |
| **Return**              | list |


Stop a single EC2 instance.

You may provide an instance id explicitly or, if you only specify the AZ,
a random instance will be selected. If you need more control, you can
also provide a list of filters following the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def stop_instance(
        instance_id: str = None,
        az: str = None,
        force: bool = False,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **az**      | string | null | No |
| **force**      | boolean | false | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
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
=== "YAML"
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
| **Return**              | list |


Stop the given EC2 instances or, if none is provided, all instances
of the given availability zone. If you need more control, you can
also provide a list of filters following the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def stop_instances(
        instance_ids: List[str] = None,
        az: str = None,
        filters: List[Dict[str, Any]] = None,
        force: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |
| **force**      | boolean | false | No |




**Usage:**

=== "JSON"
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
=== "YAML"
    ```yaml

    name: stop-instances
    provider:
      func: stop_instances
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `terminate_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | terminate_instance |
| **Return**              | list |


Terminates a single EC2 instance.

An instance may be targeted by specifying it by instance-id. If only the
availability-zone is provided, a random instances in that AZ will be
selected and terminated. For more control, please reference the available
filters found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def terminate_instance(
        instance_id: str = None,
        az: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "terminate-instance",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "terminate_instance"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: terminate-instance
    provider:
      func: terminate_instance
      module: chaosaws.ec2.actions
      type: python
    type: action
    

    ```



***

#### `terminate_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | terminate_instances |
| **Return**              | list |


Terminates multiple EC2 instances

A set of instances may be targeted by providing them as the instance-ids.

WARNING: If  only an Availability Zone is specified, all instances in
that AZ will be terminated.

Additional filters may be used to narrow the scope:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
def terminate_instances(
        instance_ids: List[str] = None,
        az: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "terminate-instances",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ec2.actions",
        "func": "terminate_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: terminate-instances
    provider:
      func: terminate_instances
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

=== "JSON"
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
=== "YAML"
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


Delete an ECS cluster

:param cluster: The ECS cluster name or ARN
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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


Deregister an ECS container

Warning: If using "force", Any tasks not deleted before deregistration
will remain orphaned

:param cluster: The ECS cluster name or ARN or ARN
:param instance_id: The container instance id or ARN
:param force: Force deregistraion of container instance
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

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

=== "JSON"
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
=== "YAML"
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

#### `describe_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ecs.probes |
| **Name**              | describe_cluster |
| **Return**              | mapping |


Returns AWS response describing the specified cluster

Probe example:
    "steady-state-hypothesis": {
   "title": "MyCluster has 3 running tasks",
   "probes": [{
  "type": "probe",
  "name": "Cluster running task count",
  "tolerance": {
 "type": "jsonpath",
 "path": $.clusters[0].runningTasksCount,
 "expect": 3
  },
  "provider": {
 "type": "python",
 "module": "chaosaws.ecs.probes",
 "func": "describe_cluster",
 "arguments": {
"cluster": "MyCluster"
 }
  }
   }
    }

Full list of possible paths can be found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_clusters

**Signature:**

```python
def describe_cluster(
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

=== "JSON"
    ```json

    {
      "name": "describe-cluster",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.probes",
        "func": "describe_cluster",
        "arguments": {
          "cluster": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-cluster
    provider:
      arguments:
        cluster: ''
      func: describe_cluster
      module: chaosaws.ecs.probes
      type: python
    type: probe
    

    ```



***

#### `describe_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ecs.probes |
| **Name**              | describe_service |
| **Return**              | mapping |


Returns AWS response describing the specified cluster service

Probe example:
    "steady-state-hypothesis": {
   "title": "MyService pending count is 1",
   "probes": [{
  "type": "probe",
  "name": "Service pending count",
  "tolerance": {
 "type": "jsonpath",
 "path": $.services[0].pendingCount,
 "expect": 1
  },
  "provider": {
 "type": "python",
 "module": "chaosaws.ecs.probes",
 "func": "describe_service",
 "arguments": {
"cluster": "MyCluster",
"service": "MyService"
 }
  }
   }]
    }

Full list of possible paths can be found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_services

**Signature:**

```python
def describe_service(
        cluster: str,
        service: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-service",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.probes",
        "func": "describe_service",
        "arguments": {
          "cluster": "",
          "service": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-service
    provider:
      arguments:
        cluster: ''
        service: ''
      func: describe_service
      module: chaosaws.ecs.probes
      type: python
    type: probe
    

    ```



***

#### `describe_tasks`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.ecs.probes |
| **Name**              | describe_tasks |
| **Return**              | mapping |


Returns AWS response describing the tasks for a provided cluster

Probe example:
    "steady-state-hypothesis": {
   "title": "MyCluster tasks are healthy",
   "probes": [{
  "type": "probe",
  "name": "first task is healthy",
  "tolerance": {
 "type": "jsonpath",
 "path": $.tasks[0].healthStatus,
 "expect": "HEALTHY"
  },
  "provider": {
 "type": "python",
 "module": "chaosaws.ecs.probes",
 "func": "describe_tasks",
 "arguments": {
"cluster": "MyCluster"
 }
  }
   }]
    }

Full list of possible paths can be found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_tasks

**Signature:**

```python
def describe_tasks(
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

=== "JSON"
    ```json

    {
      "name": "describe-tasks",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.probes",
        "func": "describe_tasks",
        "arguments": {
          "cluster": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-tasks
    provider:
      arguments:
        cluster: ''
      func: describe_tasks
      module: chaosaws.ecs.probes
      type: python
    type: probe
    

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

=== "JSON"
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
=== "YAML"
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

#### `set_service_deployment_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | set_service_deployment_configuration |
| **Return**              | mapping |


Sets the maximum healthy count and minimum healthy percentage values for
a services deployment configuration

:param cluster: The ECS cluster name or ARN
:param service: The ECS service name
:param maximum_percent: The upper limit on the number of tasks a service is
    allowed to have in RUNNING or PENDING during deployment
:param minimum_healthy_percent: The lower limit on the number of tasks a
    service must keep in RUNNING to be considered healthy during deployment
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def set_service_deployment_configuration(
        cluster: str,
        service: str,
        maximum_percent: int = 200,
        minimum_healthy_percent: int = 100,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |
| **maximum_percent**      | integer | 200 | No |
| **minimum_healthy_percent**      | integer | 100 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "set-service-deployment-configuration",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "set_service_deployment_configuration",
        "arguments": {
          "cluster": "",
          "service": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: set-service-deployment-configuration
    provider:
      arguments:
        cluster: ''
        service: ''
      func: set_service_deployment_configuration
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `set_service_placement_strategy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | set_service_placement_strategy |
| **Return**              | mapping |


Sets the service's instance placement strategy

:param cluster: The ECS cluster name or ARN
:param service: The ECS service name
:param placement_type: The type of placement strategy to employ
    (random, spread, or binpack)
:param placement_field: The field to apply the strategy against
    (eg: "attribute:ecs.availability-zone")
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def set_service_placement_strategy(
        cluster: str,
        service: str,
        placement_type: str,
        placement_field: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |
| **placement_type**      | string |  | Yes |
| **placement_field**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "set-service-placement-strategy",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "set_service_placement_strategy",
        "arguments": {
          "cluster": "",
          "service": "",
          "placement_type": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: set-service-placement-strategy
    provider:
      arguments:
        cluster: ''
        placement_type: ''
        service: ''
      func: set_service_placement_strategy
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `stop_random_tasks`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | stop_random_tasks |
| **Return**              | list |


Stop a random number of tasks based on given task_count or task_percent

You can specify a cluster by its ARN identifier or, if not provided, the
default cluster will be picked up.

:param cluster: The ECS cluster Name
:param task_count: The number of tasks to stop
:param task_percent: The percentage of total tasks to stop
:param service: The ECS service name
:param reason: An explanation of why the service was stopped
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: List[Dict[str, Any]]

**Signature:**

```python
def stop_random_tasks(
        cluster: str,
        task_count: int = None,
        task_percent: int = None,
        service: str = None,
        reason: str = 'Chaos Testing',
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **task_count**      | integer | null | No |
| **task_percent**      | integer | null | No |
| **service**      | string | null | No |
| **reason**      | string | "Chaos Testing" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "stop-random-tasks",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "stop_random_tasks",
        "arguments": {
          "cluster": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: stop-random-tasks
    provider:
      arguments:
        cluster: ''
      func: stop_random_tasks
      module: chaosaws.ecs.actions
      type: python
    type: action
    

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

=== "JSON"
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
=== "YAML"
    ```yaml

    name: stop-task
    provider:
      func: stop_task
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `tag_resource`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | tag_resource |
| **Return**              | None |


Tags the provided resource(s) with provided tags

** For ECS resources, the long form ARN must be used
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-account-settings.html#ecs-resource-arn-timeline

Example:
    {
   "tags": [
  {"key": "MyTagKey", "value": "MyTagValue"},
  {"key": "MyOtherTagKey", "value": "MyOtherTagValue"}
   ],
   "resource_arn": "arn:aws:ecs:us-east-1:123456789012:cluster/name"
    }

:param tags: A list of key/value pairs
:param resource_arn: The ARN of the resource to tag.
    Valid resources: capacity providers, tasks, services, task definitions,
    clusters, and container instances
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def tag_resource(tags: List[Dict[str, str]],
                 resource_arn: str,
                 configuration: Dict[str, Dict[str, str]] = None,
                 secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tags**      | list |  | Yes |
| **resource_arn**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "tag-resource",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "tag_resource",
        "arguments": {
          "tags": [],
          "resource_arn": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: tag-resource
    provider:
      arguments:
        resource_arn: ''
        tags: []
      func: tag_resource
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `untag_resource`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | untag_resource |
| **Return**              | None |


Removes the given tags from the provided resource

** For ECS resources, the long form ARN must be used
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-account-settings.html#ecs-resource-arn-timeline

Example:
    {
   "tag_keys": ["MyTagKey", "MyOtherTagKey"],
   "resource_arn": "arn:aws:ecs:...:service/cluster-name/service-name"
    }

:param tag_keys: A list of tag keys to remove
:param resource_arn: The ARN of the resource to tag.
    Valid resources: capacity providers, tasks, services, task definitions,
    clusters, and container instances
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def untag_resource(tag_keys: List[str],
                   resource_arn: str,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tag_keys**      | list |  | Yes |
| **resource_arn**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "untag-resource",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "untag_resource",
        "arguments": {
          "tag_keys": [],
          "resource_arn": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: untag-resource
    provider:
      arguments:
        resource_arn: ''
        tag_keys: []
      func: untag_resource
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `update_container_instances_state`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | update_container_instances_state |
| **Return**              | mapping |


Modify the status of an ACTIVE ECS container instance

:param cluster: The ECS cluster name or ARN
:param container_instances: A list of container instance ids for ARNs
:param status: The desired instance state (Valid States: ACTIVE, DRAINING)
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def update_container_instances_state(
        cluster: str,
        container_instances: List[str],
        status: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **container_instances**      | list |  | Yes |
| **status**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "update-container-instances-state",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "update_container_instances_state",
        "arguments": {
          "cluster": "",
          "container_instances": [],
          "status": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: update-container-instances-state
    provider:
      arguments:
        cluster: ''
        container_instances: []
        status: ''
      func: update_container_instances_state
      module: chaosaws.ecs.actions
      type: python
    type: action
    

    ```



***

#### `update_desired_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | update_desired_count |
| **Return**              | mapping |


Set the number of desired tasks for an ECS service

:param cluster: The ECS cluster name or ARN or ARN
:param service: The ECS service name
:param desired_count: The number of instantiation of the tasks to run
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

Example:
    "method": {
   "type": "action",
   "name": "update service",
   "provider": {
  "type": "python",
  "module": "chaosaws.ecs.actions",
  "func": "update_desired_count",
  "arguments": {
 "cluster": "my_cluster_name",
 "service": "my_service_name",
 "desired_count": 6
  }
   }
    }

**Signature:**

```python
def update_desired_count(
        cluster: str,
        service: str,
        desired_count: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |
| **desired_count**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "update-desired-count",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "update_desired_count",
        "arguments": {
          "cluster": "",
          "service": "",
          "desired_count": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: update-desired-count
    provider:
      arguments:
        cluster: ''
        desired_count: 0
        service: ''
      func: update_desired_count
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
    ```yaml

    name: list-clusters
    provider:
      func: list_clusters
      module: chaosaws.eks.probes
      type: python
    type: probe
    

    ```




### elasticache



***

#### `count_cache_clusters_from_replication_group`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elasticache.probes |
| **Name**              | count_cache_clusters_from_replication_group |
| **Return**              | integer |


Returns the number of cache clusters that are part of the given
ReplicationGroupId
:param replication_group_id: The identifier for the replication group
to be described
:param configuration: Configuration
:param secrets: Secrets
Probe example:
    "steady-state-hypothesis": {
   "title": "MyCluster has 3 nodes",
   "probes": [{
  "type": "probe",
  "name": "Cluster running node count",
  "tolerance": 3,
  "provider": {
 "type": "python",
 "module": "modules.elasticache",
 "func": "count_cache_clusters_from_replication_group",
 "arguments": {
"replication_group_id": "MyCluster"
 }
  }
   }
    }

**Signature:**

```python
def count_cache_clusters_from_replication_group(
        replication_group_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **replication_group_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "count-cache-clusters-from-replication-group",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.probes",
        "func": "count_cache_clusters_from_replication_group",
        "arguments": {
          "replication_group_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: count-cache-clusters-from-replication-group
    provider:
      arguments:
        replication_group_id: ''
      func: count_cache_clusters_from_replication_group
      module: chaosaws.elasticache.probes
      type: python
    type: probe
    

    ```



***

#### `delete_cache_clusters`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | delete_cache_clusters |
| **Return**              | list |


Deletes one or more cache clusters and creates a final snapshot

:
cluster_ids: list: a list of one or more cache cluster ids
final_snapshot_id: str: an identifier to give the final snapshot

**Signature:**

```python
def delete_cache_clusters(
        cluster_ids: List[str],
        final_snapshot_id: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_ids**      | list |  | Yes |
| **final_snapshot_id**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-cache-clusters",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.actions",
        "func": "delete_cache_clusters",
        "arguments": {
          "cluster_ids": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-cache-clusters
    provider:
      arguments:
        cluster_ids: []
      func: delete_cache_clusters
      module: chaosaws.elasticache.actions
      type: python
    type: action
    

    ```



***

#### `delete_replication_groups`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | delete_replication_groups |
| **Return**              | list |


Deletes one or more replication groups and creates a final snapshot

:
    group_ids: list: a list of one or more replication group ids
    final_snapshot_id: str: an identifier to give the final snapshot
    retain_primary_cluster: bool (default: True): delete only the read
   replicas associated to the replication group, not the primary

**Signature:**

```python
def delete_replication_groups(
        group_ids: List[str],
        final_snapshot_id: str = None,
        retain_primary_cluster: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group_ids**      | list |  | Yes |
| **final_snapshot_id**      | string | null | No |
| **retain_primary_cluster**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-replication-groups",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.actions",
        "func": "delete_replication_groups",
        "arguments": {
          "group_ids": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-replication-groups
    provider:
      arguments:
        group_ids: []
      func: delete_replication_groups
      module: chaosaws.elasticache.actions
      type: python
    type: action
    

    ```



***

#### `describe_cache_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elasticache.probes |
| **Name**              | describe_cache_cluster |
| **Return**              | mapping |


Returns cache cluster data for given cluster

:param cluster_id: str: the name of the cache cluster
:param show_node_info: bool: show associated nodes (default: False)
:param configuration: Configuration
:param secrets: Secrets

:example:
{
    "type": "probe",
    "name": "validate cache cluster engine",
    "tolerance": {
   "type": "jsonpath",
   "path": $.CacheClusters[0].Engine,
   "expect": "memcached"
    },
    "provider": {
   "type": "python",
   "module": "chaosaws.elasticache.probes",
   "func": "describe_cache_cluster",
   "arguments": {
  "cluster_id": "MyTestCluster"
   }
    }
}

Full list of possible paths can be found:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_clusters

**Signature:**

```python
def describe_cache_cluster(
        cluster_id: str,
        show_node_info: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **show_node_info**      | boolean | false | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-cache-cluster",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.probes",
        "func": "describe_cache_cluster",
        "arguments": {
          "cluster_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-cache-cluster
    provider:
      arguments:
        cluster_id: ''
      func: describe_cache_cluster
      module: chaosaws.elasticache.probes
      type: python
    type: probe
    

    ```



***

#### `get_cache_node_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elasticache.probes |
| **Name**              | get_cache_node_count |
| **Return**              | integer |


Returns the number of cache nodes associated to the cluster

:param cluster_id: str: the name of the cache cluster
:param configuration: Configuration
:param secrets: Secrets

:example:
{
    "type": "probe",
    "name": "validate cache node count",
    "tolerance": 3,
    "provider": {
   "type": "python",
   "module": "chaosaws.elasticache.probes",
   "func": "get_cache_node_count",
   "arguments": {
  "cluster_id": "MyTestCluster"
   }
    }
}

**Signature:**

```python
def get_cache_node_count(cluster_id: str,
                         configuration: Dict[str, Dict[str, str]] = None,
                         secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-cache-node-count",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.probes",
        "func": "get_cache_node_count",
        "arguments": {
          "cluster_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-cache-node-count
    provider:
      arguments:
        cluster_id: ''
      func: get_cache_node_count
      module: chaosaws.elasticache.probes
      type: python
    type: probe
    

    ```



***

#### `get_cache_node_status`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elasticache.probes |
| **Name**              | get_cache_node_status |
| **Return**              | string |


Returns the status of the given cache cluster

:param cluster_id: str: the name of the cache cluster
:param configuration: Configuration
:param secrets: Secrets

:example:
{
    "type": "probe",
    "name": "validate cache node status",
    "tolerance": "available",
    "provider": {
   "type": "python",
   "module": "chaosaws.elasticache.probes",
   "func": "get_cache_node_status",
   "arguments": {
  "cluster_id": "MyTestCluster"
   }
    }
}

**Signature:**

```python
def get_cache_node_status(cluster_id: str,
                          configuration: Dict[str, Dict[str, str]] = None,
                          secrets: Dict[str, Dict[str, str]] = None) -> str:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-cache-node-status",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.probes",
        "func": "get_cache_node_status",
        "arguments": {
          "cluster_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-cache-node-status
    provider:
      arguments:
        cluster_id: ''
      func: get_cache_node_status
      module: chaosaws.elasticache.probes
      type: python
    type: probe
    

    ```



***

#### `reboot_cache_clusters`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | reboot_cache_clusters |
| **Return**              | list |


Reboots one or more nodes in a cache cluster.
If no node ids are supplied, all nodes in the cluster will be rebooted

:
    cluster_ids: list: a list of one or more cache cluster ids
    node_ids: list: a list of one or more node ids in to the cluster

**Signature:**

```python
def reboot_cache_clusters(
        cluster_ids: List[str],
        node_ids: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_ids**      | list |  | Yes |
| **node_ids**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "reboot-cache-clusters",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.actions",
        "func": "reboot_cache_clusters",
        "arguments": {
          "cluster_ids": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: reboot-cache-clusters
    provider:
      arguments:
        cluster_ids: []
      func: reboot_cache_clusters
      module: chaosaws.elasticache.actions
      type: python
    type: action
    

    ```



***

#### `test_failover`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | test_failover |
| **Return**              | list |


Tests automatic failover on a single shard (also known as node groups).
You can only invoke test_failover for no more than 5 shards in any rolling 24-hour
period.

:
    replication_group_id: str: the name of the replication group
   (also known as cluster) whose automatic failover is being
   tested by this operation.
    node_group_id: str: the name of the node group (also known as shard)
   in this replication group on which automatic failover is to be tested.

**Signature:**

```python
def test_failover(
        replication_group_id: str,
        node_group_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **replication_group_id**      | string |  | Yes |
| **node_group_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "test-failover",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elasticache.actions",
        "func": "test_failover",
        "arguments": {
          "replication_group_id": "",
          "node_group_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: test-failover
    provider:
      arguments:
        node_group_id: ''
        replication_group_id: ''
      func: test_failover
      module: chaosaws.elasticache.actions
      type: python
    type: action
    

    ```




### elbv2



***

#### `all_targets_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elbv2.probes |
| **Name**              | all_targets_healthy |
| **Return**              | mapping |


Return true/false based on if all targets for listed
target groups are healthy

**Signature:**

```python
def all_targets_healthy(
        tg_names: List[str],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_names**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "all-targets-healthy",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.probes",
        "func": "all_targets_healthy",
        "arguments": {
          "tg_names": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: all-targets-healthy
    provider:
      arguments:
        tg_names: []
      func: all_targets_healthy
      module: chaosaws.elbv2.probes
      type: python
    type: probe
    

    ```



***

#### `delete_load_balancer`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elbv2.actions |
| **Name**              | delete_load_balancer |
| **Return**              | None |


Deletes the provided load balancer(s).

:
    - load_balancer_names: a list of load balancer names

**Signature:**

```python
def delete_load_balancer(load_balancer_names: List[str],
                         configuration: Dict[str, Dict[str, str]] = None,
                         secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-load-balancer",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.actions",
        "func": "delete_load_balancer",
        "arguments": {
          "load_balancer_names": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-load-balancer
    provider:
      arguments:
        load_balancer_names: []
      func: delete_load_balancer
      module: chaosaws.elbv2.actions
      type: python
    type: action
    

    ```



***

#### `deregister_target`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elbv2.actions |
| **Name**              | deregister_target |
| **Return**              | mapping |


Deregisters one random target from target group

**Signature:**

```python
def deregister_target(
        tg_name: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deregister-target",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.actions",
        "func": "deregister_target",
        "arguments": {
          "tg_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deregister-target
    provider:
      arguments:
        tg_name: ''
      func: deregister_target
      module: chaosaws.elbv2.actions
      type: python
    type: action
    

    ```



***

#### `enable_access_log`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elbv2.actions |
| **Name**              | enable_access_log |
| **Return**              | boolean |


Enable or Disable Access logs of ELB

**Signature:**

```python
def enable_access_log(load_balancer_arn: str,
                      enable: bool = False,
                      bucket_name: str = None,
                      configuration: Dict[str, Dict[str, str]] = None,
                      secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_arn**      | string |  | Yes |
| **enable**      | boolean | false | No |
| **bucket_name**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "enable-access-log",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.actions",
        "func": "enable_access_log",
        "arguments": {
          "load_balancer_arn": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: enable-access-log
    provider:
      arguments:
        load_balancer_arn: ''
      func: enable_access_log
      module: chaosaws.elbv2.actions
      type: python
    type: action
    

    ```



***

#### `is_access_log_enabled`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elbv2.probes |
| **Name**              | is_access_log_enabled |
| **Return**              | mapping |


Verify access logging enabled on load balancer

**Signature:**

```python
def is_access_log_enabled(
        load_balancer_arn: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_arn**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "is-access-log-enabled",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.probes",
        "func": "is_access_log_enabled",
        "arguments": {
          "load_balancer_arn": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: is-access-log-enabled
    provider:
      arguments:
        load_balancer_arn: ''
      func: is_access_log_enabled
      module: chaosaws.elbv2.probes
      type: python
    type: probe
    

    ```



***

#### `set_security_groups`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elbv2.actions |
| **Name**              | set_security_groups |
| **Return**              | list |


Changes the security groups for the specified load balancer(s).
This action will replace the existing security groups on an application
load balancer with the specified security groups.

:
    - load_balancer_names: a list of load balancer names
    - security_group_ids: a list of security group ids

returns:
    [
   {
  'LoadBalancerArn': 'string',
  'SecurityGroupIds': ['sg-0000000', 'sg-0000001']
   },
   ...
    ]

**Signature:**

```python
def set_security_groups(
        load_balancer_names: List[str],
        security_group_ids: List[str],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |
| **security_group_ids**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "set-security-groups",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.actions",
        "func": "set_security_groups",
        "arguments": {
          "load_balancer_names": [],
          "security_group_ids": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: set-security-groups
    provider:
      arguments:
        load_balancer_names: []
        security_group_ids: []
      func: set_security_groups
      module: chaosaws.elbv2.actions
      type: python
    type: action
    

    ```



***

#### `set_subnets`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elbv2.actions |
| **Name**              | set_subnets |
| **Return**              | list |


Changes the subnets for the specified application load balancer(s)
This action will replace the existing security groups on an application
load balancer with the specified security groups.

:
    - load_balancer_names: a list of load balancer names
    - subnet_ids: a list of subnet ids

returns:
    [
   {
  'LoadBalancerArn': 'string',
  'AvailabilityZones': {
 'ZoneName': 'string',
 'SubnetId': 'string',
 'LoadBalancerAddresses': [
{
    'IpAddress': 'string',
    'AllocationId': 'string'
}
 ]
  }
   },
   ...
    ]

**Signature:**

```python
def set_subnets(
        load_balancer_names: List[str],
        subnet_ids: List[str],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |
| **subnet_ids**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "set-subnets",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.actions",
        "func": "set_subnets",
        "arguments": {
          "load_balancer_names": [],
          "subnet_ids": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: set-subnets
    provider:
      arguments:
        load_balancer_names: []
        subnet_ids: []
      func: set_subnets
      module: chaosaws.elbv2.actions
      type: python
    type: action
    

    ```



***

#### `targets_health_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.elbv2.probes |
| **Name**              | targets_health_count |
| **Return**              | mapping |


Count of healthy/unhealthy targets per targetgroup

**Signature:**

```python
def targets_health_count(
        tg_names: List[str],
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_names**      | list |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "targets-health-count",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.elbv2.probes",
        "func": "targets_health_count",
        "arguments": {
          "tg_names": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: targets-health-count
    provider:
      arguments:
        tg_names: []
      func: targets_health_count
      module: chaosaws.elbv2.probes
      type: python
    type: probe
    

    ```




### emr



***

#### `describe_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.emr.probes |
| **Name**              | describe_cluster |
| **Return**              | mapping |


Describe a single EMR cluster

:param cluster_id: The cluster id
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def describe_cluster(
        cluster_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-cluster",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.probes",
        "func": "describe_cluster",
        "arguments": {
          "cluster_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-cluster
    provider:
      arguments:
        cluster_id: ''
      func: describe_cluster
      module: chaosaws.emr.probes
      type: python
    type: probe
    

    ```



***

#### `describe_instance_fleet`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.emr.probes |
| **Name**              | describe_instance_fleet |
| **Return**              | mapping |


Describe a single EMR instance fleet

:param cluster_id: The cluster id
:param fleet_id: The instance fleet id
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def describe_instance_fleet(
        cluster_id: str,
        fleet_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **fleet_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-instance-fleet",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.probes",
        "func": "describe_instance_fleet",
        "arguments": {
          "cluster_id": "",
          "fleet_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-instance-fleet
    provider:
      arguments:
        cluster_id: ''
        fleet_id: ''
      func: describe_instance_fleet
      module: chaosaws.emr.probes
      type: python
    type: probe
    

    ```



***

#### `describe_instance_group`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.emr.probes |
| **Name**              | describe_instance_group |
| **Return**              | mapping |


Describe a single EMR instance group

:param cluster_id: The cluster id
:param group_id: The instance group id
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def describe_instance_group(
        cluster_id: str,
        group_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **group_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-instance-group",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.probes",
        "func": "describe_instance_group",
        "arguments": {
          "cluster_id": "",
          "group_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-instance-group
    provider:
      arguments:
        cluster_id: ''
        group_id: ''
      func: describe_instance_group
      module: chaosaws.emr.probes
      type: python
    type: probe
    

    ```



***

#### `list_cluster_fleet_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.emr.probes |
| **Name**              | list_cluster_fleet_instances |
| **Return**              | mapping |


Get a list of instance fleet instances associated to the EMR cluster

:param cluster_id: The cluster id
:param fleet_id: The instance fleet id
:param fleet_type: The instance fleet type
:param instance_states: A list of instance states to include
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def list_cluster_fleet_instances(
        cluster_id: str,
        fleet_id: str,
        fleet_type: str = None,
        instance_states: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **fleet_id**      | string |  | Yes |
| **fleet_type**      | string | null | No |
| **instance_states**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-cluster-fleet-instances",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.probes",
        "func": "list_cluster_fleet_instances",
        "arguments": {
          "cluster_id": "",
          "fleet_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-cluster-fleet-instances
    provider:
      arguments:
        cluster_id: ''
        fleet_id: ''
      func: list_cluster_fleet_instances
      module: chaosaws.emr.probes
      type: python
    type: probe
    

    ```



***

#### `list_cluster_group_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.emr.probes |
| **Name**              | list_cluster_group_instances |
| **Return**              | mapping |


Get a list of instance group instances associated to the EMR cluster

:param cluster_id: The cluster id
:param group_id: The instance group id
:param group_type: The instance group type
:param instance_states: A list of instance states to include
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def list_cluster_group_instances(
        cluster_id: str,
        group_id: str,
        group_type: str = None,
        instance_states: List[str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **group_id**      | string |  | Yes |
| **group_type**      | string | null | No |
| **instance_states**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-cluster-group-instances",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.probes",
        "func": "list_cluster_group_instances",
        "arguments": {
          "cluster_id": "",
          "group_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-cluster-group-instances
    provider:
      arguments:
        cluster_id: ''
        group_id: ''
      func: list_cluster_group_instances
      module: chaosaws.emr.probes
      type: python
    type: probe
    

    ```



***

#### `modify_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.emr.actions |
| **Name**              | modify_cluster |
| **Return**              | mapping |


Set the step concurrency level on the provided cluster

:param cluster_id: The cluster id
:param concurrency: The number of steps to execute concurrently (1 - 256)
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def modify_cluster(
        cluster_id: str,
        concurrency: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **concurrency**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "modify-cluster",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.actions",
        "func": "modify_cluster",
        "arguments": {
          "cluster_id": "",
          "concurrency": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: modify-cluster
    provider:
      arguments:
        cluster_id: ''
        concurrency: 0
      func: modify_cluster
      module: chaosaws.emr.actions
      type: python
    type: action
    

    ```



***

#### `modify_instance_fleet`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.emr.actions |
| **Name**              | modify_instance_fleet |
| **Return**              | mapping |


Modify the on-demand and spot capacities for an instance fleet

:param cluster_id: The cluster id
:param fleet_id: The instance fleet id
:param on_demand_capacity: Target capacity of on-demand units
:param spot_capacity: Target capacity of spot units
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def modify_instance_fleet(
        cluster_id: str,
        fleet_id: str,
        on_demand_capacity: int = None,
        spot_capacity: int = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **fleet_id**      | string |  | Yes |
| **on_demand_capacity**      | integer | null | No |
| **spot_capacity**      | integer | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "modify-instance-fleet",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.actions",
        "func": "modify_instance_fleet",
        "arguments": {
          "cluster_id": "",
          "fleet_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: modify-instance-fleet
    provider:
      arguments:
        cluster_id: ''
        fleet_id: ''
      func: modify_instance_fleet
      module: chaosaws.emr.actions
      type: python
    type: action
    

    ```



***

#### `modify_instance_groups_instance_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.emr.actions |
| **Name**              | modify_instance_groups_instance_count |
| **Return**              | mapping |


Modify the number of instances in an instance group

:param cluster_id: The cluster id
:param group_id: The instance group id
:param instance_count: The target size for the instance group
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def modify_instance_groups_instance_count(
        cluster_id: str,
        group_id: str,
        instance_count: int,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **group_id**      | string |  | Yes |
| **instance_count**      | integer |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "modify-instance-groups-instance-count",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.actions",
        "func": "modify_instance_groups_instance_count",
        "arguments": {
          "cluster_id": "",
          "group_id": "",
          "instance_count": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: modify-instance-groups-instance-count
    provider:
      arguments:
        cluster_id: ''
        group_id: ''
        instance_count: 0
      func: modify_instance_groups_instance_count
      module: chaosaws.emr.actions
      type: python
    type: action
    

    ```



***

#### `modify_instance_groups_shrink_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.emr.actions |
| **Name**              | modify_instance_groups_shrink_policy |
| **Return**              | mapping |


Modify an instance groups shrink operations

:param cluster_id: The cluster id
:param group_id: The instance group id
:param decommission_timeout: Timeout for decommissioning an instance
:param terminate_instances: Instance id list to terminate when shrinking
:param protect_instances: Instance id list to protect when shrinking
:param termination_timeout: Override for list of instances to terminate
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: Dict[str, Any]

**Signature:**

```python
def modify_instance_groups_shrink_policy(
        cluster_id: str,
        group_id: str,
        decommission_timeout: int = None,
        terminate_instances: List[str] = None,
        protect_instances: List[str] = None,
        termination_timeout: int = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |
| **group_id**      | string |  | Yes |
| **decommission_timeout**      | integer | null | No |
| **terminate_instances**      | list | null | No |
| **protect_instances**      | list | null | No |
| **termination_timeout**      | integer | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "modify-instance-groups-shrink-policy",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.emr.actions",
        "func": "modify_instance_groups_shrink_policy",
        "arguments": {
          "cluster_id": "",
          "group_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: modify-instance-groups-shrink-policy
    provider:
      arguments:
        cluster_id: ''
        group_id: ''
      func: modify_instance_groups_shrink_policy
      module: chaosaws.emr.actions
      type: python
    type: action
    

    ```




### fis



***

#### `get_experiment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.fis.probes |
| **Name**              | get_experiment |
| **Return**              | mapping |


Gets information about the specified experiment.

:param experiment_id: str representing the id of the experiment to fetch information
    of
:param configuration: Configuration object representing the CTK Configuration
:param secrets: Secret object representing the CTK Secrets
:returns: AWSResponse representing the response from FIS upon retrieving the
    experiment information



>>> get_experiment(
...    experiment_id="EXPTUCK2dxepXgkR38"
... )
{'ResponseMetadata': {'RequestId': '0665fe39-2213-400b-b7ff-5f1ab9b7a5ea',
'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Fri, 20 Aug 2021 11:08:27 GMT',
...
'experiment': {'id': 'EXPTUCK2dxepXgkR38',
'experimentTemplateId': 'EXT6oWVA1WrLNy4XS',
...
}

**Signature:**

```python
def get_experiment(
        experiment_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **experiment_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-experiment",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.fis.probes",
        "func": "get_experiment",
        "arguments": {
          "experiment_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-experiment
    provider:
      arguments:
        experiment_id: ''
      func: get_experiment
      module: chaosaws.fis.probes
      type: python
    type: probe
    

    ```



***

#### `start_experiment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.fis.actions |
| **Name**              | start_experiment |
| **Return**              | mapping |


Starts running an experiment from the specified experiment template.

:param experiment_template_id: str representing the id of the experiment template
    to run
:param client_token: str representing the unique identifier for this experiment run.
    If a value is not provided, boto3 generates one for you
:param tags: Dict[str, str] representing tags to apply to the experiment that is
    started
:param configuration: Configuration object representing the CTK Configuration
:param secrets: Secret object representing the CTK Secrets
:returns: AWSResponse representing the response from FIS upon starting the
    experiment



>>> start_experiment(
...experiment_template_id="EXT6oWVA1WrLNy4XS"
... )
{
'ResponseMetadata': {'RequestId': '1ceaedae-5897-4b64-9ade-9e94449f1262',
'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 12 Aug 2021 14:21:19 GMT',
...
'experiment': {'id': 'EXPXDPecuQBFiZs1Jz',
'experimentTemplateId': 'EXT6oWVA1WrLNy4XS',
...
}

>>> start_experiment(
...experiment_template_id="EXT6oWVA1WrLNy4XS",
...client_token="my-unique-token",
...tags={"a-key": "a-value"}
... )

**Signature:**

```python
def start_experiment(
        experiment_template_id: str,
        client_token: str = None,
        tags: Dict[str, str] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **experiment_template_id**      | string |  | Yes |
| **client_token**      | string | null | No |
| **tags**      | mapping | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "start-experiment",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.fis.actions",
        "func": "start_experiment",
        "arguments": {
          "experiment_template_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: start-experiment
    provider:
      arguments:
        experiment_template_id: ''
      func: start_experiment
      module: chaosaws.fis.actions
      type: python
    type: action
    

    ```



***

#### `stop_experiment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.fis.actions |
| **Name**              | stop_experiment |
| **Return**              | mapping |


Stops the specified experiment.

:param experiment_id: str representing the running experiment to stop
:param configuration: Configuration object representing the CTK Configuration
:param secrets: Secret object representing the CTK Secrets
:returns: AWSResponse representing the response from FIS upon stopping the
    experiment



>>> stop_experiment(experiment_id="EXPTUCK2dxepXgkR38")
{'ResponseMetadata': {'RequestId': 'e5e9f9a9-f4d0-4d72-8704-1f26cc8b6ad6',
'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Fri, 13 Aug 2021 09:12:17 GMT',
...'experiment': {'id': 'EXPTUCK2dxepXgkR38',
'experimentTemplateId': 'EXT6oWVA1WrLNy4XS', ... }

**Signature:**

```python
def stop_experiment(
        experiment_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **experiment_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "stop-experiment",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.fis.actions",
        "func": "stop_experiment",
        "arguments": {
          "experiment_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: stop-experiment
    provider:
      arguments:
        experiment_id: ''
      func: stop_experiment
      module: chaosaws.fis.actions
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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

=== "JSON"
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
=== "YAML"
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




### rds



***

#### `cluster_membership_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.rds.probes |
| **Name**              | cluster_membership_count |
| **Return**              | integer |




**Signature:**

```python
def cluster_membership_count(cluster_id: str,
                             configuration: Dict[str, Dict[str, str]] = None,
                             secrets: Dict[str, Dict[str, str]] = None) -> int:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "cluster-membership-count",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.probes",
        "func": "cluster_membership_count",
        "arguments": {
          "cluster_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: cluster-membership-count
    provider:
      arguments:
        cluster_id: ''
      func: cluster_membership_count
      module: chaosaws.rds.probes
      type: python
    type: probe
    

    ```



***

#### `cluster_status`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.rds.probes |
| **Name**              | cluster_status |
| **Return**              | Union[str, List[str]] |




**Signature:**

```python
def cluster_status(
        cluster_id: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Union[str, List[str]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_id**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "cluster-status",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.probes",
        "func": "cluster_status"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: cluster-status
    provider:
      func: cluster_status
      module: chaosaws.rds.probes
      type: python
    type: probe
    

    ```



***

#### `delete_db_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | delete_db_cluster |
| **Return**              | mapping |


Deletes an Aurora DB cluster

- db_cluster_identifier: the identifier of the cluster to delete
- skip_final_snapshot: boolean (true): determines whether or not to
    perform a final snapshot of the cluster before deletion
- db_snapshot_identifier: the identifier to give the final rds snapshot

**Signature:**

```python
def delete_db_cluster(
        db_cluster_identifier: str,
        skip_final_snapshot: bool = True,
        db_snapshot_identifier: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |
| **skip_final_snapshot**      | boolean | true | No |
| **db_snapshot_identifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-db-cluster",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "delete_db_cluster",
        "arguments": {
          "db_cluster_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-db-cluster
    provider:
      arguments:
        db_cluster_identifier: ''
      func: delete_db_cluster
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `delete_db_cluster_endpoint`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | delete_db_cluster_endpoint |
| **Return**              | mapping |


Deletes the custom endpoint of an Aurora cluster

- db_cluster_identifier: the identifier of the cluster to delete the
    endpoint from

**Signature:**

```python
def delete_db_cluster_endpoint(
        db_cluster_identifier: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-db-cluster-endpoint",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "delete_db_cluster_endpoint",
        "arguments": {
          "db_cluster_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-db-cluster-endpoint
    provider:
      arguments:
        db_cluster_identifier: ''
      func: delete_db_cluster_endpoint
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `delete_db_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | delete_db_instance |
| **Return**              | mapping |


Deletes a RDS instance

- db_instance_identifier: the identifier of the RDS instance to delete
- skip_final_snapshot: boolean (true): determines whether or not to
    perform a final snapshot of the rds instance before deletion
- db_snapshot_identifier: the identifier to give the final rds snapshot
- delete_automated_backups: boolean (true): determines if the automated
    backups of the rds instance are deleted immediately

**Signature:**

```python
def delete_db_instance(
        db_instance_identifier: str,
        skip_final_snapshot: bool = True,
        db_snapshot_identifier: str = None,
        delete_automated_backups: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **skip_final_snapshot**      | boolean | true | No |
| **db_snapshot_identifier**      | string | null | No |
| **delete_automated_backups**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-db-instance",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "delete_db_instance",
        "arguments": {
          "db_instance_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-db-instance
    provider:
      arguments:
        db_instance_identifier: ''
      func: delete_db_instance
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `failover_db_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | failover_db_cluster |
| **Return**              | mapping |


Forces a failover for a DB cluster.

**Signature:**

```python
def failover_db_cluster(
        db_cluster_identifier: str,
        target_db_instance_identifier: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |
| **target_db_instance_identifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "failover-db-cluster",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "failover_db_cluster",
        "arguments": {
          "db_cluster_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: failover-db-cluster
    provider:
      arguments:
        db_cluster_identifier: ''
      func: failover_db_cluster
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `instance_status`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.rds.probes |
| **Name**              | instance_status |
| **Return**              | Union[str, List[str]] |




**Signature:**

```python
def instance_status(
        instance_id: str = None,
        filters: List[Dict[str, Any]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Union[str, List[str]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "instance-status",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.probes",
        "func": "instance_status"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: instance-status
    provider:
      func: instance_status
      module: chaosaws.rds.probes
      type: python
    type: probe
    

    ```



***

#### `reboot_db_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | reboot_db_instance |
| **Return**              | mapping |


Forces a reboot of your DB instance.

**Signature:**

```python
def reboot_db_instance(
        db_instance_identifier: str,
        force_failover: bool = False,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **force_failover**      | boolean | false | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "reboot-db-instance",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "reboot_db_instance",
        "arguments": {
          "db_instance_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: reboot-db-instance
    provider:
      arguments:
        db_instance_identifier: ''
      func: reboot_db_instance
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `stop_db_cluster`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | stop_db_cluster |
| **Return**              | mapping |


Stop a RDS Cluster

- db_cluster_identifier: the identifier of the RDS cluster to stop

**Signature:**

```python
def stop_db_cluster(
        db_cluster_identifier: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "stop-db-cluster",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "stop_db_cluster",
        "arguments": {
          "db_cluster_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: stop-db-cluster
    provider:
      arguments:
        db_cluster_identifier: ''
      func: stop_db_cluster
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```



***

#### `stop_db_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.rds.actions |
| **Name**              | stop_db_instance |
| **Return**              | mapping |


Stops a RDS DB instance

- db_instance_identifier: the instance identifier of the RDS instance
- db_snapshot_identifier: the name of the DB snapshot made before stop

**Signature:**

```python
def stop_db_instance(
        db_instance_identifier: str,
        db_snapshot_identifier: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **db_snapshot_identifier**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "stop-db-instance",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.rds.actions",
        "func": "stop_db_instance",
        "arguments": {
          "db_instance_identifier": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: stop-db-instance
    provider:
      arguments:
        db_instance_identifier: ''
      func: stop_db_instance
      module: chaosaws.rds.actions
      type: python
    type: action
    

    ```




### route53



***

#### `associate_vpc_with_zone`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.route53.actions |
| **Name**              | associate_vpc_with_zone |
| **Return**              | mapping |


Associate a VPC with a private hosted zone

:param zone_id: The hosted zone id
:param vpc_id: The id of the vpc
:param vpc_region: The region of the vpc
:param configuration: access values used by actions/probes
:param comment: a comment regarding the request
:param secrets: values that need to be passed on to actions/probes
:returns: Dict[str, Any]

**Signature:**

```python
def associate_vpc_with_zone(
        zone_id: str,
        vpc_id: str,
        vpc_region: str,
        comment: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **zone_id**      | string |  | Yes |
| **vpc_id**      | string |  | Yes |
| **vpc_region**      | string |  | Yes |
| **comment**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "associate-vpc-with-zone",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.route53.actions",
        "func": "associate_vpc_with_zone",
        "arguments": {
          "zone_id": "",
          "vpc_id": "",
          "vpc_region": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: associate-vpc-with-zone
    provider:
      arguments:
        vpc_id: ''
        vpc_region: ''
        zone_id: ''
      func: associate_vpc_with_zone
      module: chaosaws.route53.actions
      type: python
    type: action
    

    ```



***

#### `disassociate_vpc_from_zone`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.route53.actions |
| **Name**              | disassociate_vpc_from_zone |
| **Return**              | mapping |


Remove an association between a VPC and a private hosted zone

:param zone_id: The hosted zone id
:param vpc_id: The id of the vpc
:param vpc_region: The region of the vpc
:param comment: A note regarding the disassociation request
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:returns: Dict[str, Any]

**Signature:**

```python
def disassociate_vpc_from_zone(
        zone_id: str,
        vpc_id: str,
        vpc_region: str,
        comment: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **zone_id**      | string |  | Yes |
| **vpc_id**      | string |  | Yes |
| **vpc_region**      | string |  | Yes |
| **comment**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "disassociate-vpc-from-zone",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.route53.actions",
        "func": "disassociate_vpc_from_zone",
        "arguments": {
          "zone_id": "",
          "vpc_id": "",
          "vpc_region": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: disassociate-vpc-from-zone
    provider:
      arguments:
        vpc_id: ''
        vpc_region: ''
        zone_id: ''
      func: disassociate_vpc_from_zone
      module: chaosaws.route53.actions
      type: python
    type: action
    

    ```



***

#### `get_dns_answer`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.route53.probes |
| **Name**              | get_dns_answer |
| **Return**              | mapping |


Get the DNS response for the specified record name & type

:param zone_id: The route53 zone id
:param record_name: The name of the record to get a response for
:param record_type: The type of the record set
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:returns: Dict[str, Any]

**Signature:**

```python
def get_dns_answer(
        zone_id: str,
        record_name: str,
        record_type: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **zone_id**      | string |  | Yes |
| **record_name**      | string |  | Yes |
| **record_type**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-dns-answer",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.route53.probes",
        "func": "get_dns_answer",
        "arguments": {
          "zone_id": "",
          "record_name": "",
          "record_type": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-dns-answer
    provider:
      arguments:
        record_name: ''
        record_type: ''
        zone_id: ''
      func: get_dns_answer
      module: chaosaws.route53.probes
      type: python
    type: probe
    

    ```



***

#### `get_health_check_status`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.route53.probes |
| **Name**              | get_health_check_status |
| **Return**              | mapping |


Get the status of the specified health check

:param check_id: The health check id
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:returns: Dict[str, Any]

**Signature:**

```python
def get_health_check_status(
        check_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **check_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-health-check-status",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.route53.probes",
        "func": "get_health_check_status",
        "arguments": {
          "check_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-health-check-status
    provider:
      arguments:
        check_id: ''
      func: get_health_check_status
      module: chaosaws.route53.probes
      type: python
    type: probe
    

    ```



***

#### `get_hosted_zone`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.route53.probes |
| **Name**              | get_hosted_zone |
| **Return**              | mapping |


Pull information regarding a specific zone id

:param zone_id: The route53 zone id
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:returns: Dict[str, Any]

**Signature:**

```python
def get_hosted_zone(
        zone_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **zone_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-hosted-zone",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.route53.probes",
        "func": "get_hosted_zone",
        "arguments": {
          "zone_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-hosted-zone
    provider:
      arguments:
        zone_id: ''
      func: get_hosted_zone
      module: chaosaws.route53.probes
      type: python
    type: probe
    

    ```




### s3



***

#### `bucket_exists`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.s3.probes |
| **Name**              | bucket_exists |
| **Return**              | boolean |


Validate that a bucket exists

:param bucket_name: The name of the S3 bucket
:param configuration: access values used by actions/probes
:param secrets: values that need to be passed on to actions/probes
:return: boolean

**Signature:**

```python
def bucket_exists(bucket_name: str,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "bucket-exists",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.s3.probes",
        "func": "bucket_exists",
        "arguments": {
          "bucket_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: bucket-exists
    provider:
      arguments:
        bucket_name: ''
      func: bucket_exists
      module: chaosaws.s3.probes
      type: python
    type: probe
    

    ```



***

#### `delete_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.s3.actions |
| **Name**              | delete_object |
| **Return**              | None |


Delete an object in a S3 bucket

:param bucket_name: the S3 bucket name
:param object_key: the path to the object
:param version_id: the version id of the object (optional)
:param configuration: access values used by actions/probes (optional)
:param secrets: values that need to be passed on to actions/probes (optional)
:return: None

**Signature:**

```python
def delete_object(bucket_name: str,
                  object_key: str,
                  version_id: str = None,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |
| **object_key**      | string |  | Yes |
| **version_id**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.s3.actions",
        "func": "delete_object",
        "arguments": {
          "bucket_name": "",
          "object_key": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-object
    provider:
      arguments:
        bucket_name: ''
        object_key: ''
      func: delete_object
      module: chaosaws.s3.actions
      type: python
    type: action
    

    ```



***

#### `object_exists`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosaws.s3.probes |
| **Name**              | object_exists |
| **Return**              | boolean |


Validate that an object exists in a S3 bucket

:param bucket_name: the name of the S3 bucket
:param object_key: the path to the object
:param version_id: the version id of the object (optional)
:param configuration: access values used by actions/probes (optional)
:param secrets: values that need to be passed on to actions/probes (optional)
:return: boolean

**Signature:**

```python
def object_exists(bucket_name: str,
                  object_key: str,
                  version_id: str = None,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |
| **object_key**      | string |  | Yes |
| **version_id**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "object-exists",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosaws.s3.probes",
        "func": "object_exists",
        "arguments": {
          "bucket_name": "",
          "object_key": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: object-exists
    provider:
      arguments:
        bucket_name: ''
        object_key: ''
      func: object_exists
      module: chaosaws.s3.probes
      type: python
    type: probe
    

    ```



***

#### `toggle_versioning`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.s3.actions |
| **Name**              | toggle_versioning |
| **Return**              | null |


Toggles versioning on a S3 bucket

If the "status" parameter is not provided, the bucket will be scanned to
determine if versioning is enabled. If it is enabled, it will be suspended.
If it is suspended it will be enabled using basic values unless MFA is provided.

:param bucket_name: The S3 bucket name
:param status: "Enabled" to turn on versioning, "Suspended" to disable
:param mfa: The authentication device serial number, a space, and the value from
    the device (optional)
:param mfa_delete: Specifies if MFA delete is enabled in the bucket versioning
    (optional)
:param owner: The account ID of the expected bucket owner (optional)
:param configuration: access values used by actions/probes (optional)
:param secrets: values that need to be passed on to actions/probes (optional)
:return: None

**Signature:**

```python
def toggle_versioning(bucket_name: str,
                      mfa_delete: str = None,
                      status: str = None,
                      mfa: str = None,
                      owner: str = None,
                      configuration: Dict[str, Dict[str, str]] = None,
                      secrets: Dict[str, Dict[str, str]] = None) -> None:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |
| **mfa_delete**      | string | null | No |
| **status**      | string | null | No |
| **mfa**      | string | null | No |
| **owner**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "toggle-versioning",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.s3.actions",
        "func": "toggle_versioning",
        "arguments": {
          "bucket_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: toggle-versioning
    provider:
      arguments:
        bucket_name: ''
      func: toggle_versioning
      module: chaosaws.s3.actions
      type: python
    type: action
    

    ```




### controls




### ssm



***

#### `create_document`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ssm.actions |
| **Name**              | create_document |
| **Return**              | mapping |


creates a Systems Manager (SSM) document.
An SSM document defines the actions that SSM performs on your managed.
For more information about SSM documents:
https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-ssm-docs.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_document

**Signature:**

```python
def create_document(
        path_content: str,
        name: str,
        version_name: str = None,
        document_type: str = None,
        document_format: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **path_content**      | string |  | Yes |
| **name**      | string |  | Yes |
| **version_name**      | string | null | No |
| **document_type**      | string | null | No |
| **document_format**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-document",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ssm.actions",
        "func": "create_document",
        "arguments": {
          "path_content": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-document
    provider:
      arguments:
        name: ''
        path_content: ''
      func: create_document
      module: chaosaws.ssm.actions
      type: python
    type: action
    

    ```



***

#### `delete_document`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ssm.actions |
| **Name**              | delete_document |
| **Return**              | mapping |


creates a Systems Manager (SSM) document.

An SSM document defines the actions that SSM performs on your managed.
For more information about SSM documents:
https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-ssm-docs.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.create_document

**Signature:**

```python
def delete_document(
        name: str,
        version_name: str = None,
        force: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **version_name**      | string | null | No |
| **force**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-document",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ssm.actions",
        "func": "delete_document",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-document
    provider:
      arguments:
        name: ''
      func: delete_document
      module: chaosaws.ssm.actions
      type: python
    type: action
    

    ```



***

#### `put_parameter`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ssm.actions |
| **Name**              | put_parameter |
| **Return**              | mapping |


Add or update a parameter in the Systems Manager Parameter Store.

:param name: str name of the parameter
:param value: str value of the parameter
:param description: str information about the parameter
:param type: str type of the paramater value, such as 'String'
:param key_id: str KMS key id to use while encrypting the parameter value
:param overwrite: bool allow the parameter value to be overwritten
:param allowed_pattern: str regex to validate parameter value
:param tags: List[Dict[str, str]] metadata about the parameter
:param tier: str storage classes such as 'Advanced' to allow larger parameter
    values
:param policies: str storage policies such as expiration in JSON format
:param data_type: str data type for String. Allows the validation of AMI IDs
:param configuration: Configuration object representing the CTK Configuration
:param secrets: Secret object representing the CTK Secrets
:returns: dict representing the Version and Tier of the parameter



>>> Configuration within experiment
   {
   "name": "Activate Chaos",
   "type": "action",
   "provider": {
  "type": "python",
  "module": "chaosaws.ssm.actions",
  "func": "put_parameter",
  "arguments": {
 "name": "chaos_trigger",
 "value": true,
 "overwrite": true,
 "type": "SecureString",
  }
   },
    }

**Signature:**

```python
def put_parameter(name: str,
                  value: str,
                  description: str = None,
                  type: str = None,
                  key_id: str = None,
                  overwrite: bool = False,
                  allowed_pattern: str = None,
                  tags: List[Dict[str, str]] = None,
                  tier: str = None,
                  policies: str = None,
                  data_type: str = None,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **value**      | string |  | Yes |
| **description**      | string | null | No |
| **type**      | string | null | No |
| **key_id**      | string | null | No |
| **overwrite**      | boolean | false | No |
| **allowed_pattern**      | string | null | No |
| **tags**      | list | null | No |
| **tier**      | string | null | No |
| **policies**      | string | null | No |
| **data_type**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "put-parameter",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ssm.actions",
        "func": "put_parameter",
        "arguments": {
          "name": "",
          "value": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: put-parameter
    provider:
      arguments:
        name: ''
        value: ''
      func: put_parameter
      module: chaosaws.ssm.actions
      type: python
    type: action
    

    ```



***

#### `send_command`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ssm.actions |
| **Name**              | send_command |
| **Return**              | mapping |


Runs commands on one or more managed instances.

An SSM document defines the actions that SSM performs on your managed.
For more information about SSM SendCommand:
https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_SendCommand.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command

**Signature:**

```python
def send_command(document_name: str,
                 targets: List[Dict[str, Any]] = None,
                 document_version: str = None,
                 parameters: Dict[str, Any] = None,
                 timeout_seconds: int = None,
                 max_concurrency: str = None,
                 max_errors: str = None,
                 region: str = None,
                 configuration: Dict[str, Dict[str, str]] = None,
                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **document_name**      | string |  | Yes |
| **targets**      | list | null | No |
| **document_version**      | string | null | No |
| **parameters**      | mapping | null | No |
| **timeout_seconds**      | integer | null | No |
| **max_concurrency**      | string | null | No |
| **max_errors**      | string | null | No |
| **region**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "send-command",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosaws.ssm.actions",
        "func": "send_command",
        "arguments": {
          "document_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: send-command
    provider:
      arguments:
        document_name: ''
      func: send_command
      module: chaosaws.ssm.actions
      type: python
    type: action
    

    ```



