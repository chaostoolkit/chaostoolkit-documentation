# Extension `chaosgandi`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.1.1 |
| **Repository**        | https://github.com/chaostoolkit-incubator/chaostoolkit-gandi |


 
[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-gandi.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-gandi)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-gandi.svg)](https://www.python.org/)


This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
pip install -U chaostoolkit-gandi
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "title": "Our domains are not going expiring within a month",
    "description": "We need time to renew.",
    "secrets": {
        "gandi": {
            "apikey": {
                "type": "env",
                "key": "GANDI_API_KEY"
            }
        }
    },
    "steady-state-hypothesis": {
        "title": "Check domains are all more than 1 month away from expiring",
        "probes": [
            {
                "type": "probe",
                "name": "list-my-domains",
                "tolerance": {
                    "type": "probe",
                    "name": "validate-domain-expire-date",
                    "provider": {
                        "type": "python",
                        "secrets": ["gandi"],
                        "module": "chaosgandi.domains.tolerances",
                        "func": "domains_should_not_expire_in",
                        "arguments": {
                            "when": "1 month"
                        }
                    }
                },
                "provider": {
                    "type": "python",
                    "secrets": ["gandi"],
                    "module": "chaosgandi.domains.probes",
                    "func": "list_domains"
                }
            }
        ]
    },
    "method": []
}

```

That's it!

Set the `GANDI_API_KEY` environment variable to your Gandi API Key.

Please explore the code to see existing probes and actions.

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
pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
pytest
```





## Exported Activities



### domains



***

#### `domains_should_not_expire_in`

|                       |               |
| --------------------- | ------------- |
| **Type**              | tolerance |
| **Module**            | chaosgandi.domains.tolerances |
| **Name**              | domains_should_not_expire_in |
| **Return**              | None |


Go through the list of Gandi domains and fails if any expires before
the given date treshold as a relative time to now.

**Signature:**

```python
("def domains_should_not_expire_in(value: List[Dict[str, Any]] = None,\n                                 when: str = '1 month'):\n    pass\n",)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **value**      | list | null | No |
| **when**      | string | "1 month" | No |



!!! info ""
    Tolerances declare the `value` argument which is automatically injected by
    Chaos Toolkit as the output of the probe they are evaluating.


**Usage:**

```json
{
  "steady-state-hypothesis": {
    "title": "...",
    "probes": [
      {
        "type": "probe",
        "tolerance": {
          "name": "domains-should-not-expire-in",
          "type": "tolerance",
          "provider": {
            "type": "python",
            "module": "chaosgandi.domains.tolerances",
            "func": "domains_should_not_expire_in"
          }
        },
        "...": "..."
      }
    ]
  }
}
```

```yaml
steady-state-hypothesis:
  probes:
  - '...': '...'
    tolerance:
      name: domains-should-not-expire-in
      provider:
        func: domains_should_not_expire_in
        module: chaosgandi.domains.tolerances
        type: python
      type: tolerance
    type: probe
  title: '...'

```



***

#### `list_domains`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgandi.domains.probes |
| **Name**              | list_domains |
| **Return**              | list |


List all domains or those matching the given TLD or FQDN filters and
return the list as-is.

See https://api.gandi.net/docs/domains/#v5-domain-domains

**Signature:**

```python
('def list_domains(\n        fqdn_filter: str = None,\n        tld_filter: str = None,\n        configuration: Dict[str, Dict[str, str]] = None,\n        secrets: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **fqdn_filter**      | string | null | No |
| **tld_filter**      | string | null | No |




**Usage:**

```json
{
  "name": "list-domains",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosgandi.domains.probes",
    "func": "list_domains"
  }
}
```

```yaml
name: list-domains
provider:
  func: list_domains
  module: chaosgandi.domains.probes
  type: python
type: probe

```



***

#### `list_nameservers`

|                       |               |
| --------------------- | ------------- |
| **Type**              | probe |
| **Module**            | chaosgandi.domains.probes |
| **Name**              | list_nameservers |
| **Return**              | list |


List nameservers set for this domain and return them as a list of strings.

See https://api.gandi.net/docs/domains/#v5-domain-domains-domain-nameservers

**Signature:**

```python
('def list_nameservers(domain: str,\n                     configuration: Dict[str, Dict[str, str]] = None,\n                     secrets: Dict[str, Dict[str, str]] = None) -> List[str]:\n    pass\n',)
```

**Arguments:**

| Name | Type | Default | Required |
| --------------------- | ------------- | ------------- | ------------- |
| **domain**      | string |  | Yes |




**Usage:**

```json
{
  "name": "list-nameservers",
  "type": "probe",
  "provider": {
    "type": "python",
    "module": "chaosgandi.domains.probes",
    "func": "list_nameservers",
    "arguments": {
      "domain": ""
    }
  }
}
```

```yaml
name: list-nameservers
provider:
  arguments:
    domain: ''
  func: list_nameservers
  module: chaosgandi.domains.probes
  type: python
type: probe

```



