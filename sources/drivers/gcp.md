# Extension `chaosgcp`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform |



[![Build Status](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform.svg?branch=master)](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-google-cloud-platform.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Google Cloud Platform][gcp] platform.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[gce]: https://cloud.google.com/compute/
[gcp]: https://cloud.google.com


## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
pip install -U chaostoolkit-google-cloud-platform
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "swap-nodepool-for-a-new-one",
    "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "swap_nodepool",
        "secrets": ["gcp"],
        "arguments": {
            "body": {
                "nodePool": {
                    "config": { 
                        "oauthScopes": [
                            "gke-version-default",
                            "https://www.googleapis.com/auth/devstorage.read_only",
                            "https://www.googleapis.com/auth/logging.write",
                            "https://www.googleapis.com/auth/monitoring",
                            "https://www.googleapis.com/auth/service.management.readonly",
                            "https://www.googleapis.com/auth/servicecontrol",
                            "https://www.googleapis.com/auth/trace.append"
                        ]
                    },
                    "initialNodeCount": 3,
                    "name": "new-default-pool"
                }
            }
        }
    }
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

Note that most functions exposed in this package also take those values
directly when you want specific values for them.

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

While the embedded way looks like this:


```json
{
    "secrets": {
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


### Putting it all together

Here is a full example:

```json
{
    "version": "1.0.0",
    "title": "...",
    "description": "...",
    "configuration": {
        "gcp_project_id": "...",
        "gcp_gke_cluster_name": "...",
        "gcp_region": "...",
        "gcp_zone": "..."
    },
    "secrets": {
        "gcp": {
            "service_account_file": "/path/to/sa.json"
        }
    },
    "method": [
        {
            "type": "action",
            "name": "swap-nodepool-for-a-new-one",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "swap_nodepool",
                "secrets": ["gcp"],
                "arguments": {
                    "body": {
                        "nodePool": {
                            "config": { 
                                "oauthScopes": [
                                    "gke-version-default",
                                    "https://www.googleapis.com/auth/devstorage.read_only",
                                    "https://www.googleapis.com/auth/logging.write",
                                    "https://www.googleapis.com/auth/monitoring",
                                    "https://www.googleapis.com/auth/service.management.readonly",
                                    "https://www.googleapis.com/auth/servicecontrol",
                                    "https://www.googleapis.com/auth/trace.append"
                                ]
                            },
                            "initialNodeCount": 3,
                            "name": "new-default-pool"
                        }
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
    - "gce_project_id" -> "gcp_project_id"
    - "gce_region" -> "gcp_region"
    - "gce_zone" -> "gcp_zone"
    - "gce_cluster_name" -> "gcp_gke_cluster_name"

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





## Exported Activities



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
('def create_new_nodepool(\n        body: Dict[str, Any],\n        wait_until_complete: bool = True,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **body**      | mapping |  | Yes |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

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
('def delete_nodepool(\n        node_pool_id: str,\n        wait_until_complete: bool = True,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **node_pool_id**      | string |  | Yes |
| **wait_until_complete**      | boolean | true | No |




**Usage:**

```json
{
  "name": "delete-nodepool",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosgcp.gke.nodepool.actions",
    "func": "delete_nodepool",
    "arguments": {
      "node_pool_id": ""
    }
  }
}
```

```yaml
name: delete-nodepool
provider:
  arguments:
    node_pool_id: ''
  func: delete_nodepool
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

**Signature:**

```python
('def swap_nodepool(old_node_pool_id: str,\n                  new_nodepool_body: Dict[str, Any],\n                  wait_until_complete: bool = True,\n                  delete_old_node_pool: bool = False,\n                  drain_timeout: int = 120,\n                  configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **old_node_pool_id**      | string |  | Yes |
| **new_nodepool_body**      | mapping |  | Yes |
| **wait_until_complete**      | boolean | true | No |
| **delete_old_node_pool**      | boolean | false | No |
| **drain_timeout**      | integer | 120 | No |




**Usage:**

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

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/get

:param instance_id: Cloud SQL instance ID.

**Signature:**

```python
('def describe_instance(\n        instance_id: str,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |




**Usage:**

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

#### `export_data`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgcp.sql.actions |
| **Name**              | export_data |
| **Return**              | mapping |


Exports data from a Cloud SQL instance to a Cloud Storage bucket
as a SQL dump or CSV file.

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/export

If `project_id` is given, it will take precedence over the global
project ID defined at the configuration level.

**Signature:**

```python
("def export_data(instance_id: str,\n                storage_uri: str,\n                project_id: str = None,\n                file_type: str = 'sql',\n                databases: List[str] = None,\n                tables: List[str] = None,\n                export_schema_only: bool = False,\n                wait_until_complete: bool = True,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
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

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/import

If `project_id` is given, it will take precedence over the global
project ID defined at the configuration level.

**Signature:**

```python
("def import_data(instance_id: str,\n                storage_uri: str,\n                database: str,\n                project_id: str = None,\n                file_type: str = 'sql',\n                import_user: str = None,\n                table: str = None,\n                columns: List[str] = None,\n                wait_until_complete: bool = True,\n                configuration: Dict[str, Dict[str, str]] = None,\n                secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n",)
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

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/list

**Signature:**

```python
('def list_instances(\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |




**Usage:**

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

```yaml
name: list-instances
provider:
  func: list_instances
  module: chaosgcp.sql.probes
  type: python
type: probe

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

See: https://cloud.google.com/sql/docs/postgres/admin-api/v1beta4/instances/failover

:param instance_id: Cloud SQL instance ID.
:param wait_until_complete: wait for the operation in progress to complete.
:param settings_version: The current settings version of this instance.

:return:

**Signature:**

```python
('def trigger_failover(\n        instance_id: str,\n        wait_until_complete: bool = True,\n        settings_version: int = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **instance_id**      | string |  | Yes |
| **wait_until_complete**      | boolean | true | No |
| **settings_version**      | integer | null | No |




**Usage:**

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
('def object_exists(bucket_name: str,\n                  object_name: str,\n                  configuration: Dict[str, Dict[str, str]] = None,\n                  secrets: Dict[str, Dict[str, str]] = None) -> bool:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **bucket_name**      | string |  | Yes |
| **object_name**      | string |  | Yes |




**Usage:**

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



