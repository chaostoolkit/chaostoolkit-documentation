# Extension `chaosgcp`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.8.2 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform |



[![Build Status](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform.svg?branch=master)](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-google-cloud-platform.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Google Cloud Platform][gcp].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[gce]: https://cloud.google.com/compute/
[gcp]: https://cloud.google.com


## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install --prefer-binary -U chaostoolkit-google-cloud-platform
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "version": "1.0.0",
    "title": "create and delete a cloud run service",
    "description": "n/a",
    "secrets": {
        "gcp": {
            "service_account_file": "service_account.json"
        }
    },
    "method": [
        {
            "name": "create-cloud-run-service",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudrun.actions",
                "func": "create_service",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/...",
                    "service_id": "demo",
                    "container": {
                        "name": "demo",
                        "image": "gcr.io/google-samples/hello-app:1.0"
                    }
                }
            }
        },
        {
            "name": "delete-cloud-run-service",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudrun.actions",
                "func": "delete_service",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../services/demo"
                }
            }
        }
    ]
}
```

That's it!

Please explore the code to see existing probes and actions.


## Configuration

### Project and Cluster Information

You can pass the context via the `configuration` section of your experiment:

```json
{
    "configuration": {
        "gcp_project_id": "...",
        "gcp_gke_cluster_name": "...",
        "gcp_region": "...",
        "gcp_zone": "..."
    }
}
```

This is only valuable when you want to reuse the same context everywhere.
A finer approach is to set the the `parent` argument on activities that
support it. It should be of the form
`projects/*/locations/*` or `projects/*/locations/*/clusters/*`, where
`location` is either a region or a zone, depending on the context and defined
by the GCP API.

When provided, this takes precedence over the context defined in the
configuration. In some cases, it also means you do not need to pass the
values in the configuration at all as the extension will derive the
context from the `parent` value.

### Credentials

This extension expects a [service account][sa] with enough permissions to
perform its operations. Please create such a service account manually (do not
use the default one for your cluster if you can, so you'll be able to delete
that service account if need be).

[sa]: https://cloud.google.com/iam/docs/creating-managing-service-accounts 

Once you have created your service account, either keep the file on the same
machine where you will be running the experiment from. Or, pass its content
as part of the `secrets` section, although this is not recommended because your
sensitive data will be quite visible.

Here is the first way:

```json
{
    "secrets": {
        "gcp": {
            "service_account_file": "/path/to/sa.json"
        }
    }
}
```

You can also use the well-known `GOOGLE_APPLICATION_CREDENTIALS` environment
variables. iI that case, you do not need to set any secrets in the
experiment.


While the embedded way looks like this:


```json
{
    "secrets": {
        "k8s": {
            "KUBERNETES_CONTEXT": "..."
        },
        "gcp": {
            "service_account_info": {
                "type": "service_account",
                "project_id": "...",
                "private_key_id": "...",
                "private_key": "...",
                "client_email": "...",
                "client_id": "...",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...."
            }
        }
    }
}
```

Notice also how we provided here the `k8s` entry. This is only because, in our
example we use the `swap_nodepool` action which drains the Kubernetes nodes
and it requires the Kubernetes cluster credentials to work. These are documented
in the [Kubernetes extension for Chaos Toolkit][k8sctk]. This is the only
action that requires such a secret payload, others only speak to the GCP API.

[k8sctk]: https://docs.chaostoolkit.org/drivers/kubernetes/

### Putting it all together

Here is a full example which creates a node pool then swap it for a new one.

```json
{
    "version": "1.0.0",
    "title": "do stuff ye",
    "description": "n/a",
    "secrets": {
        "k8s": {
            "KUBERNETES_CONTEXT": "gke_..."
        },
        "gcp": {
            "service_account_file": "service-account.json"
        }
    },
    "method": [
        {
            "name": "create-our-nodepool",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "create_new_nodepool",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/...",
                    "body": {
                        "config": { 
                            "oauth_scopes": [
                                "gke-version-default",
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/trace.append"
                            ]
                        },
                        "initial_node_count": 1,
                        "name": "default-pool"
                    }
                }
            }
        },
        {
            "name": "fetch-our-nodepool",
            "type": "probe",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.probes",
                "func": "get_nodepool",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/.../nodePools/default-pool"
                }
            }
        },
        {
            "name": "swap-our-nodepool",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "swap_nodepool",
                "secrets": ["gcp", "k8s"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/...",
                    "delete_old_node_pool": true,
                    "old_node_pool_id": "default-pool",
                    "new_nodepool_body": {
                        "config": { 
                            "oauth_scopes": [
                                "gke-version-default",
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/trace.append"
                            ]
                        },
                        "initial_node_count": 1,
                        "name": "default-pool-1"
                    }
                }
            }
        }
    ]
}
```


## Migrate from GCE extension

If you previously used the deprecated [GCE extension][ctk-gce], here is a quick
recap of changes you'll need to go through to update your experiments.

[ctk-gce]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud

-   The module `chaosgce.nodepool.actions` has been replaced by
    `chaosgcp.gke.nodepool.actions`.
    You will need to update the `module` key for the python providers.
-   The configuration keys in the `configuration` section have been
    renamed accordingly:
    - `"gce_project_id"` -> `"gcp_project_id"`
    - `"gce_region"` -> `"gcp_region"`
    - `"gce_zone"` -> `"gcp_zone"`
    - `"gce_cluster_name"` -> `"gcp_gke_cluster_name"`

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

If you wish to add a new function to this extension, that is related to a 
Google Cloud product that is not available yet in this package, please use 
the product short name or acronym as a first level subpackage (eg. iam, gke, 
sql, storage, ...). See the list of [GCP products and services][gcp_products].

[gcp_products] https://cloud.google.com/products/

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






## Exported Activities



### cloudbuild



***

#### `get_trigger`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudbuild.probes |
| **Name**              | get_trigger |
| **Return**              | None |


Returns information about a BuildTrigger.

See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/get

:param name: name of the trigger
:param configuration:
:param secrets:
:return:

**Signature:**

```python
def get_trigger(name: str,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None):
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
      "name": "get-trigger",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudbuild.probes",
        "func": "get_trigger",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-trigger
    provider:
      arguments:
        name: ''
      func: get_trigger
      module: chaosgcp.cloudbuild.probes
      type: python
    type: probe
    

    ```



***

#### `list_trigger_names`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudbuild.probes |
| **Name**              | list_trigger_names |
| **Return**              | None |


List only the trigger names of a project

:param configuration:
:param secrets:

:return:

**Signature:**

```python
def list_trigger_names(configuration: Dict[str, Dict[str, str]] = None,
                       secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-trigger-names",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudbuild.probes",
        "func": "list_trigger_names"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-trigger-names
    provider:
      func: list_trigger_names
      module: chaosgcp.cloudbuild.probes
      type: python
    type: probe
    

    ```



***

#### `list_triggers`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudbuild.probes |
| **Name**              | list_triggers |
| **Return**              | None |


Lists existing BuildTriggers.

See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/list

:param configuration:
:param secrets:

:return:

**Signature:**

```python
def list_triggers(configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-triggers",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudbuild.probes",
        "func": "list_triggers"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-triggers
    provider:
      func: list_triggers
      module: chaosgcp.cloudbuild.probes
      type: python
    type: probe
    

    ```



***

#### `run_trigger`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.cloudbuild.actions |
| **Name**              | run_trigger |
| **Return**              | None |


Runs a BuildTrigger at a particular source revision.

NB: The trigger must exist in the targeted project.

See: https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.triggers/run

:param name: name of the trigger
:param source: location of the source in a Google Cloud Source Repository
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def run_trigger(name: str,
                source: Dict[Any, Any],
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **name**      | string |  | Yes |
| **source**      | mapping |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "run-trigger",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudbuild.actions",
        "func": "run_trigger",
        "arguments": {
          "name": "",
          "source": {}
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: run-trigger
    provider:
      arguments:
        name: ''
        source: {}
      func: run_trigger
      module: chaosgcp.cloudbuild.actions
      type: python
    type: action
    

    ```




### cloudrun



***

#### `create_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.cloudrun.actions |
| **Name**              | create_service |
| **Return**              | None |


Deletes a Cloud Run service and all its revisions. Cannot be undone.

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

:param parent: the path to the location in the project 'projects/PROJECT_ID/locations/LOC
:param service_id: unique identifier for the service
:param container: definition of the container as per https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.Container
:param description: optional text description of the service
:param max_instance_request_concurrency: optional maximum number of requests that each serving instance can receive
:param labels: optional labels to set on the service
:param annotations: optional annotations to set on the service
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def create_service(parent: str,
                   service_id: str,
                   container: Dict[str, Any],
                   description: str = None,
                   max_instance_request_concurrency: int = 0,
                   service_account: str = None,
                   encryption_key: str = None,
                   traffic: List[Dict[str, Any]] = None,
                   labels: Dict[str, str] = None,
                   annotations: Dict[str, str] = None,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string |  | Yes |
| **service_id**      | string |  | Yes |
| **container**      | mapping |  | Yes |
| **description**      | string | null | No |
| **max_instance_request_concurrency**      | integer | 0 | No |
| **service_account**      | string | null | No |
| **encryption_key**      | string | null | No |
| **traffic**      | list | null | No |
| **labels**      | mapping | null | No |
| **annotations**      | mapping | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-service",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.actions",
        "func": "create_service",
        "arguments": {
          "parent": "",
          "service_id": "",
          "container": {}
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-service
    provider:
      arguments:
        container: {}
        parent: ''
        service_id: ''
      func: create_service
      module: chaosgcp.cloudrun.actions
      type: python
    type: action
    

    ```



***

#### `delete_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.cloudrun.actions |
| **Name**              | delete_service |
| **Return**              | None |


Deletes a Cloud Run service and all its revisions. Cannot be undone.

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

:param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def delete_service(parent: str,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-service",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.actions",
        "func": "delete_service",
        "arguments": {
          "parent": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-service
    provider:
      arguments:
        parent: ''
      func: delete_service
      module: chaosgcp.cloudrun.actions
      type: python
    type: action
    

    ```



***

#### `get_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudrun.probes |
| **Name**              | get_service |
| **Return**              | mapping |


Retrieve a single cloud run service

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_get_service

:param name: the path to the service 'projects/PROJECT_ID/locations/LOC/services/SVC
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def get_service(name: str,
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
      "name": "get-service",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.probes",
        "func": "get_service",
        "arguments": {
          "name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-service
    provider:
      arguments:
        name: ''
      func: get_service
      module: chaosgcp.cloudrun.probes
      type: python
    type: probe
    

    ```



***

#### `list_service_revisions`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudrun.probes |
| **Name**              | list_service_revisions |
| **Return**              | list |


List all Cloud Run service revisions for a specific service.

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.revisions.RevisionsClient#google_cloud_run_v2_services_revisions_RevisionsClient_list_revisions

:param parent: the path to the service 'projects/PROJECT_ID/locations/LOC/service/SVC
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def list_service_revisions(
        parent: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-service-revisions",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.probes",
        "func": "list_service_revisions",
        "arguments": {
          "parent": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-service-revisions
    provider:
      arguments:
        parent: ''
      func: list_service_revisions
      module: chaosgcp.cloudrun.probes
      type: python
    type: probe
    

    ```



***

#### `list_services`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.cloudrun.probes |
| **Name**              | list_services |
| **Return**              | list |


List all Cloud Run services

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_list_services

:param parent: the path to the service 'projects/PROJECT_ID/locations/LOC
:param configuration:
:param secrets:

:return:

**Signature:**

```python
def list_services(
        parent: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-services",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.probes",
        "func": "list_services",
        "arguments": {
          "parent": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-services
    provider:
      arguments:
        parent: ''
      func: list_services
      module: chaosgcp.cloudrun.probes
      type: python
    type: probe
    

    ```



***

#### `update_service`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.cloudrun.actions |
| **Name**              | update_service |
| **Return**              | None |


Updates a Cloud Run service.

For example:

```json
{
    "name": "route-traffic-two-latest-and-older-revision",
    "type": "action",
    "provider": {
   "type": "python",
   "module": chaosgcp.cloudrun.actions",
   "func": "update_service",
   "arguments": {
  "parent": "projects/${gcp_project_id}/locations/${gcp_location}/services/${service_name}",
  "container": {
 "image": "eu.gcr.io/${gcp_project_id}/demo"
  },
  "traffic": [{
 "type_": 1,
 "percent": 50
  }, {
 "type_": 2,
 "revision": "whatever-w788x",
 "percent": 50
  }],
   }
    }
}
```

See: https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.services.services.ServicesClient#google_cloud_run_v2_services_services_ServicesClient_delete_service

:param container: definition of the container as per https://cloud.google.com/python/docs/reference/run/latest/google.cloud.run_v2.types.Container
:param labels: optional labels to set on the service
:param annotations: optional annotations to set on the service
:param configuration:
:param secrets:
:param vpc_access_config: optional value for vpc_connect

:return:

**Signature:**

```python
def update_service(parent: str,
                   container: Dict[str, Any] = None,
                   max_instance_request_concurrency: int = 100,
                   service_account: str = None,
                   encryption_key: str = None,
                   traffic: List[Dict[str, Any]] = None,
                   labels: Dict[str, str] = None,
                   annotations: Dict[str, str] = None,
                   vpc_access_config: Dict[str, str] = None,
                   configuration: Dict[str, Dict[str, str]] = None,
                   secrets: Dict[str, Dict[str, str]] = None):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string |  | Yes |
| **container**      | mapping | null | No |
| **max_instance_request_concurrency**      | integer | 100 | No |
| **service_account**      | string | null | No |
| **encryption_key**      | string | null | No |
| **traffic**      | list | null | No |
| **labels**      | mapping | null | No |
| **annotations**      | mapping | null | No |
| **vpc_access_config**      | mapping | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "update-service",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.cloudrun.actions",
        "func": "update_service",
        "arguments": {
          "parent": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: update-service
    provider:
      arguments:
        parent: ''
      func: update_service
      module: chaosgcp.cloudrun.actions
      type: python
    type: action
    

    ```




### nodepool



***

#### `create_new_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.gke.nodepool.actions |
| **Name**              | create_new_nodepool |
| **Return**              | mapping |


Create a new node pool in the given cluster/zone of the provided project.

The node pool config must be passed a mapping to the `body` parameter and
respect the REST API.

If `wait_until_complete` is set to `True` (the default), the function
will block until the node pool is ready. Otherwise, will return immediatly
with the operation information.

See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create

**Signature:**

```python
def create_new_nodepool(
        body: Dict[str, Any],
        parent: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **body**      | mapping |  | Yes |
| **parent**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "create-new-nodepool",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "create_new_nodepool",
        "arguments": {
          "body": {}
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: create-new-nodepool
    provider:
      arguments:
        body: {}
      func: create_new_nodepool
      module: chaosgcp.gke.nodepool.actions
      type: python
    type: action
    

    ```



***

#### `delete_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.gke.nodepool.actions |
| **Name**              | delete_nodepool |
| **Return**              | mapping |


Delete node pool from the given cluster/zone of the provided project.

If `wait_until_complete` is set to `True` (the default), the function
will block until the node pool is deleted. Otherwise, will return
immediatly with the operation information.

See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create

**Signature:**

```python
def delete_nodepool(
        parent: str = None,
        node_pool_id: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string | null | No |
| **node_pool_id**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "delete-nodepool",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "delete_nodepool"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: delete-nodepool
    provider:
      func: delete_nodepool
      module: chaosgcp.gke.nodepool.actions
      type: python
    type: action
    

    ```



***

#### `get_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.gke.nodepool.probes |
| **Name**              | get_nodepool |
| **Return**              | mapping |


Get a specific nodepool of a cluster.

The `parent` is following the form
`projects/*/locations/*/clusters/*/nodePools/*`
and will override any settings in the configuration block.

```json
{
    "name": "retrieve-our-nodepool",
    "type": "probe",
    "provider": {
   "type": "python",
   "module": "chaosgcp.gke.nodepool.probes",
   "func": "get_nodepool",
   "secrets": ["gcp"],
   "arguments": {
  "parent": "projects/my-project-89/locations/us-east1/clusters/cluster-1/nodePools/default-pool"
   }
    }
}
```

If not provided this action uses the configuration settings. In that case,
make sure to also pass the `node_pool_id` value.

```json
{
    "name": "retrieve-our-nodepool",
    "type": "probe",
    "provider": {
   "type": "python",
   "module": "chaosgcp.gke.nodepool.probes",
   "func": "get_nodepool",
   "secrets": ["gcp"],
   "arguments": {
  "node_pool_id": "default-pool"
   }
    }
}
```

See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/get

**Signature:**

```python
def get_nodepool(node_pool_id: str = None,
                 parent: str = None,
                 configuration: Dict[str, Dict[str, str]] = None,
                 secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **node_pool_id**      | string | null | No |
| **parent**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-nodepool",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.probes",
        "func": "get_nodepool"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-nodepool
    provider:
      func: get_nodepool
      module: chaosgcp.gke.nodepool.probes
      type: python
    type: probe
    

    ```



***

#### `list_nodepools`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.gke.nodepool.probes |
| **Name**              | list_nodepools |
| **Return**              | mapping |


List nodepools of a cluster.

The `parent` is following the form `projects/*/locations/*/clusters/*`
and will override any settings in the configuration block. If not provided
this action uses the configuration settings.

See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/list

**Signature:**

```python
def list_nodepools(
        parent: str = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **parent**      | string | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "list-nodepools",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.probes",
        "func": "list_nodepools"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-nodepools
    provider:
      func: list_nodepools
      module: chaosgcp.gke.nodepool.probes
      type: python
    type: probe
    

    ```



***

#### `rollback_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.gke.nodepool.actions |
| **Name**              | rollback_nodepool |
| **Return**              | mapping |


Rollback a previously Aborted or Failed NodePool upgrade.

If `wait_until_complete` is set to `True` (the default), the function
will block until the node pool is ready. Otherwise, will return immediatly
with the operation information.

See: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters.nodePools/create

**Signature:**

```python
def rollback_nodepool(
        node_pool_id: str,
        parent: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **node_pool_id**      | string |  | Yes |
| **parent**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "rollback-nodepool",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "rollback_nodepool",
        "arguments": {
          "node_pool_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: rollback-nodepool
    provider:
      arguments:
        node_pool_id: ''
      func: rollback_nodepool
      module: chaosgcp.gke.nodepool.actions
      type: python
    type: action
    

    ```



***

#### `swap_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.gke.nodepool.actions |
| **Name**              | swap_nodepool |
| **Return**              | mapping |


Create a new nodepool, drain the old one so pods can be rescheduled on the
new pool. Delete the old nodepool only `delete_old_node_pool` is set to
`True`, which is not the default. Otherwise, leave the old node pool
cordonned so it cannot be scheduled any longer.

Please ensure to provide the Kubernetes secrets as well when calling this
action.
See https://github.com/chaostoolkit/chaostoolkit-kubernetes#configuration

**Signature:**

```python
def swap_nodepool(old_node_pool_id: str,
                  new_nodepool_body: Dict[str, Any],
                  parent: str = None,
                  wait_until_complete: bool = True,
                  delete_old_node_pool: bool = False,
                  drain_timeout: int = 120,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **old_node_pool_id**      | string |  | Yes |
| **new_nodepool_body**      | mapping |  | Yes |
| **parent**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |
| **delete_old_node_pool**      | boolean | false | No |
| **drain_timeout**      | integer | 120 | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "swap-nodepool",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "swap_nodepool",
        "arguments": {
          "old_node_pool_id": "",
          "new_nodepool_body": {}
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: swap-nodepool
    provider:
      arguments:
        new_nodepool_body: {}
        old_node_pool_id: ''
      func: swap_nodepool
      module: chaosgcp.gke.nodepool.actions
      type: python
    type: action
    

    ```




### monitoring



***

#### `get_metrics`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.monitoring.probes |
| **Name**              | get_metrics |
| **Return**              | list |


Query for Cloud Monitoring metrics and returns a list of time series
objects for the metric and period.

Refer to the documentation
https://cloud.google.com/python/docs/reference/monitoring/latest/query
to learn about the various flags.

**Signature:**

```python
def get_metrics(
        metric_type: str,
        metric_labels_filters: Optional[Dict[str, str]] = None,
        resource_labels_filters: Optional[Dict[str, str]] = None,
        end_time: str = 'now',
        window: str = '5 minutes',
        aligner: int = 0,
        aligner_minutes: int = 1,
        reducer: int = 0,
        reducer_group_by: Optional[List[str]] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **metric_type**      | string |  | Yes |
| **metric_labels_filters**      | object | null | No |
| **resource_labels_filters**      | object | null | No |
| **end_time**      | string | "now" | No |
| **window**      | string | "5 minutes" | No |
| **aligner**      | integer | 0 | No |
| **aligner_minutes**      | integer | 1 | No |
| **reducer**      | integer | 0 | No |
| **reducer_group_by**      | object | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "get-metrics",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.monitoring.probes",
        "func": "get_metrics",
        "arguments": {
          "metric_type": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: get-metrics
    provider:
      arguments:
        metric_type: ''
      func: get_metrics
      module: chaosgcp.monitoring.probes
      type: python
    type: probe
    

    ```




### sql



***

#### `describe_instance`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.sql.probes |
| **Name**              | describe_instance |
| **Return**              | mapping |


Displays configuration and metadata about a Cloud SQL instance.

Information such as instance name, IP address, region, the CA certificate
and configuration settings will be displayed.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/get

:param instance_id: Cloud SQL instance ID.

**Signature:**

```python
def describe_instance(
        instance_id: str,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "describe-instance",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.probes",
        "func": "describe_instance",
        "arguments": {
          "instance_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: describe-instance
    provider:
      arguments:
        instance_id: ''
      func: describe_instance
      module: chaosgcp.sql.probes
      type: python
    type: probe
    

    ```



***

#### `disable_replication`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | disable_replication |
| **Return**              | mapping |


Disable replication on a read replica.

See also: https://cloud.google.com/sql/docs/postgres/replication/manage-replicas#disable_replication

**Signature:**

```python
def disable_replication(
        replica_name: str,
        project_id: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **replica_name**      | string |  | Yes |
| **project_id**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "disable-replication",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "disable_replication",
        "arguments": {
          "replica_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: disable-replication
    provider:
      arguments:
        replica_name: ''
      func: disable_replication
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```



***

#### `enable_replication`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | enable_replication |
| **Return**              | mapping |


Enable replication on a read replica.

See also: https://cloud.google.com/sql/docs/postgres/replication/manage-replicas#enable_replication

**Signature:**

```python
def enable_replication(
        replica_name: str,
        project_id: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **replica_name**      | string |  | Yes |
| **project_id**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "enable-replication",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "enable_replication",
        "arguments": {
          "replica_name": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: enable-replication
    provider:
      arguments:
        replica_name: ''
      func: enable_replication
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```



***

#### `export_data`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | export_data |
| **Return**              | mapping |


Exports data from a Cloud SQL instance to a Cloud Storage bucket
as a SQL dump or CSV file.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/export

If `project_id` is given, it will take precedence over the global
project ID defined at the configuration level.

**Signature:**

```python
def export_data(instance_id: str,
                storage_uri: str,
                project_id: str = None,
                file_type: str = 'sql',
                databases: List[str] = None,
                tables: List[str] = None,
                export_schema_only: bool = False,
                wait_until_complete: bool = True,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |
| **storage_uri**      | string |  | Yes |
| **project_id**      | string | null | No |
| **file_type**      | string | "sql" | No |
| **databases**      | list | null | No |
| **tables**      | list | null | No |
| **export_schema_only**      | boolean | false | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "export-data",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "export_data",
        "arguments": {
          "instance_id": "",
          "storage_uri": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: export-data
    provider:
      arguments:
        instance_id: ''
        storage_uri: ''
      func: export_data
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```



***

#### `import_data`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | import_data |
| **Return**              | mapping |


Imports data into a Cloud SQL instance from a SQL dump or CSV file
in Cloud Storage.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/import

If `project_id` is given, it will take precedence over the global
project ID defined at the configuration level.

**Signature:**

```python
def import_data(instance_id: str,
                storage_uri: str,
                database: str,
                project_id: str = None,
                file_type: str = 'sql',
                import_user: str = None,
                table: str = None,
                columns: List[str] = None,
                wait_until_complete: bool = True,
                configuration: Dict[str, Dict[str, str]] = None,
                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |
| **storage_uri**      | string |  | Yes |
| **database**      | string |  | Yes |
| **project_id**      | string | null | No |
| **file_type**      | string | "sql" | No |
| **import_user**      | string | null | No |
| **table**      | string | null | No |
| **columns**      | list | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "import-data",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "import_data",
        "arguments": {
          "instance_id": "",
          "storage_uri": "",
          "database": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: import-data
    provider:
      arguments:
        database: ''
        instance_id: ''
        storage_uri: ''
      func: import_data
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```



***

#### `list_instances`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.sql.probes |
| **Name**              | list_instances |
| **Return**              | mapping |


Lists Cloud SQL instances in a given project in the alphabetical order of
the instance name.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/list

**Signature:**

```python
def list_instances(
        configuration: Dict[str, Dict[str, str]] = None,
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
      "name": "list-instances",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.probes",
        "func": "list_instances"
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: list-instances
    provider:
      func: list_instances
      module: chaosgcp.sql.probes
      type: python
    type: probe
    

    ```



***

#### `restore_backup`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | restore_backup |
| **Return**              | mapping |


Performs a restore of a given backup. If `target_instance_id` is not set
then source and target are the same. If `backup_run_id` is not set, then
it picks the most recent backup automatically.

You may wait for the operation to complete, but bear in mind this can
take several minutes.

**Signature:**

```python
def restore_backup(
        source_instance_id: str,
        target_instance_id: Optional[str] = None,
        backup_run_id: Optional[str] = None,
        project_id: str = None,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **source_instance_id**      | string |  | Yes |
| **target_instance_id**      | object | null | No |
| **backup_run_id**      | object | null | No |
| **project_id**      | string | null | No |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "restore-backup",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "restore_backup",
        "arguments": {
          "source_instance_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: restore-backup
    provider:
      arguments:
        source_instance_id: ''
      func: restore_backup
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```



***

#### `trigger_failover`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | trigger_failover |
| **Return**              | mapping |


Causes a high-availability Cloud SQL instance to failover.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1/instances/failover

:param instance_id: Cloud SQL instance ID.
:param wait_until_complete: wait for the operation in progress to complete.
:param settings_version: The current settings version of this instance.

:return:

**Signature:**

```python
def trigger_failover(
        instance_id: str,
        wait_until_complete: bool = True,
        settings_version: Optional[int] = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |
| **wait_until_complete**      | boolean | true | No |
| **settings_version**      | object | null | No |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "trigger-failover",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.sql.actions",
        "func": "trigger_failover",
        "arguments": {
          "instance_id": ""
        }
      }
    }
    
    ```
=== "YAML"
    ```yaml

    name: trigger-failover
    provider:
      arguments:
        instance_id: ''
      func: trigger_failover
      module: chaosgcp.sql.actions
      type: python
    type: action
    

    ```




### storage



***

#### `object_exists`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgcp.storage.probes |
| **Name**              | object_exists |
| **Return**              | boolean |


Indicates whether a file in Cloud Storage bucket exists.

:param bucket_name: name of the bucket
:param object_name: name of the object within the bucket as path
:param configuration:
:param secrets:

**Signature:**

```python
def object_exists(bucket_name: str,
                  object_name: str,
                  configuration: Dict[str, Dict[str, str]] = None,
                  secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |
| **object_name**      | string |  | Yes |




**Usage:**

=== "JSON"
    ```json

    {
      "name": "object-exists",
      "type": "probe",
      "provider": {
        "type": "python",
        "module": "chaosgcp.storage.probes",
        "func": "object_exists",
        "arguments": {
          "bucket_name": "",
          "object_name": ""
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
        object_name: ''
      func: object_exists
      module: chaosgcp.storage.probes
      type: python
    type: probe
    

    ```



