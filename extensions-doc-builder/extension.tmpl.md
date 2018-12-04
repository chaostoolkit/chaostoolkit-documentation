# Extension `{{ext.name}}`

|                       |               |
| --------------------- | ------------- |
| **Version**           | {{ext.version}} |
| **Repository**        | {{ext.repo_url}} |

{{readme}}

{%if controls.enabled %}
## Exported Controls
This package exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment**               | {{controls.experiment.before}} | {{controls.experiment.after}} |
| **Steady-state Hypothesis**  | {{controls.hypothesis.before}} | {{controls.hypothesis.after}} |
| **Method**                   | {{controls.method.before}} | {{controls.method.after}} |
| **Rollback**                 | {{controls.rollback.before}} | {{controls.rollback.after}} |
| **Activities**               | {{controls.activity.before}} | {{controls.activity.after}} |

To use this control module, please add the following section to your experiment:

```json
{{controls.as_json}}
```

```yaml
{{controls.as_yaml}}
```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.
{% endif %}

{%if activities %}
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
{% endif %}