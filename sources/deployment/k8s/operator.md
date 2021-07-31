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

For macOS, you can also install it via the Homebrew package manager: 

```
$ brew install kustomize
```

Next, simply run the following:

```console
$ kustomize build manifests/overlays/generic-rbac | kubectl apply -f -
```

This will build the manifests and apply them on your current default cluster.
Notice how we use the RBAC variant of the deployment. If you have other
requirements (no-RBAC, pod security or network policies), then check the
[operator's documentation][op] to deploy the appropriate variant.

You can install another variant as follows:

```console
$ kustomize build manifests/overlays/generic[-rbac[-podsec[-netsec]]] | kubectl apply -f -
```

By now, you should have the operator running in the `chaostoolkit-crd`.

```console
$ kubectl -n chaostoolkit-crd get pods
NAME                                READY   STATUS    RESTARTS   AGE
chaostoolkit-crd-7ddb9b78d9-dgxx7   1/1     Running   0          35s
```

The operator deployment created two namespaces, by default:
- the `chaostoolkit-crd` namespace contains the operator pod and Chaos Toolkit
 experiment definitions 
- the `chaostoolkit-run` namespace contains pods running the Chaos Toolkit
 experiments

## Run an experiment
    
Now that your controller is listening, you can ask it to schedule a Chaos
Toolkit experiment by applying a resource with the following API:

```yaml
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
```

Below is a basic example, assuming a file named `basic.yaml`:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-experiment
  namespace: chaostoolkit-run
data:
  experiment.json: |
    {
      "version": "1.0.0",
      "title": "Hello world!",
      "description": "Say hello world.",
      "method": [
        {
          "type": "action",
          "name": "say-hello",
          "provider": {
            "type": "process",
            "path": "echo",
            "arguments": "hello"
          }
        }
      ]
    }
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd

```

First, we will use the default namespace in which the Chaos Toolkit will run.

Then, we need a config map to pass the experiment to execute.

Finally, we simply create a `ChaosToolkitExperiment` object that the
controller picks up and understand as a new experiment to run in its own pod.

Apply it as follows:

```console
$ kubectl apply -f basic.yaml
```

Then, you can check the Chaos Toolkit experiment has been registered, and will
be scheduled to run as soon as possible:

````console
$ kubectl -n chaostoolkit-crd get ctks
````

Look at the Chaos Toolkit running:

```console
$ kubectl -n chaostoolkit-run get pods
```

The status of the experiment's run, if it deviated, defines the status
if the pod. So, when the experiment does deviate, the pod should have a
status set to `Error`. Otherwise, the status will be `Completed`.

## Manage the Chaos Toolkit Experiments

### List and inspect experiments

You can list your experiments as follows:

```
$ kubectl -n chaostoolkit-crd get chaosexperiments 
```

You can describe one experiment as follows:

```
$ kubectl -n chaostoolkit-crd describe chaosexperiment my-chaos-exp 
```

You can also use the short names for the custom resource `ctks` and `ctk`.

### Delete the experiment run's resources

You can delete an experiment and its related resources as follows:

```
$ kubectl -n chaostoolkit-crd delete ctk my-chaos-exp 
```

However, the custom resources (ConfigMap, Secrets, etc.) won't be deleted. 
This command only deletes the resources that the operator creates for the 
experiment to be able to run.

To delete all the run's resources, simply delete the objects as follows:

```
$ kubectl delete -f basic.yaml
```

## Various configurations

You may decide to change various aspects of the final pod (such as passing
settings as secrets, changing the roles allowed to the pod, even override
the entire pod template).

### Make the operator more verbose

By default, the operator logs at INFO level. To enable the DEBUG level,
 you need to change the operator's deployment command:

In the file `manifests/base/common/deployment.yaml`:

Change:

```yaml
  - name: crd
    image: chaostoolkit/k8scrd:latest
    imagePullPolicy: Always
```

to:

```yaml
  - name: crd
    image: chaostoolkit/k8scrd:latest
    imagePullPolicy: Always
    command:
        - kopf
    args:
        - run
        - --verbose
        - --namespace
        - chaostoolkit-crd
        - controller.py
```

Then re-deploy using Kustomize.

### Configure the toolkit with environment variables

Chaos Toolkit experiments often expect data to be passed as environment
variables of the `chaos`'s command shell.

The operator allows you to specify those values through the config map:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-env
  namespace: chaostoolkit-run
data:
  NAME: "Jane Doe"
```

They will be injected into the Chaos Toolkit's pod as environment variables.

You might need several environment config maps for various experiments. You can
tell the operator where to find the config map to be loaded as environment
variables.

We'll assume you defined another config map named `my-chaos-env-vars`. You
can use it by setting the `configMapName` in the `env` block of the pod spec: 

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  pod:
    env:
      configMapName: my-chaos-env-vars
```

You can disable loading environment variables into the pod by using
the `enabled` property:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  pod:
    env:
      enabled: false
```

Plain text environment variables might not be secure enough in some use cases, 
such as database user name & passord, API keys, tokens, etc.
You can define multiple encrypted key-value pairs in a Kubernetes secret and
load them as environment variables. To to so, you shall indicate the name
of the secret with the `secretName` property.

Assuming you created a generic secret named `chaostoolkit-secrets`, you can
load the values as shown below:
```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  pod:
    env:
      secretName: chaostoolkit-secrets
```
 
All the key-value pairs from the secret will be injected into the 
Chaos Toolkit's pod as environment variables.

### Handle multiple experiment files

In the basic example, the name of the config map holding the experiment 
is the default value `chaostoolkit-experiment`. Usually, you'll want a more
unique name since you'll probably run multiple experiments from the
`chaostoolkit-run` namespace.

In that case, do it as follows:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-experiment-1234
  namespace: chaostoolkit-run
data:
  experiment.json: |
    {
        "title": "...",
    }
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  pod:
    experiment:
      configMapName: chaostoolkit-experiment-1234
```

You need to define the `configMapName` in the `experiment` block of 
the pod spec. 

### Use the experiment in YAML format

If your experiments are encoded using YAML, you can set it as follows:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chaostoolkit-experiment-1234
  namespace: chaostoolkit-run
data:
  experiment.yaml: |
    ---
    title: "..."
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  pod:
    experiment:
      configMapName: chaostoolkit-experiment-1234
      configMapExperimentFileName: experiment.yaml
```

### Load the experiment from a URL

By default, the experiment is read from a file. But you may store it remotely
e.g. GitHub and have it available over HTTP. You might want to load it from
its remote URL instead.

You can tell the Chaos Toolkit to load it from a remote URL rather than from
a local file, as follows:

```yaml
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
  pod:
    experiment:
      asFile: false

```

First, you need to pass the `EXPERIMENT_URL` environment variable.

Then, tell the operator not to mount the default experiment volume. To do so,
you need to set `asFile` to `false` in the `experiment` block of the pod spec.

### Run experiments in another namespace

You may create the namespace in which the resources will be deployed:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: my-other-namespace
```

You need to defined the `namespace` value at the spec level.

If the namespace already exists, a message will be logged but this will not
abort the operation.

However, this namespace will be entirely under your responsibility. No network
nor pod securities will be managed in your namespace, if the operator was 
installed with those variants. You'll need to manage them yourself.  

### Pass Chaos Toolkit settings as a Kubernetes secret

Chaos Toolkit reads its settings from a file and you can pass yours
by creating a Kubernetes secret named, by default, `chaostoolkit-settings`.

For instance, assuming you have a Chaos Toolkit settings file,
you can create a secret from it as follows:

```console
$ kubectl -n chaostoolkit-run \
    create secret generic chaostoolkit-settings \
    --from-file=settings.yaml=./settings.yaml
```

Note, the settings file must be named as `settings.yaml` within the secret.

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

You need to set the variable `enabled` to `true`in the `settings` block of the 
pod spec.

The default name for that secret is `chaostoolkit-settings` but you can change
it with the `secretName` variable, as follows:

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
      secretName: my-super-secret
```


### Keep generated resources even when the CRO is deleted

When you delete the `ChaosToolkitExperiment` resource, all the allocated
resources are deleted too (pod, service account, ...). To prevent this, you may
set the `keep_resources_on_delete` property to `true` at the spec level. 

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
  keep_resources_on_delete: true
```

In that case, you are responsible to cleanup all resources.

### Pass your own role to bind to the service account

If your cluster has enabled RBAC, then the operator automatically binds a basic
role to the service account associated with the chaostoolkit pod. That role
allows your experiment to create/get/list/delete other pods in the same
namespace.

You probably have more specific requirements, here is how to do it:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
  role:
    name: my-role
```

The property `name` should be set to the name of the role you have created in
the namespace which the experiment is executed in. The service account
associated with the pod will be bound to that role.

### Override the default chaos command arguments

The pod template executes the `chaos run` command by default. You may want to
extends or change the sub-command to execute when running the pod. You can
define the `chaos` arguments as follow:

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
    chaosArgs:
    - --verbose
    - run
    - --dry
    - $(EXPERIMENT_PATH)
```

You need to set the list of arguments in the `chaosArgs` variable at pod 
spec level.

### Label your Chaos Toolkit experiment

Experiment labels can be defined in the `ChaosToolkitExperiment`'s metadata.
All labels will be forwarded, if not already defined, in the pod running the
experiment.

You can define labels as follow:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
  labels:
    environment: staging
    tier: backend
    target: database
```

These labels can then be used as selectors.

### Allow network traffic for Chaos Toolkit experiments

When the operator is installed with the network security variant, the
`chaostoolkit` pod has limited network access. The pod is, by default,
isolated for ingress connectivity and is limited to only DNS lookup &
HTTPS for external traffic.

To allow the pod for other access, you may create another network policy
within the `chaostoolkit-run` namespace for pods matching the 
`app: chaostoolkit` label:

```yaml
---
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: my-custom-network-policy
  namespace: chaostoolkit-run
spec:
  podSelector:
    matchLabels:
      app: chaostoolkit
```


### Run periodic and recurring experiments

The operator supports `crontab` schedule for running Chaos Toolkit experiments
periodically on a given schedule.

To do so, you can define a `.spec.schedule` section, as follow:

```yaml
---
apiVersion: chaostoolkit.org/v1
kind: ChaosToolkitExperiment
metadata:
  name: my-chaos-exp
  namespace: chaostoolkit-crd
spec:
  namespace: chaostoolkit-run
  schedule:
    kind: cronJob
    value: "*/1 * * * *"
```

This example runs a Chaos Toolkit experiment every minute.

You can list your scheduled experiments with the kubernetes' `cronjob`
resource:

```
$ kubectl -n chaostoolkit-run get cronjobs
```

## Run an experiment with specific extensions

The default container image used by the operator is the official 
[Chaos Toollkit image][dockerfile] which embeds no
[Chaos Toolkit extensions][ext].

[dockerfile]: https://raw.githubusercontent.com/chaostoolkit/chaostoolkit/master/Dockerfile
[ext]: ../../drivers/overview.md

This means that you will likely need to create your bespoke container image.
For instance, to install the Chaos Toolkit Kubernetes extension, create
a Dockerfile like this:

```dockerfile
FROM chaostoolkit/chaostoolkit

USER root
RUN apk update && \
    apk add --virtual build-deps libffi-dev openssl-dev gcc python3-dev \
        musl-dev && \
    pip install --no-cache-dir chaostoolkit-addons chaostoolkit-reliably && \
    apk del build-deps
USER 1001
```

Then create the image with docker:

```
$ docker build --tag my/chaostoolkit -f ./Dockerfile .
```

or, something such as [Podman][]:

[podman]: https://podman.io/

```
$ podman build --tag my/chaostoolkit -f ./Dockerfile
```

You can check your image contains the installed extensions as follows:

```
$ docker run --rm -it my/chaostoolkit info extensions
```

Once this image is pushed to any registry you can access, you need to
let the operator know it must use it.

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
    image: my/chaostoolkit
```

## Uninstall the operator

To uninstall the operator and its own resources, simply run the following
command for the overlay that is deployed.

```console
$ kustomize build manifests/overlays/generic[-rbac[-podsec[-netsec]]] | kubectl delete -f -
```
