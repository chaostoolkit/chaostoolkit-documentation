# Extension `chaosaws`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.13.0 |
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
pip install -U chaostoolkit-aws
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
            "env": "type",
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
python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
pytest
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






## Exported Activities



### awslambda



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
('def delete_function_concurrency(\n        function_name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |




**Usage:**

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
('def get_function_concurrency(\n        function_name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |




**Usage:**

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
('def get_function_memory_size(function_name: str,\n                             qualifier: str = None,\n                             configuration: Dict[str, Dict[str, str]] = None,\n                             secrets: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **qualifier**      | string | null | No |




**Usage:**

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
('def get_function_timeout(function_name: str,\n                         qualifier: str = None,\n                         configuration: Dict[str, Dict[str, str]] = None,\n                         secrets: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **qualifier**      | string | null | No |




**Usage:**

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
("def invoke_function(\n        function_name: str,\n        function_arguments: Dict[str, Any] = None,\n        invocation_type: str = 'RequestResponse',\n        client_context: Dict[str, Any] = None,\n        qualifier: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
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
('def put_function_concurrency(\n        function_name: str,\n        concurrent_executions: int,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **concurrent_executions**      | integer |  | Yes |




**Usage:**

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
('def put_function_memory_size(\n        function_name: str,\n        memory_size: int,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **memory_size**      | integer |  | Yes |




**Usage:**

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
('def put_function_timeout(\n        function_name: str,\n        timeout: int,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **function_name**      | string |  | Yes |
| **timeout**      | integer |  | Yes |




**Usage:**

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
('def delete_rule(rule_name: str,\n                force: bool = False,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **force**      | boolean | false | No |




**Usage:**

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
('def disable_rule(rule_name: str,\n                 configuration: Dict[str, Dict[str, str]] = None,\n                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |




**Usage:**

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
('def enable_rule(rule_name: str,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |




**Usage:**

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
('def get_alarm_state_value(alarm_name: str,\n                          configuration: Dict[str, Dict[str, str]] = None,\n                          secrets: Dict[str, Dict[str, str]] = None) -> str:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **alarm_name**      | string |  | Yes |




**Usage:**

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

More information about input parameters are available in the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics

**Signature:**

```python
('def get_metric_statistics(namespace: str,\n                          metric_name: str,\n                          dimension_name: str,\n                          dimension_value: str,\n                          duration: int = 60,\n                          offset: int = 0,\n                          statistic: str = None,\n                          extended_statistic: str = None,\n                          unit: str = None,\n                          configuration: Dict[str, Dict[str, str]] = None,\n                          secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **namespace**      | string |  | Yes |
| **metric_name**      | string |  | Yes |
| **dimension_name**      | string |  | Yes |
| **dimension_value**      | string |  | Yes |
| **duration**      | integer | 60 | No |
| **offset**      | integer | 0 | No |
| **statistic**      | string | null | No |
| **extended_statistic**      | string | null | No |
| **unit**      | string | null | No |




**Usage:**

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
      "metric_name": "",
      "dimension_name": "",
      "dimension_value": ""
    }
  }
}
```

```yaml
name: get-metric-statistics
provider:
  arguments:
    dimension_name: ''
    dimension_value: ''
    metric_name: ''
    namespace: ''
  func: get_metric_statistics
  module: chaosaws.cloudwatch.probes
  type: python
type: probe

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
('def put_rule(rule_name: str,\n             schedule_expression: str = None,\n             event_pattern: str = None,\n             state: str = None,\n             description: str = None,\n             role_arn: str = None,\n             configuration: Dict[str, Dict[str, str]] = None,\n             secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def put_rule_targets(\n        rule_name: str,\n        targets: List[Dict[str, Any]],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **targets**      | list |  | Yes |




**Usage:**

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
('def remove_rule_targets(\n        rule_name: str,\n        target_ids: List[str] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **rule_name**      | string |  | Yes |
| **target_ids**      | list | null | No |




**Usage:**

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

Parameters:
    One of:
        instance_ids: list: instance ids
        filters: list: key/value pairs to pull ec2 instances

**Signature:**

```python
('def attach_volume(\n        instance_ids: List[str] = None,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def count_instances(filters: List[Dict[str, Any]],\n                    configuration: Dict[str, Dict[str, str]] = None,\n                    secrets: Dict[str, Dict[str, str]] = None) -> int:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **filters**      | list |  | Yes |




**Usage:**

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
('def describe_instances(\n        filters: List[Dict[str, Any]],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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

#### `detach_random_volume`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ec2.actions |
| **Name**              | detach_random_volume |
| **Return**              | list |


Detaches a random ebs volume (non root) from one or more EC2 instances

Parameters:
    One of:
        instance_ids: a list of one or more ec2 instance ids
        filters: a list of key/value pairs to pull ec2 instances

    force: force detach volume (default: true)

Additional filters may be used to narrow the scope:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
('def detach_random_volume(\n        instance_ids: List[str] = None,\n        filters: List[Dict[str, Any]] = None,\n        force: bool = True,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |
| **force**      | boolean | true | No |




**Usage:**

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
('def instance_state(state: str,\n                   instance_ids: List[str] = None,\n                   filters: List[Dict[str, Any]] = None,\n                   configuration: Dict[str, Dict[str, str]] = None,\n                   secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **state**      | string |  | Yes |
| **instance_ids**      | list | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def restart_instances(\n        instance_ids: List[str] = None,\n        az: str = None,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def start_instances(\n        instance_ids: List[str] = None,\n        az: str = None,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def stop_instance(\n        instance_id: str = None,\n        az: str = None,\n        force: bool = False,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **az**      | string | null | No |
| **force**      | boolean | false | No |
| **filters**      | list | null | No |




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
| **Return**              | list |


Stop the given EC2 instances or, if none is provided, all instances
of the given availability zone. If you need more control, you can
also provide a list of filters following the documentation
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

**Signature:**

```python
('def stop_instances(\n        instance_ids: List[str] = None,\n        az: str = None,\n        filters: List[Dict[str, Any]] = None,\n        force: bool = False,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |
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
('def terminate_instance(\n        instance_id: str = None,\n        az: str = None,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def terminate_instances(\n        instance_ids: List[str] = None,\n        az: str = None,\n        filters: List[Dict[str, Any]] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_ids**      | list | null | No |
| **az**      | string | null | No |
| **filters**      | list | null | No |




**Usage:**

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
('def are_all_desired_tasks_running(\n        cluster: str,\n        service: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
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
('def delete_cluster(\n        cluster: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def delete_service(\n        service: str = None,\n        cluster: str = None,\n        service_pattern: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def deregister_container_instance(\n        cluster: str,\n        instance_id: str,\n        force: bool = False,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def describe_cluster(\n        cluster: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |




**Usage:**

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
('def describe_service(\n        cluster: str,\n        service: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |




**Usage:**

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
('def describe_tasks(\n        cluster: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |




**Usage:**

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
('def service_is_deploying(cluster: str,\n                         service: str,\n                         configuration: Dict[str, Dict[str, str]] = None,\n                         secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
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

#### `stop_random_tasks`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | stop_random_tasks |
| **Return**              | mapping |


Stop a random number of tasks based on given task_count or task_percent

You can specify a cluster by its ARN identifier or, if not provided, the
default cluster will be picked up.

Parameters:
Required:
    - cluster: name of the cluster to stop tasks in

Optional:
    - service: name of the service to stop tasks in

One Of:
    - task_count: the number of tasks to stop
    - task_percent: the percentage of tasks to stop

**Signature:**

```python
("def stop_random_tasks(\n        cluster: str = None,\n        task_count: int = None,\n        task_percent: int = None,\n        service: str = None,\n        reason: str = 'Chaos Testing',\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string | null | No |
| **task_count**      | integer | null | No |
| **task_percent**      | integer | null | No |
| **service**      | string | null | No |
| **reason**      | string | "Chaos Testing" | No |




**Usage:**

```json
{
  "name": "stop-random-tasks",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosaws.ecs.actions",
    "func": "stop_random_tasks"
  }
}
```

```yaml
name: stop-random-tasks
provider:
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
("def stop_task(cluster: str = None,\n              task_id: str = None,\n              service: str = None,\n              reason: str = 'Chaos Testing',\n              configuration: Dict[str, Dict[str, str]] = None,\n              secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
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



***

#### `update_desired_count`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.ecs.actions |
| **Name**              | update_desired_count |
| **Return**              | mapping |


Allows for changing the desired task count value for a given ecs service

Action Example:
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
('def update_desired_count(\n        cluster: str,\n        service: str,\n        desired_count: int,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster**      | string |  | Yes |
| **service**      | string |  | Yes |
| **desired_count**      | integer |  | Yes |




**Usage:**

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
('def create_cluster(\n        name: str,\n        role_arn: str,\n        vpc_config: Dict[str, Any],\n        version: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def delete_cluster(\n        name: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def describe_cluster(\n        name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def list_clusters(configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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




### elasticache



***

#### `delete_cache_clusters`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | delete_cache_clusters |
| **Return**              | list |


Deletes one or more cache clusters and creates a final snapshot

Parameters:
     cluster_ids: list: a list of one or more cache cluster ids
     final_snapshot_id: str: an identifier to give the final snapshot

**Signature:**

```python
('def delete_cache_clusters(\n        cluster_ids: List[str],\n        final_snapshot_id: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_ids**      | list |  | Yes |
| **final_snapshot_id**      | string | null | No |




**Usage:**

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

Parameters:
    group_ids: list: a list of one or more replication group ids
    final_snapshot_id: str: an identifier to give the final snapshot
    retain_primary_cluster: bool (default: True): delete only the read
        replicas associated to the replication group, not the primary

**Signature:**

```python
('def delete_replication_groups(\n        group_ids: List[str],\n        final_snapshot_id: str = None,\n        retain_primary_cluster: bool = True,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group_ids**      | list |  | Yes |
| **final_snapshot_id**      | string | null | No |
| **retain_primary_cluster**      | boolean | true | No |




**Usage:**

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

#### `reboot_cache_clusters`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosaws.elasticache.actions |
| **Name**              | reboot_cache_clusters |
| **Return**              | list |


Reboots one or more nodes in a cache cluster.
If no node ids are supplied, all nodes in the cluster will be rebooted

Parameters:
    cluster_ids: list: a list of one or more cache cluster ids
    node_ids: list: a list of one or more node ids in to the cluster

**Signature:**

```python
('def reboot_cache_clusters(\n        cluster_ids: List[str],\n        node_ids: List[str] = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cluster_ids**      | list |  | Yes |
| **node_ids**      | list | null | No |




**Usage:**

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
('def all_targets_healthy(\n        tg_names: List[str],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_names**      | list |  | Yes |




**Usage:**

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

Parameters:
    - load_balancer_names: a list of load balancer names

**Signature:**

```python
('def delete_load_balancer(load_balancer_names: List[str],\n                         configuration: Dict[str, Dict[str, str]] = None,\n                         secrets: Dict[str, Dict[str, str]] = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |




**Usage:**

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
('def deregister_target(\n        tg_name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_name**      | string |  | Yes |




**Usage:**

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

Parameters:
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
('def set_security_groups(\n        load_balancer_names: List[str],\n        security_group_ids: List[str],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |
| **security_group_ids**      | list |  | Yes |




**Usage:**

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

Parameters:
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
('def set_subnets(\n        load_balancer_names: List[str],\n        subnet_ids: List[str],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **load_balancer_names**      | list |  | Yes |
| **subnet_ids**      | list |  | Yes |




**Usage:**

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
('def targets_health_count(\n        tg_names: List[str],\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **tg_names**      | list |  | Yes |




**Usage:**

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
('def attach_role_policy(\n        arn: str,\n        role_name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
("def create_policy(name: str,\n                  policy: Dict[str, Any],\n                  path: str = '/',\n                  description: str = '',\n                  configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
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
('def detach_role_policy(\n        arn: str,\n        role_name: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
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
('def get_policy(arn: str,\n               configuration: Dict[str, Dict[str, str]] = None,\n               secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
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




### rds



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
('def delete_db_cluster(\n        db_cluster_identifier: str,\n        skip_final_snapshot: bool = True,\n        db_snapshot_identifier: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |
| **skip_final_snapshot**      | boolean | true | No |
| **db_snapshot_identifier**      | string | null | No |




**Usage:**

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
('def delete_db_cluster_endpoint(\n        db_cluster_identifier: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |




**Usage:**

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
('def delete_db_instance(\n        db_instance_identifier: str,\n        skip_final_snapshot: bool = True,\n        db_snapshot_identifier: str = None,\n        delete_automated_backups: bool = True,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **skip_final_snapshot**      | boolean | true | No |
| **db_snapshot_identifier**      | string | null | No |
| **delete_automated_backups**      | boolean | true | No |




**Usage:**

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
('def failover_db_cluster(\n        db_cluster_identifier: str,\n        target_db_instance_identifier: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |
| **target_db_instance_identifier**      | string | null | No |




**Usage:**

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
('def reboot_db_instance(\n        db_instance_identifier: str,\n        force_failover: bool = False,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **force_failover**      | boolean | false | No |




**Usage:**

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
('def stop_db_cluster(\n        db_cluster_identifier: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_cluster_identifier**      | string |  | Yes |




**Usage:**

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
('def stop_db_instance(\n        db_instance_identifier: str,\n        db_snapshot_identifier: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **db_instance_identifier**      | string |  | Yes |
| **db_snapshot_identifier**      | string | null | No |




**Usage:**

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



