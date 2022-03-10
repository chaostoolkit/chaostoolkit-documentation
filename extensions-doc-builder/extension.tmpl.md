# Extension `{{ext.name}}`

|                       |               |
| --------------------- | ------------- |
| **Version**           | {{ext.version}} |
| **Repository**        | {{ext.repo_url}} |


{{readme}}

{%if controls %}
## Exported Controls
{% endif %}
{% for control_name, control in controls.items() %}
{%if control.enabled %}
### {{control_name}}


{%if control.doc %}
{{ control.doc }}
{% endif %}

This module exports [controls][] covering the following phases of the execution
of an experiment:

[controls]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

|            Level             |             Before             |             After             |
| -----------------------------| ------------------------------ |------------------------------ |
| **Experiment Loading**       | {{control.loading_experiment.before}} | {{control.loading_experiment.after}} |
| **Experiment**               | {{control.experiment.before}} | {{control.experiment.after}} |
| **Steady-state Hypothesis**  | {{control.hypothesis.before}} | {{control.hypothesis.after}} |
| **Method**                   | {{control.method.before}} | {{control.method.after}} |
| **Rollback**                 | {{control.rollback.before}} | {{control.rollback.after}} |
| **Activities**               | {{control.activity.before}} | {{control.activity.after}} |

In addition, the controls may define the followings:

|            Level             |             Enabled             |
| -----------------------------| ------------------------------ |
| **Validate Control**       | {{control.validate}} |
| **Configure Control**       | {{control.configure}} |
| **Cleanup Control**       | {{control.cleanup}} |

To use this control module, please add the following section to your experiment:

=== "JSON"
    ```json
    {{control.as_json}}
    ```
=== "YAML"
    ```yaml
    {{control.as_yaml}}
    ```

This block may also be enabled at any other level (steady-state hypothesis or
activity) to focus only on that level.

When enabled at the experiment level, by default, all sub-levels are also
applied unless you set the `automatic` properties to `false`.
{% endif %}
{% endfor %}

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

{% if activity.type == "tolerance" %}
!!! info ""
    Tolerances declare the `value` argument which is automatically injected by
    Chaos Toolkit as the output of the probe they are evaluating.
{% endif %}

**Usage:**

=== "JSON"
    ```json
    {{activity.as_json}}
    ```
=== "YAML"
    ```yaml
    {{activity.as_yaml}}
    ```

{% endfor %}
{% endfor %}
{% endif %}