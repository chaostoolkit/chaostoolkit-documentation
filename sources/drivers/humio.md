# Extension `chaoshumio`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.0 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-humio |

N/A

## Exported Activities



### notification



***

#### `notify`

|                       |               |
| --------------------- | ------------- |
| **Type**              |  |
| **Module**            | chaoshumio.notification |
| **Name**              | notify |
| **Return**              | None |


Send a log message to the Humio ingest endpoint.

The settings must contain:

- `"token"`: a slack API token
- `"url"`: the channel where to send this event notification

If one of these two attributes is missing, no notification is sent.

**Signature:**

```python
def notify(settings: Dict[str, Any], event: Dict[str, Any]):
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **settings**      | mapping |  | Yes |
| **event**      | mapping |  | Yes |


**Usage:**

```json
{
  "name": "notify",
  "type": "",
  "provider": {
    "type": "python",
    "module": "chaoshumio.notification",
    "func": "notify",
    "arguments": {
      "settings": {},
      "event": {}
    }
  }
}
```

```yaml
name: notify
provider:
  arguments:
    event: {}
    settings: {}
  func: notify
  module: chaoshumio.notification
  type: python
type: ''

```


