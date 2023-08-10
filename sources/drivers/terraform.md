# Extension `chaosterraform`

|                       |               |
| --------------------- | ------------- |
| **Version**           | 0.0.9 |
| **Repository**        | https://github.com/mcastellin/chaostoolkit-terraform |



A [Chaos Toolkit](https://chaostoolkit.org/) driver to extend chaos experiments with [Terraform](https://www.terraform.io/)

## Package Installation

### From Python package index

To install the latest `chaostoolkit-terraform` stable release:

```shell
pip install -U chaostoolkit-terraform
```

### Edge version from the GitHub repository

To install the *edge* version of the `chaostoolkit-terraform` package directly from the repository source code:

```shell
pip install -U "git+https://github.com/mcastellin/chaostoolkit-terraform.git#egg=chaostoolkit-terraform"
```

## Usage

**chaostoolkit-terraform** provides a control to deploy Terraform modules. The control will automatically create the resources defined in the Terraform stack before experiment execution and destroy them once the experiment is completed.

To activate the `chaosterraform.control` for your experiments you need to define it in your experiment files (or settings):

```yaml
title: My experiment
description: ...

controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control

steady-state-hypothesis: {...}

method: []
```

By default the `chaosterraform.control` will reference the Terraform module found in the current working directory.

The control will execute Terraform command in the following phases of the experiment execution:

| Phase                 | Actions |
| --------------------- | ------- |
| **Configure control** | Initialize the Terraform driver in Chaos Toolkit|
| **Before experiment** | Initialize and apply the selected Terraform module |
| **After experiment**  | Run terraform destroy unless specifically asked to retain the created resources |

## Configuration

You can configure the Terraform control either via *control arguments* or using Chaos Toolkit parameters with the `tf_conf__` prefix:

**Configuration with control arguments**
```yaml
controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control
      arguments:
        silent: false
        retain: true
```

**Configuration using Chaos Toolkit parameters**
```yaml
configuration:
# parameters prefixed with `tf_conf__` will configure chaosterraform driver
  tf_conf__silent: false
  tf_conf__retain: true

controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control
```

> When both options are provided **configuration parameters supplied via the experiment configuration will
> be used**.


| Parameter Name        | Usage |
| --------------------- | ------- |
| **silent** | Suppress Terraform console output to avoid verbose experiment logs, defaults to `true`|
| **retain** | Do not run `terraform destroy` at the end of the experiment to retain resources, defaults to `false` |
| **chdir** | Instruct Terraform to change its working directory |

## Provide Input Variables for Terraform

You can override input variables defined in the Terraform module from within the experiment using the `variables` argument for the control:

```yaml
controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control
      arguments:
        variables:
          vpc_id: "vpc-0000000000"
          number_of_azs: 2
```

Alternatively, you can provide input variables from Chaos Toolkit configuration by referencing a parameter name already defined in Chaos Toolkit configuration:

```yaml
configuration:
  env_name: "live"
  ...

controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control
      arguments:
        variables:
          environment:
            name: "env_name"
```

## Use Terraform Outputs In Chaos Experiments

If your Terraform module exports some output variables you can use them in the Chaos Toolkit experiments
as regular experiment parameters. Such variables are added to the configuration context with the `tf_out__` prefix.

For example, this Terraform module exports a load balancer DNS name:

```terraform
terraform {
    ...
}

output "alb_dns_name" {
    value = aws_lb.application_lb.dns_name
}
```

We can use the exported DNS name in our chaos experiment like so:

```yaml
controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control

steady-state-hypothesis:
  title: "Application is available"
  probes:
    - type: probe
      name: "should-respond-200"
      tolerance: 200
      provider:
        type: http
        url: "http://${tf_out__alb_dns_name}"
        method: "GET"
        timeout: 3
```

In addition, we can ask the `chaosterraform.control` to map Terraform output values to new Chaos Toolkit configuration variables or override existing ones using the `outputs` argument:

```yaml
controls:
  - name: "Deploy Terraform module"
    provider:
      type: python
      module: chaosterraform.control
      arguments:
        outputs:
            alb_dns_name: "application_dns_name"
```

In the example above, the control will map the output value `alb_dns_name` into a new Chaos Toolkit configuration `application_dns_name` that can be referenced in the experiment template using the `${application_dns_name}` notation.





