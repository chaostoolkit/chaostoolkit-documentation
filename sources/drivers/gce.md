# Extension `chaosgce`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.2.2 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud |

N/A

## Exported Activities



### nodepool



***

#### `create_new_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgce.nodepool.actions |
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
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

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
    "module": "chaosgce.nodepool.actions",
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
  module: chaosgce.nodepool.actions
  type: python
type: action

```



***

#### `delete_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgce.nodepool.actions |
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
        node_pool_id: str,
        wait_until_complete: bool = True,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

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
    "module": "chaosgce.nodepool.actions",
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
  module: chaosgce.nodepool.actions
  type: python
type: action

```



***

#### `swap_nodepool`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosgce.nodepool.actions |
| **Name**              | swap_nodepool |
| **Return**              | mapping |


Create a new nodepool, drain the old one so pods can be rescheduled on the
new pool. Delete the old nodepool only `delete_old_node_pool` is set to
`True`, which is not the default. Otherwise, leave the old node pool
cordonned so it cannot be scheduled any longer.

**Signature:**

```python
def swap_nodepool(old_node_pool_id: str,
                  new_nodepool_body: Dict[str, Any],
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
    "module": "chaosgce.nodepool.actions",
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
  module: chaosgce.nodepool.actions
  type: python
type: action

```


