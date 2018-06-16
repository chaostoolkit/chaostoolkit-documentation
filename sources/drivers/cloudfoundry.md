# Extension `chaoscf`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.5.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-cloud-foundry |

N/A

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
def delete_app(app_name: str,
               configuration: Dict[str, Dict[str, str]],
               secrets: Dict[str, Dict[str, str]],
               org_name: str = None,
               space_name: str = None):
    pass

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
def map_route_to_app(app_name: str,
                     host_name: str,
                     configuration: Dict[str, Dict[str, str]],
                     secrets: Dict[str, Dict[str, str]],
                     org_name: str = None,
                     space_name: str = None) -> List[Dict[str, Any]]:
    pass

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
def remove_routes_from_app(app_name: str,
                           route_host: str,
                           configuration: Dict[str, Dict[str, str]],
                           secrets: Dict[str, Dict[str, str]],
                           org_name: str = None,
                           space_name: str = None):
    pass

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
def terminate_app_instance(app_name: str,
                           instance_index: int,
                           configuration: Dict[str, Dict[str, str]],
                           secrets: Dict[str, Dict[str, str]],
                           org_name: str = None,
                           space_name: str = None):
    pass

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
def terminate_some_random_instance(app_name: str,
                                   configuration: Dict[str, Dict[str, str]],
                                   secrets: Dict[str, Dict[str, str]],
                                   org_name: str = None,
                                   space_name: str = None):
    pass

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
def unbind_service_from_app(app_name: str,
                            bind_name: str,
                            configuration: Dict[str, Dict[str, str]],
                            secrets: Dict[str, Dict[str, str]],
                            org_name: str = None,
                            space_name: str = None):
    pass

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
def unmap_route_from_app(app_name: str,
                         host_name: str,
                         configuration: Dict[str, Dict[str, str]],
                         secrets: Dict[str, Dict[str, str]],
                         org_name: str = None,
                         space_name: str = None):
    pass

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
def call_api(path: str,
             configuration: Dict[str, Dict[str, str]],
             secrets: Dict[str, Dict[str, str]],
             query: Dict[str, Any] = None,
             data: Dict[str, Any] = None,
             method: str = 'GET',
             headers: Dict[str, str] = None) -> requests.models.Response:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **path**      | string |  | Yes |
| **query**      | mapping | null | No |
| **data**      | mapping | null | No |
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
def get_app_by_name(app_name: str,
                    configuration: Dict[str, Dict[str, str]],
                    secrets: Dict[str, Dict[str, str]],
                    space_name: str = None,
                    space_guid: str = None,
                    org_name: str = None,
                    org_guid: str = None) -> Dict[str, Any]:
    pass

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
def get_app_instances(app_name: str,
                      configuration: Dict[str, Dict[str, str]],
                      secrets: Dict[str, Dict[str, str]],
                      space_name: str = None,
                      space_guid: str = None,
                      org_name: str = None,
                      org_guid: str = None) -> Dict[str, Dict[str, Any]]:
    pass

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
def get_app_routes_by_host(app_name: str,
                           route_host: str,
                           configuration: Dict[str, Dict[str, str]],
                           secrets: Dict[str, Dict[str, str]],
                           space_name: str = None,
                           space_guid: str = None,
                           org_name: str = None,
                           org_guid: str = None) -> List[Dict[str, Any]]:
    pass

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
def get_bind_by_name(bind_name: str,
                     configuration: Dict[str, Dict[str, str]],
                     secrets: Dict[str, Dict[str, str]],
                     space_name: str = None,
                     space_guid: str = None,
                     org_name: str = None,
                     org_guid: str = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bind_name**      | string |  | Yes |
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
def get_org_by_name(org_name: str, configuration: Dict[str, Dict[str, str]],
                    secrets: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    pass

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
def get_routes_by_host(route_host: str,
                       configuration: Dict[str, Dict[str, str]],
                       secrets: Dict[str, Dict[str, str]],
                       org_name: str = None,
                       org_guid: str = None) -> Dict[str, Any]:
    pass

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
def get_space_by_name(space_name: str,
                      configuration: Dict[str, Dict[str, str]],
                      secrets: Dict[str, Dict[str, str]],
                      org_name: str = None,
                      org_guid=None) -> Dict[str, Any]:
    pass

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
def get_app_stats(app_name: str,
                  configuration: Dict[str, Dict[str, str]],
                  secrets: Dict[str, Dict[str, str]],
                  org_name: str = None,
                  space_name: str = None) -> Dict[str, Any]:
    pass

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
def list_apps(configuration: Dict[str, Dict[str, str]],
              secrets: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    pass

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


