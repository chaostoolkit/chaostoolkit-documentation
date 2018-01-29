# Extension Projects

In addition to the core projects, the Chaos Toolkit manages some extension
projects which provide probes and/or actions for experiments.

## chaostoolkit-kubernetes

The [chaostoolkit-kubernetes][chaoskube] project implements probes and actions
for experiments targetting a [Kubernetes][kubernetes] cluster. Those activities
are implemented as Python functions.

[chaoskube]: https://github.com/chaostoolkit/chaostoolkit-kubernetes
[kubernetes]: https://kubernetes.io/

This project is implemented in Python 3.

## chaostoolkit-gremlin

The [chaostoolkit-gremlin][chaosgremlin] project implements actions
for experiments exploring resource failures (CPU, Memory, Network...) in their
system through the [Gremlin, Inc.][gremlin] services. Those activities
are implemented as Python functions talking to the [Gremlin API][gremlinapi].

[chaosgremlin]: https://github.com/chaostoolkit/chaostoolkit-gremlin
[gremlin]: https://gremlininc.com/
[gremlinapi]: https://help.gremlininc.com/api/

This project is implemented in Python 3.

## chaostoolkit-prometheus

The [chaostoolkit-prometheus][chaosprom] project implements probes to fetch
information from your system through [Prometheus][prometheus]. Those probes
are implemented as Python functions talking to the [Prometheus API][promapi].

[chaosprom]: https://github.com/chaostoolkit/chaostoolkit-prometheus
[prometheus]: https://prometheus.io/
[promapi]: https://prometheus.io/docs/querying/api/

This project is implemented in Python 3.