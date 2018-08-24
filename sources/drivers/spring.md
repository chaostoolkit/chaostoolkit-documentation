# Extension `chaosspring`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-spring |

N/A

## Exported Activities



### actions



***

#### `change_assaults_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | change_assaults_configuration |
| **Return**              | string |


Change Assaults configuration on a specific service.

**Signature:**

```python
def change_assaults_configuration(
        base_url: str,
        assaults_configuration: Dict[str, Any],
        timeout: float = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> str:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **assaults_configuration**      | mapping |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "change-assaults-configuration",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "change_assaults_configuration",
    "arguments": {
      "base_url": "",
      "assaults_configuration": {}
    }
  }
}
```

```yaml
name: change-assaults-configuration
provider:
  arguments:
    assaults_configuration: {}
    base_url: ''
  func: change_assaults_configuration
  module: chaosspring.actions
  type: python
type: action

```



***

#### `disable_chaosmonkey`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | disable_chaosmonkey |
| **Return**              | string |


Disable Chaos Monkey on a specific service.

**Signature:**

```python
def disable_chaosmonkey(base_url: str,
                        timeout: float = None,
                        configuration: Dict[str, Dict[str, str]] = None,
                        secrets: Dict[str, Dict[str, str]] = None) -> str:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "disable-chaosmonkey",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "disable_chaosmonkey",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: disable-chaosmonkey
provider:
  arguments:
    base_url: ''
  func: disable_chaosmonkey
  module: chaosspring.actions
  type: python
type: action

```



***

#### `enable_chaosmonkey`

|                       |               |
| --------------------- | ------------- |
| **Type**              | action |
| **Module**            | chaosspring.actions |
| **Name**              | enable_chaosmonkey |
| **Return**              | string |


Enable Chaos Monkey on a specific service.

**Signature:**

```python
def enable_chaosmonkey(base_url: str,
                       timeout: float = None,
                       configuration: Dict[str, Dict[str, str]] = None,
                       secrets: Dict[str, Dict[str, str]] = None) -> str:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "enable-chaosmonkey",
  "type": "action",
  "provider": {
    "type": "python",
    "module": "chaosspring.actions",
    "func": "enable_chaosmonkey",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: enable-chaosmonkey
provider:
  arguments:
    base_url: ''
  func: enable_chaosmonkey
  module: chaosspring.actions
  type: python
type: action

```




### probes



***

#### `assaults_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | assaults_configuration |
| **Return**              | mapping |


Get the current assaults configuration from the specified service.

**Signature:**

```python
def assaults_configuration(
        base_url: str,
        timeout: float = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "assaults-configuration",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "assaults_configuration",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: assaults-configuration
provider:
  arguments:
    base_url: ''
  func: assaults_configuration
  module: chaosspring.probes
  type: python
type: probe

```



***

#### `chaosmonkey_enabled`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | chaosmonkey_enabled |
| **Return**              | boolean |


Enquire whether Chaos Monkey is enabled on the
specified service.

**Signature:**

```python
def chaosmonkey_enabled(base_url: str,
                        timeout: float = None,
                        configuration: Dict[str, Dict[str, str]] = None,
                        secrets: Dict[str, Dict[str, str]] = None) -> bool:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "chaosmonkey-enabled",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "chaosmonkey_enabled",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: chaosmonkey-enabled
provider:
  arguments:
    base_url: ''
  func: chaosmonkey_enabled
  module: chaosspring.probes
  type: python
type: probe

```



***

#### `watcher_configuration`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosspring.probes |
| **Name**              | watcher_configuration |
| **Return**              | mapping |


Get the current watcher configuration from the specified service.

**Signature:**

```python
def watcher_configuration(
        base_url: str,
        timeout: float = None,
        configuration: Dict[str, Dict[str, str]] = None,
        secrets: Dict[str, Dict[str, str]] = None) -> Dict[str, Any]:
    pass

```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **base_url**      | string |  | Yes |
| **timeout**      | number | null | No |


**Usage:**

```json
{
  "name": "watcher-configuration",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosspring.probes",
    "func": "watcher_configuration",
    "arguments": {
      "base_url": ""
    }
  }
}
```

```yaml
name: watcher-configuration
provider:
  arguments:
    base_url: ''
  func: watcher_configuration
  module: chaosspring.probes
  type: python
type: probe

```


