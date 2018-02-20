# Extension Projects

In addition to the core projects, the Chaos Toolkit manages some extension
projects which provide probes and/or actions for experiments.

### Official Extensions

#### chaostoolkit-kubernetes

The [chaostoolkit-kubernetes][chaoskube] project implements probes and actions
for experiments targetting a [Kubernetes][kubernetes] cluster. Those activities
are implemented as Python functions.

[chaoskube]: https://github.com/chaostoolkit/chaostoolkit-kubernetes
[kubernetes]: https://kubernetes.io/

This project is implemented in Python 3.

### Incubating Extensions

These extensions are under work and not mature yet to be part of the core
of the Chaos Toolkit.

#### chaostoolkit-gremlin

The [chaostoolkit-gremlin][chaosgremlin] project implements actions
for experiments exploring resource failures (CPU, Memory, Network...) in their
system through the [Gremlin, Inc.][gremlin] services. Those activities
are implemented as Python functions talking to the [Gremlin API][gremlinapi].

[chaosgremlin]: https://github.com/chaostoolkit/chaostoolkit-gremlin
[gremlin]: https://gremlininc.com/
[gremlinapi]: https://help.gremlininc.com/api/

This project is implemented in Python 3.

#### chaostoolkit-prometheus

The [chaostoolkit-prometheus][chaosprom] project implements probes to fetch
information from your system through [Prometheus][prometheus]. Those probes
are implemented as Python functions talking to the [Prometheus API][promapi].

[chaosprom]: https://github.com/chaostoolkit/chaostoolkit-prometheus
[prometheus]: https://prometheus.io/
[promapi]: https://prometheus.io/docs/querying/api/

This project is implemented in Python 3.

#### chaostoolkit-aws

The [chaostoolkit-aws][chaosaws] project implements actions and probes
for experiments exploring chaos engineering against your [AWS][aws] environment.
Those activities are implemented as Python functions talking to the
[AWS API][awsapi].

[chaosaws]: https://github.com/chaostoolkit-incubator/chaostoolkit-aws
[aws]: https://aws.amazon.com/
[awsapi]: https://aws.amazon.com/documentation/

This project is implemented in Python 3.

#### chaostoolkit-cloud-foundry

The [chaostoolkit-cloud-foundry][chaoscf] project implements actions and probes
for experiments exploring chaos engineering against your [Cloud Foundry][cf]
environment. Those activities are implemented as Python functions talking to the
[Cloud Foundry API][cfapi].

[chaoscf]: https://github.com/chaostoolkit-incubator/chaostoolkit-cloud-foundry
[cf]: https://www.cloudfoundry.org/
[cfapi]: https://apidocs.cloudfoundry.org/

This project is implemented in Python 3.

#### chaostoolkit-slack

The [chaostoolkit-slack][chaosslack] project implements the notification
interface to push Chaos Toolkit events to Slack channels.

[chaosslack]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack

This project is implemented in Python 3.
