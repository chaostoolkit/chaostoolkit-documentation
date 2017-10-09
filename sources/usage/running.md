# Running the Chaos Toolkit

The `chaostoolkit` CLI will display commands it supports as follows:

```
(chaostk) $ chaos --help
```

!!! note "Activate the Python virtual environment"

    If you run the Chaos Toolkit directly, rather than using a container,
    always ensure you have activated the virtual environment so that it can
    be found along its dependencies:

    ```
    $ source ~/.venvs/chaostk/bin/activate
    (chaostk) $
    ```

### Executing a plan

The main function of the `chaostoolkit` CLI is to execute the plan you
declared. This is done as follows:

```
(chaostk) $ chaos run my-plan.json
```

`chaostoolkit` will log all the steps it follows from your plan.

If you run the command from a container:

```
$ docker run --rm -it \
    --user `id -u` \
    -v $HOME/.kube:/root/.kube \
    -v $HOME/.minikube:$HOME/.minikube \
    -v `pwd`:/tmp/chaos \
    chaostoolkit/chaostoolkit run /tmp/chaos/my-plan.json
```

This command snippet shows how you would share your [Kubernetes][kube]
 and [minikube][] configurations if your experiment targets Kubernetes.

[kube]: https://kubernetes.io/
[minikube]: https://github.com/kubernetes/minikube


!!! warning "Battery not included in the container"

    Depending on your experiment, running as a container may not be as simple
    as it looks because all the extensions (Python packages, commands to run,
    config files...) are not included in the base image.

