# Extension `chaosk8s`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.26.3 |
| **Repository**        | https://github.com/chaostoolkit/chaostoolkit-kubernetes |



[![PyPI](https://img.shields.io/pypi/v/rsa.svg)](https://pypi.org/project/rsa/)
[![Build Status](https://travis-ci.org/sybrenstuvel/python-rsa.svg?branch=master)](https://travis-ci.org/sybrenstuvel/python-rsa)
[![Coverage Status](https://coveralls.io/repos/github/sybrenstuvel/python-rsa/badge.svg?branch=master)](https://coveralls.io/github/sybrenstuvel/python-rsa?branch=master)
[![Code Climate](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)

[Python-RSA](https://stuvel.eu/rsa) is a pure-Python RSA implementation. It supports
encryption and decryption, signing and verifying signatures, and key
generation according to PKCS#1 version 1.5. It can be used as a Python
library as well as on the commandline. The code was mostly written by
Sybren A.  Stüvel.

Documentation can be found at the [Python-RSA homepage](https://stuvel.eu/rsa). For all changes, check [the changelog](https://github.com/sybrenstuvel/python-rsa/blob/master/CHANGELOG.md).

Download and install using:

    pip install rsa

or download it from the [Python Package Index](https://pypi.org/project/rsa/).

The source code is maintained at [GitHub](https://github.com/sybrenstuvel/python-rsa/) and is
licensed under the [Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Security

Because of how Python internally stores numbers, it is very hard (if not impossible) to make a pure-Python program secure against timing attacks. This library is no exception, so use it with care. See https://securitypitfalls.wordpress.com/2018/08/03/constant-time-compare-in-python/ for more info.

## Setup of Development Environment

```
python3 -m venv .venv
. ./.venv/bin/activate
pip install poetry
poetry install
```

## Publishing a New Release

```
. ./.venv/bin/activate
poetry publish --build
```






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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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




### crd



***

#### `create_cluster_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | create_cluster_custom_object |
| **Return**              | mapping |


Delete a custom object in the given namespace.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def create_cluster_custom_object(
        group: str,
        version: str,
        plural: str,
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-cluster-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "create_cluster_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-cluster-custom-object
    provider:
      arguments:
        group: ''
        plural: ''
        version: ''
      func: create_cluster_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `create_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | create_custom_object |
| **Return**              | mapping |


Create a custom object in the given namespace. Its custom resource
definition must already exists or this will fail with a 404.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def create_custom_object(
        group: str,
        version: str,
        plural: str,
        ns: str = 'default',
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "create_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-custom-object
    provider:
      arguments:
        group: ''
        plural: ''
        version: ''
      func: create_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `delete_cluster_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | delete_cluster_custom_object |
| **Return**              | mapping |


Delete a custom object cluster wide.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def delete_cluster_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-cluster-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "delete_cluster_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-cluster-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: delete_cluster_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `delete_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | delete_custom_object |
| **Return**              | mapping |


Create a custom object cluster wide. Its custom resource
definition must already exists or this will fail with a 404.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def delete_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        ns: str = 'default',
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "delete_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: delete_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `get_cluster_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.crd.probes |
| **Name**              | get_cluster_custom_object |
| **Return**              | mapping |


Get a custom object cluster-wide.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def get_cluster_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-cluster-custom-object",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.probes",
        "func": "get_cluster_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-cluster-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: get_cluster_custom_object
      module: chaosk8s.crd.probes
      type: python
    type: probe
    

    ```



***

#### `get_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.crd.probes |
| **Name**              | get_custom_object |
| **Return**              | mapping |


Get a custom object in the given namespace.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def get_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        ns: str = 'default',
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-custom-object",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.probes",
        "func": "get_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: get_custom_object
      module: chaosk8s.crd.probes
      type: python
    type: probe
    

    ```



***

#### `list_cluster_custom_objects`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.crd.probes |
| **Name**              | list_cluster_custom_objects |
| **Return**              | list |


List custom objects cluster-wide.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def list_cluster_custom_objects(
        group: str,
        version: str,
        plural: str,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-cluster-custom-objects",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.probes",
        "func": "list_cluster_custom_objects",
        "arguments": {
          "group": "",
          "version": "",
          "plural": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-cluster-custom-objects
    provider:
      arguments:
        group: ''
        plural: ''
        version: ''
      func: list_cluster_custom_objects
      module: chaosk8s.crd.probes
      type: python
    type: probe
    

    ```



***

#### `list_custom_objects`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.crd.probes |
| **Name**              | list_custom_objects |
| **Return**              | list |


List custom objects in the given namespace.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def list_custom_objects(
        group: str,
        version: str,
        plural: str,
        ns: str = 'default',
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-custom-objects",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.probes",
        "func": "list_custom_objects",
        "arguments": {
          "group": "",
          "version": "",
          "plural": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-custom-objects
    provider:
      arguments:
        group: ''
        plural: ''
        version: ''
      func: list_custom_objects
      module: chaosk8s.crd.probes
      type: python
    type: probe
    

    ```



***

#### `patch_cluster_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | patch_cluster_custom_object |
| **Return**              | mapping |


Patch a custom object cluster-wide. The resource must be the
updated version to apply. Force will re-acquire conflicting fields
owned by others.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def patch_cluster_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        force: bool = False,
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **force**      | boolean | false | No |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "patch-cluster-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "patch_cluster_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: patch-cluster-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: patch_cluster_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `patch_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | patch_custom_object |
| **Return**              | mapping |


Patch a custom object in the given namespace. The resource must be the
updated version to apply. Force will re-acquire conflicting fields
owned by others.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def patch_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        ns: str = 'default',
        force: bool = False,
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **force**      | boolean | false | No |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "patch-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "patch_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: patch-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: patch_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `replace_cluster_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | replace_cluster_custom_object |
| **Return**              | mapping |


Replace a custom object in the given namespace. The resource must be the
new version to apply.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def replace_cluster_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        force: bool = False,
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **force**      | boolean | false | No |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "replace-cluster-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "replace_cluster_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: replace-cluster-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: replace_cluster_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```



***

#### `replace_custom_object`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.crd.actions |
| **Name**              | replace_custom_object |
| **Return**              | mapping |


Replace a custom object in the given namespace. The resource must be the
new version to apply.

Read more about custom resources here:
https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

**Signature:**

```python
def replace_custom_object(
        group: str,
        version: str,
        plural: str,
        name: str,
        ns: str = 'default',
        force: bool = False,
        resource: Dict[str, Any] = None,
        resource_as_yaml_file: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **group**      | string |  | Yes |
| **version**      | string |  | Yes |
| **plural**      | string |  | Yes |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **force**      | boolean | false | No |
| **resource**      | mapping | null | No |
| **resource_as_yaml_file**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "replace-custom-object",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.crd.actions",
        "func": "replace_custom_object",
        "arguments": {
          "group": "",
          "version": "",
          "plural": "",
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: replace-custom-object
    provider:
      arguments:
        group: ''
        name: ''
        plural: ''
        version: ''
      func: replace_custom_object
      module: chaosk8s.crd.actions
      type: python
    type: action
    

    ```




### deployment



***

#### `create_deployment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.deployment.actions |
| **Name**              | create_deployment |
| **Return**              | None |


Create a deployment described by the deployment config, which must be the
path to the JSON or YAML representation of the deployment.

**Signature:**

```python
def create_deployment(spec_path: str,
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

=== "JSON"
    ```json

    {
      "name": "create-deployment",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.actions",
        "func": "create_deployment",
        "arguments": {
          "spec_path": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-deployment
    provider:
      arguments:
        spec_path: ''
      func: create_deployment
      module: chaosk8s.deployment.actions
      type: python
    type: action
    

    ```



***

#### `delete_deployment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.deployment.actions |
| **Name**              | delete_deployment |
| **Return**              | None |


Delete a deployment by `name` or `label_selector` in the namespace `ns`.

The deployment is deleted without a graceful period to trigger an abrupt
termination.

If neither `name` nor `label_selector` is specified, all the deployments
will be deleted in the namespace.

**Signature:**

```python
def delete_deployment(name: str = None,
                      ns: str = 'default',
                      label_selector: str = None,
                      secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-deployment",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.actions",
        "func": "delete_deployment"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-deployment
    provider:
      func: delete_deployment
      module: chaosk8s.deployment.actions
      type: python
    type: action
    

    ```



***

#### `deployment_available_and_healthy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.deployment.probes |
| **Name**              | deployment_available_and_healthy |
| **Return**              | Optional[bool] |


Lookup a deployment by `name` in the namespace `ns`.

The selected resources are matched by the given `label_selector`.

Raises :exc:`chaoslib.exceptions.ActivityFailed` when the state is not
as expected.

**Signature:**

```python
def deployment_available_and_healthy(
        name: str,
        ns: str = 'default',
        label_selector: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Optional[bool]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deployment-available-and-healthy",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.probes",
        "func": "deployment_available_and_healthy",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deployment-available-and-healthy
    provider:
      arguments:
        name: ''
      func: deployment_available_and_healthy
      module: chaosk8s.deployment.probes
      type: python
    type: probe
    

    ```



***

#### `deployment_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.deployment.probes |
| **Name**              | deployment_fully_available |
| **Return**              | Optional[bool] |


Wait until all the deployment expected replicas are available.
Once this state is reached, return `True`.
If the state is not reached after `timeout` seconds, a
:exc:`chaoslib.exceptions.ActivityFailed` exception is raised.

**Signature:**

```python
def deployment_fully_available(
        name: str,
        ns: str = 'default',
        label_selector: str = None,
        timeout: int = 30,
        secrets: Dict[str, Dict[str, str]] = None) -> Optional[bool]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deployment-fully-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.probes",
        "func": "deployment_fully_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deployment-fully-available
    provider:
      arguments:
        name: ''
      func: deployment_fully_available
      module: chaosk8s.deployment.probes
      type: python
    type: probe
    

    ```



***

#### `deployment_not_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.deployment.probes |
| **Name**              | deployment_not_fully_available |
| **Return**              | Optional[bool] |


Wait until the deployment gets into an intermediate state where not all
expected replicas are available. Once this state is reached, return `True`.
If the state is not reached after `timeout` seconds, a
:exc:`chaoslib.exceptions.ActivityFailed` exception is raised.

**Signature:**

```python
def deployment_not_fully_available(
        name: str,
        ns: str = 'default',
        label_selector: str = None,
        timeout: int = 30,
        secrets: Dict[str, Dict[str, str]] = None) -> Optional[bool]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deployment-not-fully-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.probes",
        "func": "deployment_not_fully_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deployment-not-fully-available
    provider:
      arguments:
        name: ''
      func: deployment_not_fully_available
      module: chaosk8s.deployment.probes
      type: python
    type: probe
    

    ```



***

#### `deployment_partially_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.deployment.probes |
| **Name**              | deployment_partially_available |
| **Return**              | Optional[bool] |


Check whether if the given deployment state is ready or at-least partially
ready.
Raises :exc:`chaoslib.exceptions.ActivityFailed` when the state is not
as expected.

**Signature:**

```python
def deployment_partially_available(
        name: str,
        ns: str = 'default',
        label_selector: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Optional[bool]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deployment-partially-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.probes",
        "func": "deployment_partially_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deployment-partially-available
    provider:
      arguments:
        name: ''
      func: deployment_partially_available
      module: chaosk8s.deployment.probes
      type: python
    type: probe
    

    ```



***

#### `scale_deployment`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.deployment.actions |
| **Name**              | scale_deployment |
| **Return**              | None |


Scale a deployment up or down. The `name` is the name of the deployment.

**Signature:**

```python
def scale_deployment(name: str,
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

=== "JSON"
    ```json

    {
      "name": "scale-deployment",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.deployment.actions",
        "func": "scale_deployment",
        "arguments": {
          "name": "",
          "replicas": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: scale-deployment
    provider:
      arguments:
        name: ''
        replicas: 0
      func: scale_deployment
      module: chaosk8s.deployment.actions
      type: python
    type: action
    

    ```




### networking



***

#### `allow_dns_access`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | allow_dns_access |
| **Return**              | None |


Convenient helper rule to DNS access from all pods
in a namespace, unless `label_selectors, in which case, only matching pods
will be impacted.

**Signature:**

```python
def allow_dns_access(label_selectors: Dict[str, Any] = None,
                     ns: str = 'default',
                     secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selectors**      | mapping | null | No |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "allow-dns-access",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "allow_dns_access"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: allow-dns-access
    provider:
      func: allow_dns_access
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `create_network_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | create_network_policy |
| **Return**              | None |


Create a network policy in the given namespace eitehr from the definition
as `spec` or from a file containing the definition at `spec_path`.

**Signature:**

```python
def create_network_policy(spec: Dict[str, Any] = None,
                          spec_path: str = None,
                          ns: str = 'default',
                          secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **spec**      | mapping | null | No |
| **spec_path**      | string | null | No |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-network-policy",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "create_network_policy"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-network-policy
    provider:
      func: create_network_policy
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `deny_all_egress`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | deny_all_egress |
| **Return**              | None |


Convenient helper rule to deny all egress network from all pods in a
namespace, unless `label_selectors, in which case, only matching pods will
be impacted.

**Signature:**

```python
def deny_all_egress(label_selectors: Dict[str, Any] = None,
                    ns: str = 'default',
                    secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selectors**      | mapping | null | No |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deny-all-egress",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "deny_all_egress"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deny-all-egress
    provider:
      func: deny_all_egress
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `deny_all_ingress`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | deny_all_ingress |
| **Return**              | None |


Convenient helper policy to deny ingress network to all pods in a
namespace, unless `label_selectors, in which case, only matching pods will
be impacted.

**Signature:**

```python
def deny_all_ingress(label_selectors: Dict[str, Any] = None,
                     ns: str = 'default',
                     secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selectors**      | mapping | null | No |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deny-all-ingress",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "deny_all_ingress"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deny-all-ingress
    provider:
      func: deny_all_ingress
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `remove_allow_dns_access`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | remove_allow_dns_access |
| **Return**              | None |


Remove the rule set by the `allow_dns_access` action.

**Signature:**

```python
def remove_allow_dns_access(ns: str = 'default',
                            secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "remove-allow-dns-access",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "remove_allow_dns_access"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-allow-dns-access
    provider:
      func: remove_allow_dns_access
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `remove_deny_all_egress`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | remove_deny_all_egress |
| **Return**              | None |


Remove the rule set by the `deny_all_egress` action.

**Signature:**

```python
def remove_deny_all_egress(ns: str = 'default',
                           secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "remove-deny-all-egress",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "remove_deny_all_egress"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-deny-all-egress
    provider:
      func: remove_deny_all_egress
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `remove_deny_all_ingress`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | remove_deny_all_ingress |
| **Return**              | None |


Remove the rule set by the `deny_all_ingress` action.

**Signature:**

```python
def remove_deny_all_ingress(ns: str = 'default',
                            secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "remove-deny-all-ingress",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "remove_deny_all_ingress"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-deny-all-ingress
    provider:
      func: remove_deny_all_ingress
      module: chaosk8s.networking.actions
      type: python
    type: action
    

    ```



***

#### `remove_network_policy`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.networking.actions |
| **Name**              | remove_network_policy |
| **Return**              | None |


Create a network policy in the given namespace eitehr from the definition
as `spec` or from a file containing the definition at `spec_path`.

**Signature:**

```python
def remove_network_policy(name: str,
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

=== "JSON"
    ```json

    {
      "name": "remove-network-policy",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.networking.actions",
        "func": "remove_network_policy",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-network-policy
    provider:
      arguments:
        name: ''
      func: remove_network_policy
      module: chaosk8s.networking.actions
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

=== "JSON"
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
=== "YAML"
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
def create_node(
    meta: Dict[str, Any] = None,
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

=== "JSON"
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
=== "YAML"
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
                 secrets: Dict[str, Dict[str, str]] = None,
                 pod_label_selector: str = None,
                 pod_namespace: str = None):
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
| **pod_label_selector**      | string | null | No |
| **pod_namespace**      | string | null | No |




**Usage:**

=== "JSON"
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
=== "YAML"
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
                secrets: Dict[str, Dict[str, str]] = None,
                count: int = None,
                pod_label_selector: str = None,
                pod_namespace: str = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **label_selector**      | string | null | No |
| **delete_pods_with_local_storage**      | boolean | false | No |
| **timeout**      | integer | 120 | No |
| **count**      | integer | null | No |
| **pod_label_selector**      | string | null | No |
| **pod_namespace**      | string | null | No |




**Usage:**

=== "JSON"
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
=== "YAML"
    ```yaml

    name: drain-nodes
    provider:
      func: drain_nodes
      module: chaosk8s.node.actions
      type: python
    type: action
    

    ```



***

#### `get_nodes`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.node.probes |
| **Name**              | get_nodes |
| **Return**              | None |


List all Kubernetes worker nodes in your cluster. You may filter nodes
by specifying a label selector.

**Signature:**

```python
def get_nodes(label_selector: str = None,
              configuration: Dict[str, Dict[str, str]] = None,
              secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-nodes",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.node.probes",
        "func": "get_nodes"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-nodes
    provider:
      func: get_nodes
      module: chaosk8s.node.probes
      type: python
    type: probe
    

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

=== "JSON"
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
=== "YAML"
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

#### `count_min_pods`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | count_min_pods |
| **Return**              | boolean |


Check if minimum number of pods are running.

**Signature:**

```python
def count_min_pods(label_selector: str,
                   phase: str = 'Running',
                   min_count: int = 2,
                   ns: str = 'default',
                   secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string |  | Yes |
| **phase**      | string | "Running" | No |
| **min_count**      | integer | 2 | No |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "count-min-pods",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.pod.probes",
        "func": "count_min_pods",
        "arguments": {
          "label_selector": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: count-min-pods
    provider:
      arguments:
        label_selector: ''
      func: count_min_pods
      module: chaosk8s.pod.probes
      type: python
    type: probe
    

    ```



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

=== "JSON"
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
=== "YAML"
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

#### `exec_in_pods`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.pod.actions |
| **Name**              | exec_in_pods |
| **Return**              | list |


Execute the command `cmd` in the specified pod's container.
Select the appropriate pods by label and/or name patterns.
Whenever a pattern is provided for the name, all pods retrieved will be
filtered out if their name do not match the given pattern.

If neither `label_selector` nor `name_pattern` are provided, all pods
in the namespace will be selected for termination.

If `all` is set to `True`, all matching pods will be affected.

Value of `qty` varies based on `mode`.
If `mode` is set to `fixed`, then `qty` refers to number of pods affected.
If `mode` is set to `percentage`, then `qty` refers to
percentage of pods, from 1 to 100, to be affected.
Default `mode` is `fixed` and default `qty` is `1`.

If `order` is set to `oldest`, the retrieved pods will be ordered
by the pods creation_timestamp, with the oldest pod first in list.

If `rand` is set to `True`, n random pods will be affected
Otherwise, the first retrieved n pods will be used

The `cmd` should be a string or a sequence of program arguments. Providing
a sequence of arguments is generally preferred, as it allows the action to
take care of any required escaping and quoting (e.g. to permit spaces in the
arguments). If passing a single string it will be split automatically.

**Signature:**

```python
def exec_in_pods(
        cmd: Union[str, List[str]],
        label_selector: str = None,
        name_pattern: str = None,
        all: bool = False,
        rand: bool = False,
        mode: str = 'fixed',
        qty: int = 1,
        ns: str = 'default',
        order: str = 'alphabetic',
        container_name: str = None,
        request_timeout: int = 60,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **cmd**      | object |  | Yes |
| **label_selector**      | string | null | No |
| **name_pattern**      | string | null | No |
| **all**      | boolean | false | No |
| **rand**      | boolean | false | No |
| **mode**      | string | "fixed" | No |
| **qty**      | integer | 1 | No |
| **ns**      | string | "default" | No |
| **order**      | string | "alphabetic" | No |
| **container_name**      | string | null | No |
| **request_timeout**      | integer | 60 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "exec-in-pods",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.pod.actions",
        "func": "exec_in_pods",
        "arguments": {
          "cmd": null
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: exec-in-pods
    provider:
      arguments:
        cmd: null
      func: exec_in_pods
      module: chaosk8s.pod.actions
      type: python
    type: action
    

    ```



***

#### `pod_is_not_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | pod_is_not_available |
| **Return**              | boolean |


Lookup pods with a `name` label set to the given `name` in the specified
`ns`.

Raises :exc:`chaoslib.exceptions.ActivityFailed` when one of the pods
with the specified `name` is in the `"Running"` phase.

**Signature:**

```python
def pod_is_not_available(name: str,
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

=== "JSON"
    ```json

    {
      "name": "pod-is-not-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.pod.probes",
        "func": "pod_is_not_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: pod-is-not-available
    provider:
      arguments:
        name: ''
      func: pod_is_not_available
      module: chaosk8s.pod.probes
      type: python
    type: probe
    

    ```



***

#### `pods_in_conditions`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.pod.probes |
| **Name**              | pods_in_conditions |
| **Return**              | boolean |


Lookup a pod by `label_selector` in the namespace `ns`.

Raises :exc:`chaoslib.exceptions.ActivityFailed` if one of the given
conditions type/status is not as expected

**Signature:**

```python
def pods_in_conditions(label_selector: str,
                       conditions: List[Dict[str, str]],
                       ns: str = 'default',
                       secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **label_selector**      | string |  | Yes |
| **conditions**      | list |  | Yes |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "pods-in-conditions",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.pod.probes",
        "func": "pods_in_conditions",
        "arguments": {
          "label_selector": "",
          "conditions": []
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: pods-in-conditions
    provider:
      arguments:
        conditions: []
        label_selector: ''
      func: pods_in_conditions
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

Raises :exc:`chaoslib.exceptions.ActivityFailed` when the state is not
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

=== "JSON"
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
=== "YAML"
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

Raises :exc:`chaoslib.exceptions.ActivityFailed` when the pod is in the
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

=== "JSON"
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
=== "YAML"
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
                  last: Optional[str] = None,
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

=== "JSON"
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
=== "YAML"
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
in the namespace will be selected for termination.

If `all` is set to `True`, all matching pods will be terminated.

Value of `qty` varies based on `mode`.
If `mode` is set to `fixed`, then `qty` refers to number of pods to be
terminated. If `mode` is set to `percentage`, then `qty` refers to
percentage of pods, from 1 to 100, to be terminated.
Default `mode` is `fixed` and default `qty` is `1`.

If `order` is set to `oldest`, the retrieved pods will be ordered
by the pods creation_timestamp, with the oldest pod first in list.

If `rand` is set to `True`, n random pods will be terminated
Otherwise, the first retrieved n pods will be terminated.

If `grace_period` is greater than or equal to 0, it will
be used as the grace period (in seconds) to terminate the pods.
Otherwise, the default pod's grace period will be used.

**Signature:**

```python
def terminate_pods(label_selector: str = None,
                   name_pattern: str = None,
                   all: bool = False,
                   rand: bool = False,
                   mode: str = 'fixed',
                   qty: int = 1,
                   grace_period: int = -1,
                   ns: str = 'default',
                   order: str = 'alphabetic',
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
| **mode**      | string | "fixed" | No |
| **qty**      | integer | 1 | No |
| **grace_period**      | integer | -1 | No |
| **ns**      | string | "default" | No |
| **order**      | string | "alphabetic" | No |




**Usage:**

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

**Signature:**

```python
def all_microservices_healthy(
    ns: str = 'default',
    secrets: Dict[str, Dict[str, str]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **ns**      | string | "default" | No |




**Usage:**

=== "JSON"
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
=== "YAML"
    ```yaml

    name: all-microservices-healthy
    provider:
      func: all_microservices_healthy
      module: chaosk8s.probes
      type: python
    type: probe
    

    ```



***

#### `deployment_is_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.probes |
| **Name**              | deployment_is_fully_available |
| **Return**              | None |


!!!DEPRECATED!!!

**Signature:**

```python
def deployment_is_fully_available(name: str,
                                  ns: str = 'default',
                                  label_selector: str = None,
                                  timeout: int = 30,
                                  secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "deployment-is-fully-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.probes",
        "func": "deployment_is_fully_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: deployment-is-fully-available
    provider:
      arguments:
        name: ''
      func: deployment_is_fully_available
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


!!!DEPRECATED!!!

**Signature:**

```python
def deployment_is_not_fully_available(name: str,
                                      ns: str = 'default',
                                      label_selector: str = None,
                                      timeout: int = 30,
                                      secrets: Dict[str, Dict[str,
                                                              str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
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
=== "YAML"
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
| **Return**              | Optional[bool] |


!!!DEPRECATED!!!

**Signature:**

```python
def microservice_available_and_healthy(
        name: str,
        ns: str = 'default',
        label_selector: str = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Optional[bool]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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
        last: Optional[str] = None,
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

=== "JSON"
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
=== "YAML"
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


!!!DEPRECATED!!!

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

=== "JSON"
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
=== "YAML"
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




### replicaset



***

#### `delete_replica_set`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.replicaset.actions |
| **Name**              | delete_replica_set |
| **Return**              | None |


Delete a replica set by `name` or `label_selector` in the namespace `ns`.

The replica set is deleted without a graceful period to trigger an abrupt
termination.

If neither `name` nor `label_selector` is specified, all the replica sets
will be deleted in the namespace.

**Signature:**

```python
def delete_replica_set(name: str = None,
                       ns: str = 'default',
                       label_selector: str = None,
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-replica-set",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.replicaset.actions",
        "func": "delete_replica_set"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-replica-set
    provider:
      func: delete_replica_set
      module: chaosk8s.replicaset.actions
      type: python
    type: action
    

    ```




### service



***

#### `create_service_endpoint`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.service.actions |
| **Name**              | create_service_endpoint |
| **Return**              | None |


Create a service endpoint described by the service config, which must be
the path to the JSON or YAML representation of the service.

**Signature:**

```python
def create_service_endpoint(spec_path: str,
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

=== "JSON"
    ```json

    {
      "name": "create-service-endpoint",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.service.actions",
        "func": "create_service_endpoint",
        "arguments": {
          "spec_path": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-service-endpoint
    provider:
      arguments:
        spec_path: ''
      func: create_service_endpoint
      module: chaosk8s.service.actions
      type: python
    type: action
    

    ```



***

#### `delete_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.service.actions |
| **Name**              | delete_service |
| **Return**              | None |


Remove the given service

**Signature:**

```python
def delete_service(name: str,
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

=== "JSON"
    ```json

    {
      "name": "delete-service",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.service.actions",
        "func": "delete_service",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-service
    provider:
      arguments:
        name: ''
      func: delete_service
      module: chaosk8s.service.actions
      type: python
    type: action
    

    ```



***

#### `service_is_initialized`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.service.probes |
| **Name**              | service_is_initialized |
| **Return**              | boolean |


Lookup a service endpoint by its name and raises :exc:`FailedProbe` when
the service was not found or not initialized.

**Signature:**

```python
def service_is_initialized(name: str = None,
                           ns: str = 'default',
                           label_selector: str = None,
                           secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "service-is-initialized",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.service.probes",
        "func": "service_is_initialized"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: service-is-initialized
    provider:
      func: service_is_initialized
      module: chaosk8s.service.probes
      type: python
    type: probe
    

    ```




### statefulset



***

#### `create_statefulset`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.statefulset.actions |
| **Name**              | create_statefulset |
| **Return**              | None |


Create a statefulset described by the service config, which must be
the path to the JSON or YAML representation of the statefulset.

**Signature:**

```python
def create_statefulset(spec_path: str,
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

=== "JSON"
    ```json

    {
      "name": "create-statefulset",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.statefulset.actions",
        "func": "create_statefulset",
        "arguments": {
          "spec_path": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-statefulset
    provider:
      arguments:
        spec_path: ''
      func: create_statefulset
      module: chaosk8s.statefulset.actions
      type: python
    type: action
    

    ```



***

#### `remove_statefulset`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.statefulset.actions |
| **Name**              | remove_statefulset |
| **Return**              | None |


Remove a statefulset by `name` or `label_selector` in the namespace `ns`.

The statefulset is removed by deleting it without
    a graceful period to trigger an abrupt termination.

If neither `name` nor `label_selector` is specified, all the statefulsets
will be deleted in the namespace.

**Signature:**

```python
def remove_statefulset(name: str = None,
                       ns: str = 'default',
                       label_selector: str = None,
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string | null | No |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "remove-statefulset",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.statefulset.actions",
        "func": "remove_statefulset"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: remove-statefulset
    provider:
      func: remove_statefulset
      module: chaosk8s.statefulset.actions
      type: python
    type: action
    

    ```



***

#### `scale_statefulset`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosk8s.statefulset.actions |
| **Name**              | scale_statefulset |
| **Return**              | None |


Scale a stateful set up or down. The `name` is the name of the stateful
set.

**Signature:**

```python
def scale_statefulset(name: str,
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

=== "JSON"
    ```json

    {
      "name": "scale-statefulset",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosk8s.statefulset.actions",
        "func": "scale_statefulset",
        "arguments": {
          "name": "",
          "replicas": 0
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: scale-statefulset
    provider:
      arguments:
        name: ''
        replicas: 0
      func: scale_statefulset
      module: chaosk8s.statefulset.actions
      type: python
    type: action
    

    ```



***

#### `statefulset_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.statefulset.probes |
| **Name**              | statefulset_fully_available |
| **Return**              | None |


Wait until all the statefulSet expected replicas are available.
Once this state is reached, return `True`.
If the state is not reached after `timeout` seconds, a
:exc:`chaoslib.exceptions.ActivityFailed` exception is raised.

**Signature:**

```python
def statefulset_fully_available(name: str,
                                ns: str = 'default',
                                label_selector: str = None,
                                timeout: int = 30,
                                secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "statefulset-fully-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.statefulset.probes",
        "func": "statefulset_fully_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: statefulset-fully-available
    provider:
      arguments:
        name: ''
      func: statefulset_fully_available
      module: chaosk8s.statefulset.probes
      type: python
    type: probe
    

    ```



***

#### `statefulset_not_fully_available`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosk8s.statefulset.probes |
| **Name**              | statefulset_not_fully_available |
| **Return**              | None |


Wait until the statefulSet gets into an intermediate state where not all
expected replicas are available. Once this state is reached, return `True`.
If the state is not reached after `timeout` seconds, a
:exc:`chaoslib.exceptions.ActivityFailed` exception is raised.

**Signature:**

```python
def statefulset_not_fully_available(name: str,
                                    ns: str = 'default',
                                    label_selector: str = None,
                                    timeout: int = 30,
                                    secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **ns**      | string | "default" | No |
| **label_selector**      | string | null | No |
| **timeout**      | integer | 30 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "statefulset-not-fully-available",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosk8s.statefulset.probes",
        "func": "statefulset_not_fully_available",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: statefulset-not-fully-available
    provider:
      arguments:
        name: ''
      func: statefulset_not_fully_available
      module: chaosk8s.statefulset.probes
      type: python
    type: probe
    

    ```



