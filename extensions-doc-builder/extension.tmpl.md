# Extension `{{ext.name}}`

|                       |               |
| --------------------- | ------------- |
| **Version**           | {{ext.version}} |
| **Repository**        | {{ext.repo_url}} |

{{readme}}

## Exported Activities

{% for mod in activities %}

### {{mod}}

{% for activity in activities[mod] %}

***

#### `{{activity.name}}`

|                       |               |
| --------------------- | ------------- |
| **Type**              | {{activity.type}} |
| **Module**            | {{activity.module}} |
| **Name**              | {{activity.name}} |
| **Return**              | {{activity.return}} |


{{activity.doc}}

**Signature:**

```python
{{activity.signature}}
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
{% for arg in activity.arguments %}| **{{arg.name}}**      | {{arg.type}} | {{arg.default}} | {{arg.required}} |
{% endfor %}

**Usage:**

```json
{{activity.as_json}}
```

```yaml
{{activity.as_yaml}}
```

{% endfor %}
{% endfor %}