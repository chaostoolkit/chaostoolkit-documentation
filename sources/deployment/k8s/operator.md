# Deploy Chaos Toolkit as a Kubernetes Operator

Kubernetes operators are a popular approach to create bespoke controllers of
any application on top of the Kubernetes API.

The Chaos Toolkit operator listens for experiment declarations and triggers
a new Kubernetes pod, running the Chaos Toolkit with the specified experiment.

## Deploy the operator

The [operator][op] can be found on the Chaos Toolkit incubator.

[op]: https://github.com/chaostoolkit-incubator/kubernetes-crd

It is deployed via typical Kubernetes [manifests][] which need to be applied
via [Kustomize][], the native configuration manager.

[manifests]: https://github.com/chaostoolkit-incubator/kubernetes-crd/tree/master/manifests
[Kustomize]: https://kustomize.io/

First, download the [Kustomize binary][kustrel]:

```
$ curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

[kustrel]: https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md

Next, simply run the following:

```console
$ ./kustomize build manifests/overlays/generic-rbac | kubectl apply -f -
```

This will build the manifests and apply them on your current default cluster.
Notice how we use the RBAC variant of the deployement. If you have other
requirements (no-RBAC, pod security or network policies), then check the
[operator's documentation][op] to deploy the appropriate variant.

By now, you should have the operator running in the `chaostoolkit-crd`.

```console
$ kubectl -n chaostoolkit-crd get po
NAME                                READY   STATUS    RESTARTS   AGE
chaostoolkit-crd-7ddb9b78d9-dgxx7   1/1     Running   0          35s
```

## Run an experiment

Now that your controller is listening, you can ask it to schedule a Chaos
Toolkit experiment by applying a resource with the following API:

```yaml
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
```

Below is a basic example, assuming a file named `experiment.yaml`:

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: chaostoolkit-run

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-env
  namespace: chaostoolkit-run
data:
  EXPERIMENT_URL: "https://example.com/experiment.json"

---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
```

We first create the namespace in which the Chaos Toolkit will run. This is
not mandatory as the `chaostoolkit-run` will be created if you don't
specify anything.

Then, we need a config-map to provide the necessary environment used by the
Chaos Toolkit to run. You must specify at least the `EXPERIMENT_URL` which
points to the experiment location. Here we are using a URL but we will
see later how to load from local files too.

Finally, we simply create a `ChaosToolkitExperiment` object that the
controller picks up and understand as a new experiment to run in its own pod.

Notice how the specification of that object only declare which namespace
will be used to run the experiment from, here `chaostoolkit-run` that
we created.

Apply it as follows:

```console
$ kubectl apply -f experiment.yaml
```

Look at the Chaos Toolkit running:

```console
$ kubectl -n chaostoolkit-run get po
```

The status of the experiment's run, if it deviated, defines the status
if the pod. So, when the experiment does deviate, the pod should have a
status set to `Error`.

### Delete the experiment run's resources

To delete the run's resources, simply delete the object as follows:

```
$ kubectl delete -f experiment.yaml
```

## Configure the experiment

Chaos Toolkit experiments often expect data to be passed as environment
variables of the `chaos`'s command shell.

The operator allows you to specify those values through the the config-map
as we saw above:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-env
  namespace: chaostoolkit-run
data:
  EXPERIMENT_URL: "https://example.com/experiment.json"
  NAME: "Jane Doe"
```

They will be injected into the Chaos Toolkit's pod as environment variables.


## Configure the `chaos run` command

Chaos Toolkit reads its settings from a file and you can pass yours
by creating a Kubernetes secret named, by default, `chaostoolkit-settings`.

For instance, assuming you have a [Chaos Toolkit settings file][settings],
you can create a secret from it as follows:

[settings]: ../../reference/usage/settings.md

```console
$ kubectl -n chaostoolkit-run \
    create secrets chaostoolkit-settings \
    --from-file=settings.yaml
```

Reading settings is disabled by default, so you need to let the operator
know it should allow it for that run:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
  pod:
    settings:
      enabled: true
```

## Run the experiment with specific extensions

The default container image used by the operator is the official 
[Chaos Toollkit image][dockerfile] which embeds no
[Chaos Toolkit extensions][ext].

[dockerfile]: https://raw.githubusercontent.com/chaostoolkit/chaostoolkit/master/Dockerfile
[ext]: ../../drivers/overview.md

This means that you will likely need to create your bespoke container image.
For instance, to install the Chaos Toolkit Kubernetes extension, create
a Dockerfile like this:

```dockerfile
FROM chaostoolkit:chaostoolkit

RUN apk update && \
    apk add --virtual build-deps libffi-dev openssl-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir chaostoolkit-kubernetes && \
    apk del build-deps && \
    rm -rf /tmp/* /root/.cache
```

Then create the image with docker:

```
$ docker build --tag my/chaostoolkit -f ./Dockerfile
```

or used something like [Podman][]:

[podman]: https://podman.io/

```
$ podman build --tag my/chaostoolkit -f ./Dockerfile
```

Once this image is pushed to any registry you can access, you need to
let the operator knwo it must use it.

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
  pod:
    image:
      name: my/chaostoolkit
```
