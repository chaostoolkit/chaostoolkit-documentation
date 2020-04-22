# Extension `chaoscf`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.7.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-cloud-foundry |



[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-cloud-foundry.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-cloud-foundry)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-cloud-foundry.svg)](https://www.python.org/)
[![Requirements Status](https://requires.io/github/chaostoolkit-incubator/chaostoolkit-cloud-foundry/requirements.svg?branch=master)](https://requires.io/github/chaostoolkit-incubator/chaostoolkit-cloud-foundry/requirements/?branch=master)
[![Has wheel](https://img.shields.io/pypi/wheel/chaostoolkit-cloud-foundry.svg)](http://pythonwheels.com/)

This extension package provides probes and actions for Chaos Engineering
experiments against a Cloud Foundry instance using the
[Chaos Toolkit][chaostoolkit].

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install -U chaostoolkit-cloud-foundry
```

## Usage

To use the probes and actions from this package, add a similar payload to your
experiment file:

```json
{
    "type": "action",
    "name": "terminate-random-instance",
    "provider": {
        "type": "python",
        "module": "chaoscf.probes",
        "func": "terminate_some_random_instance",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
},
{
    "type": "probe",
    "name": "fetch-app-statistics",
    "provider": {
        "type": "python",
        "module": "chaoscf.probes",
        "func": "get_app_stats",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
}
```

That's it!

Please explore the code to see existing probes and actions.

### Discovery

You may use the Chaos Toolkit to discover the capabilities of this extension:

```
$ chaos discover chaostoolkit-cloud-foundry --no-install
```

If you have logged in against a Cloud Foundry environment, this will discover
information about it along the way.

## Configuration

This extension to the Chaos Toolkit need credentials to a Cloud Foundry account
with appropriate scopes. Please add the following sections to your experiment
file:

```json
{
    "configuration": {
        "cf_api_url": "https://api.local.pcfdev.io",
        "cf_verify_ssl": false
    },
    "secrets": {
        "cloudfoundry": {
            "cf_username": "user",
            "cf_password": "pass"
        }
    }
}
```

You may leave `"cf_verifiy_ssl"` out of the configuration when you want to
verify TLS certificates. Usually, local environments are self-signed so it
may be useful to disable that check in that case.

You may also specify the `"cf_client_id"` and `"cf_client_secret"` secrets
when you need. Their default values are `"cf"` and `""` respectively. These
work well against a local [PCF dev][pcfdev] install.

[pcfdev]: https://pivotal.io/pcf-dev

Then in your probe or action:

```json
{
    "type": "probe",
    "name": "fetch-app-statistics",
    "provider": {
        "type": "python",
        "secrets": ["cloudfoundry"],
        "module": "chaoscf.probes",
        "func": "get_app_stats",
        "arguments": {
            "name": "my-app",
            "org_name": "my-org",
            "space_name": "my-space"
        }
    }
}
```


## Test

To run the tests for the project execute the following:

```
$ pip install -r requirements-dev.txt
$ pytest
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit project requires all contributors must sign a
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
$ python setup.py test
```




## Exported Activities



### actions



***

#### `delete_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | delete_app |
| **Return**              | None |


Delete application.

See https://apidocs.cloudfoundry.org/280/apps/delete_a_particular_app.html

**Signature:**

```python
('def delete_app(app_name: str,\n               configuration: Dict[str, Dict[str, str]],\n               secrets: Dict[str, Dict[str, str]],\n               org_name: str = None,\n               space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "delete-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "delete_app",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: delete-app
provider:
  arguments:
    app_name: ''
  func: delete_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `map_route_to_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | map_route_to_app |
| **Return**              | list |


Map a specific route to a given application.

As Domains are deprecated in the Cloud Foundry API, they are not
specified here.
See
https://apidocs.cloudfoundry.org/280/#domains--deprecated-
See
https://www.cloudfoundry.org/blog/coming-changes-app-manifest-simplification/

See
https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html

**Signature:**

```python
('def map_route_to_app(app_name: str,\n                     host_name: str,\n                     configuration: Dict[str, Dict[str, str]],\n                     secrets: Dict[str, Dict[str, str]],\n                     org_name: str = None,\n                     space_name: str = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **host_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "map-route-to-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "map_route_to_app",
    "arguments": {
      "app_name": "",
      "host_name": ""
    }
  }
}
```

```yaml
name: map-route-to-app
provider:
  arguments:
    app_name: ''
    host_name: ''
  func: map_route_to_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `remove_routes_from_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | remove_routes_from_app |
| **Return**              | None |


Remove routes from a given application.

See
https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html

**Signature:**

```python
('def remove_routes_from_app(app_name: str,\n                           route_host: str,\n                           configuration: Dict[str, Dict[str, str]],\n                           secrets: Dict[str, Dict[str, str]],\n                           org_name: str = None,\n                           space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **route_host**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "remove-routes-from-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "remove_routes_from_app",
    "arguments": {
      "app_name": "",
      "route_host": ""
    }
  }
}
```

```yaml
name: remove-routes-from-app
provider:
  arguments:
    app_name: ''
    route_host: ''
  func: remove_routes_from_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `start_all_apps`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | start_all_apps |
| **Return**              | None |


Start all applications for the specified org name

See https://apidocs.cloudfoundry.org/280/apps/updating_an_app.html

**Signature:**

```python
('def start_all_apps(org_name: str, configuration: Dict[str, Dict[str, str]],\n                   secrets: Dict[str, Dict[str, str]]):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **org_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "start-all-apps",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "start_all_apps",
    "arguments": {
      "org_name": ""
    }
  }
}
```

```yaml
name: start-all-apps
provider:
  arguments:
    org_name: ''
  func: start_all_apps
  module: chaoscf.actions
  type: python
type: action

```



***

#### `start_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | start_app |
| **Return**              | None |


Start application

See https://apidocs.cloudfoundry.org/280/apps/updating_an_app.html

**Signature:**

```python
('def start_app(app_name: str,\n              configuration: Dict[str, Dict[str, str]],\n              secrets: Dict[str, Dict[str, str]],\n              org_name: str = None,\n              space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "start-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "start_app",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: start-app
provider:
  arguments:
    app_name: ''
  func: start_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `stop_all_apps`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | stop_all_apps |
| **Return**              | None |


Stop all application for the specified org name

See https://apidocs.cloudfoundry.org/280/apps/updating_an_app.html

**Signature:**

```python
('def stop_all_apps(org_name: str, configuration: Dict[str, Dict[str, str]],\n                  secrets: Dict[str, Dict[str, str]]):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **org_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "stop-all-apps",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "stop_all_apps",
    "arguments": {
      "org_name": ""
    }
  }
}
```

```yaml
name: stop-all-apps
provider:
  arguments:
    org_name: ''
  func: stop_all_apps
  module: chaoscf.actions
  type: python
type: action

```



***

#### `stop_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | stop_app |
| **Return**              | None |


Stop application

See https://apidocs.cloudfoundry.org/280/apps/updating_an_app.html

**Signature:**

```python
('def stop_app(app_name: str,\n             configuration: Dict[str, Dict[str, str]],\n             secrets: Dict[str, Dict[str, str]],\n             org_name: str = None,\n             space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "stop-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "stop_app",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: stop-app
provider:
  arguments:
    app_name: ''
  func: stop_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `terminate_app_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | terminate_app_instance |
| **Return**              | None |


Terminate the application's instance at the given index.

See
https://apidocs.cloudfoundry.org/280/apps/terminate_the_running_app_instance_at_the_given_index.html

**Signature:**

```python
('def terminate_app_instance(app_name: str,\n                           instance_index: int,\n                           configuration: Dict[str, Dict[str, str]],\n                           secrets: Dict[str, Dict[str, str]],\n                           org_name: str = None,\n                           space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **instance_index**      | integer |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "terminate-app-instance",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "terminate_app_instance",
    "arguments": {
      "app_name": "",
      "instance_index": 0
    }
  }
}
```

```yaml
name: terminate-app-instance
provider:
  arguments:
    app_name: ''
    instance_index: 0
  func: terminate_app_instance
  module: chaoscf.actions
  type: python
type: action

```



***

#### `terminate_some_random_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | terminate_some_random_instance |
| **Return**              | None |


Terminate a random application's instance.

See
https://apidocs.cloudfoundry.org/280/apps/terminate_the_running_app_instance_at_the_given_index.html

**Signature:**

```python
('def terminate_some_random_instance(app_name: str,\n                                   configuration: Dict[str, Dict[str, str]],\n                                   secrets: Dict[str, Dict[str, str]],\n                                   org_name: str = None,\n                                   space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "terminate-some-random-instance",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "terminate_some_random_instance",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: terminate-some-random-instance
provider:
  arguments:
    app_name: ''
  func: terminate_some_random_instance
  module: chaoscf.actions
  type: python
type: action

```



***

#### `unbind_service_from_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | unbind_service_from_app |
| **Return**              | None |


Unbind the service from the given application.

See
https://apidocs.cloudfoundry.org/280/service_bindings/delete_a_particular_service_binding.html

**Signature:**

```python
('def unbind_service_from_app(app_name: str,\n                            bind_name: str,\n                            configuration: Dict[str, Dict[str, str]],\n                            secrets: Dict[str, Dict[str, str]],\n                            org_name: str = None,\n                            space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **bind_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "unbind-service-from-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "unbind_service_from_app",
    "arguments": {
      "app_name": "",
      "bind_name": ""
    }
  }
}
```

```yaml
name: unbind-service-from-app
provider:
  arguments:
    app_name: ''
    bind_name: ''
  func: unbind_service_from_app
  module: chaoscf.actions
  type: python
type: action

```



***

#### `unmap_route_from_app`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaoscf.actions |
| **Name**              | unmap_route_from_app |
| **Return**              | None |


Unmap a specific route from a given application.

As Domains are deprecated in the Cloud Foundry API, they are not
specified here.
See
https://apidocs.cloudfoundry.org/280/#domains--deprecated-
See
https://www.cloudfoundry.org/blog/coming-changes-app-manifest-simplification/

See
https://apidocs.cloudfoundry.org/280/apps/remove_route_from_the_app.html

**Signature:**

```python
('def unmap_route_from_app(app_name: str,\n                         host_name: str,\n                         configuration: Dict[str, Dict[str, str]],\n                         secrets: Dict[str, Dict[str, str]],\n                         org_name: str = None,\n                         space_name: str = None):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **host_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "unmap-route-from-app",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaoscf.actions",
    "func": "unmap_route_from_app",
    "arguments": {
      "app_name": "",
      "host_name": ""
    }
  }
}
```

```yaml
name: unmap-route-from-app
provider:
  arguments:
    app_name: ''
    host_name: ''
  func: unmap_route_from_app
  module: chaoscf.actions
  type: python
type: action

```




### api



***

#### `call_api`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | call_api |
| **Return**              | requests.models.Response |


Perform a Cloud Foundry API call and return the full response to the
caller.

**Signature:**

```python
("def call_api(path: str,\n             configuration: Dict[str, Dict[str, str]],\n             secrets: Dict[str, Dict[str, str]],\n             query: Dict[str, Any] = None,\n             body: Dict[str, Any] = None,\n             method: str = 'GET',\n             headers: Dict[str, str] = None) -> requests.models.Response:\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **path**      | string |  | Yes |
| **query**      | mapping | null | No |
| **body**      | mapping | null | No |
| **method**      | string | "GET" | No |
| **headers**      | mapping | null | No |




**Usage:**

```json
{
  "name": "call-api",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "call_api",
    "arguments": {
      "path": ""
    }
  }
}
```

```yaml
name: call-api
provider:
  arguments:
    path: ''
  func: call_api
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_app_by_name`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_app_by_name |
| **Return**              | mapping |


Get the application with the given name.

You may restrict the search by organization and/or space by providing the
various according parameters. When passing the names, the function performs
a lookup for each of them to fetch their GUID.

See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html

**Signature:**

```python
('def get_app_by_name(app_name: str,\n                    configuration: Dict[str, Dict[str, str]],\n                    secrets: Dict[str, Dict[str, str]],\n                    space_name: str = None,\n                    space_guid: str = None,\n                    org_name: str = None,\n                    org_guid: str = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **space_name**      | string | null | No |
| **space_guid**      | string | null | No |
| **org_name**      | string | null | No |
| **org_guid**      | string | null | No |




**Usage:**

```json
{
  "name": "get-app-by-name",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_app_by_name",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: get-app-by-name
provider:
  arguments:
    app_name: ''
  func: get_app_by_name
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_app_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_app_instances |
| **Return**              | mapping |


Get all the instances of a started application.

See https://apidocs.cloudfoundry.org/280/apps/get_the_instance_information_for_a_started_app.html

**Signature:**

```python
('def get_app_instances(app_name: str,\n                      configuration: Dict[str, Dict[str, str]],\n                      secrets: Dict[str, Dict[str, str]],\n                      space_name: str = None,\n                      space_guid: str = None,\n                      org_name: str = None,\n                      org_guid: str = None) -> Dict[str, Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **space_name**      | string | null | No |
| **space_guid**      | string | null | No |
| **org_name**      | string | null | No |
| **org_guid**      | string | null | No |




**Usage:**

```json
{
  "name": "get-app-instances",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_app_instances",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: get-app-instances
provider:
  arguments:
    app_name: ''
  func: get_app_instances
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_app_routes_by_host`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_app_routes_by_host |
| **Return**              | list |


Get all routes associated with the provided app and the given host.

See https://apidocs.cloudfoundry.org/280/routes/list_all_routes.html

**Signature:**

```python
('def get_app_routes_by_host(app_name: str,\n                           route_host: str,\n                           configuration: Dict[str, Dict[str, str]],\n                           secrets: Dict[str, Dict[str, str]],\n                           space_name: str = None,\n                           space_guid: str = None,\n                           org_name: str = None,\n                           org_guid: str = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **route_host**      | string |  | Yes |
| **space_name**      | string | null | No |
| **space_guid**      | string | null | No |
| **org_name**      | string | null | No |
| **org_guid**      | string | null | No |




**Usage:**

```json
{
  "name": "get-app-routes-by-host",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_app_routes_by_host",
    "arguments": {
      "app_name": "",
      "route_host": ""
    }
  }
}
```

```yaml
name: get-app-routes-by-host
provider:
  arguments:
    app_name: ''
    route_host: ''
  func: get_app_routes_by_host
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_apps_for_org`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_apps_for_org |
| **Return**              | None |


List all applications available in the specified CF org name.

See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html to
understand the content of the response.

**Signature:**

```python
('def get_apps_for_org(org_name: str, configuration: Dict[str, Dict[str, str]],\n                     secrets: Dict[str, Dict[str, str]]):\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **org_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "get-apps-for-org",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_apps_for_org",
    "arguments": {
      "org_name": ""
    }
  }
}
```

```yaml
name: get-apps-for-org
provider:
  arguments:
    org_name: ''
  func: get_apps_for_org
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_bind_by_name`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_bind_by_name |
| **Return**              | mapping |


Get the service bind with the given name.

You may restrict the search by organization and/or space by providing the
various according parameters. When passing the names, the function performs
a lookup for each of them to fetch their GUID.

See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html

**Signature:**

```python
('def get_bind_by_name(bind_name: str,\n                     configuration: Dict[str, Dict[str, str]],\n                     secrets: Dict[str, Dict[str, str]],\n                     app_name: str = None,\n                     space_name: str = None,\n                     space_guid: str = None,\n                     org_name: str = None,\n                     org_guid: str = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bind_name**      | string |  | Yes |
| **app_name**      | string | null | No |
| **space_name**      | string | null | No |
| **space_guid**      | string | null | No |
| **org_name**      | string | null | No |
| **org_guid**      | string | null | No |




**Usage:**

```json
{
  "name": "get-bind-by-name",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_bind_by_name",
    "arguments": {
      "bind_name": ""
    }
  }
}
```

```yaml
name: get-bind-by-name
provider:
  arguments:
    bind_name: ''
  func: get_bind_by_name
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_org_by_name`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_org_by_name |
| **Return**              | mapping |


Get the organization with the given name.

**Signature:**

```python
('def get_org_by_name(org_name: str, configuration: Dict[str, Dict[str, str]],\n                    secrets: Dict[str, Dict[str, str]]) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **org_name**      | string |  | Yes |




**Usage:**

```json
{
  "name": "get-org-by-name",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_org_by_name",
    "arguments": {
      "org_name": ""
    }
  }
}
```

```yaml
name: get-org-by-name
provider:
  arguments:
    org_name: ''
  func: get_org_by_name
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_routes_by_host`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_routes_by_host |
| **Return**              | mapping |


Get all routes with given host.

See https://apidocs.cloudfoundry.org/280/routes/list_all_routes.html

**Signature:**

```python
('def get_routes_by_host(route_host: str,\n                       configuration: Dict[str, Dict[str, str]],\n                       secrets: Dict[str, Dict[str, str]],\n                       org_name: str = None,\n                       org_guid: str = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **route_host**      | string |  | Yes |
| **org_name**      | string | null | No |
| **org_guid**      | string | null | No |




**Usage:**

```json
{
  "name": "get-routes-by-host",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_routes_by_host",
    "arguments": {
      "route_host": ""
    }
  }
}
```

```yaml
name: get-routes-by-host
provider:
  arguments:
    route_host: ''
  func: get_routes_by_host
  module: chaoscf.api
  type: python
type: ''

```



***

#### `get_space_by_name`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoscf.api |
| **Name**              | get_space_by_name |
| **Return**              | mapping |


Get the space with the given name.

You may restrict the search by organization by providing the
various according parameters. When passing the name, the function performs
a lookup for the org to fetch its GUID.

**Signature:**

```python
('def get_space_by_name(space_name: str,\n                      configuration: Dict[str, Dict[str, str]],\n                      secrets: Dict[str, Dict[str, str]],\n                      org_name: str = None,\n                      org_guid=None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **space_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **org_guid**      |  | null | No |




**Usage:**

```json
{
  "name": "get-space-by-name",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoscf.api",
    "func": "get_space_by_name",
    "arguments": {
      "space_name": ""
    }
  }
}
```

```yaml
name: get-space-by-name
provider:
  arguments:
    space_name: ''
  func: get_space_by_name
  module: chaoscf.api
  type: python
type: ''

```




### probes



***

#### `get_app_stats`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaoscf.probes |
| **Name**              | get_app_stats |
| **Return**              | mapping |


Fetch the metrics of the given application.

See https://apidocs.cloudfoundry.org/280/apps/get_detailed_stats_for_a_started_app.html
for more information.

**Signature:**

```python
('def get_app_stats(app_name: str,\n                  configuration: Dict[str, Dict[str, str]],\n                  secrets: Dict[str, Dict[str, str]],\n                  org_name: str = None,\n                  space_name: str = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **app_name**      | string |  | Yes |
| **org_name**      | string | null | No |
| **space_name**      | string | null | No |




**Usage:**

```json
{
  "name": "get-app-stats",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaoscf.probes",
    "func": "get_app_stats",
    "arguments": {
      "app_name": ""
    }
  }
}
```

```yaml
name: get-app-stats
provider:
  arguments:
    app_name: ''
  func: get_app_stats
  module: chaoscf.probes
  type: python
type: probe

```



***

#### `list_apps`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaoscf.probes |
| **Name**              | list_apps |
| **Return**              | mapping |


List all applications available to the authorized user.

See https://apidocs.cloudfoundry.org/280/apps/list_all_apps.html to
understand the content of the response.

**Signature:**

```python
('def list_apps(configuration: Dict[str, Dict[str, str]],\n              secrets: Dict[str, Dict[str, str]]) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |




**Usage:**

```json
{
  "name": "list-apps",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaoscf.probes",
    "func": "list_apps"
  }
}
```

```yaml
name: list-apps
provider:
  func: list_apps
  module: chaoscf.probes
  type: python
type: probe

```



