# Run Chaos Toolkit locally with Docker

Docker is a fantastic approach to package up your Chaos Toolkit experiment
dependencies and make it easy for anyone to run your experiments.

## Official Images

Chaos Toolkit offers three base images you can use.

* `chaostoolkit/chaostoolkit:latest` This is an Alpine based image and does
  not contain any extensions
* `chaostoolkit/chaostoolkit:basic` This is an Ubuntu based image and does
  not contain any extensions
* `chaostoolkit/chaostoolkit:full` This is an Ubuntu based image and does
  contains [many popular extensions][ext]

[ext]: https://github.com/chaostoolkit/chaostoolkit/blob/master/container/pyproject.toml

## Create your Own Container Image

While an image such as `chaostoolkit/chaostoolkit:full` is a good default
to start with, you will likely want to create your own image with specific
extensions and dependencies for your needs.

Let's see how to get on about it.

```bash title="Dockerfile"

FROM chaostoolkit/chaostoolkit:basic  # (1)!

COPY pyproject.toml pdm.lock /home/svc/  # (2)!

USER root  # (3)!

WORKDIR /home/svc

RUN apt-get update && \  # (4)!
    apt-get install -y --no-install-recommends curl python3.11-venv build-essential gcc && \  # (5)!
    curl -o install-pdm.py -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py && \  # (6)!
    python3.11 install-pdm.py -p /home/svc && \  # (7)!
    export PATH=/home/svc/bin:$PATH && \
    pdm use .venv && \  # (8)!
    pdm install --no-editable --no-self && \  # (9)!
    rm install-pdm.py && \
    chown --recursive svc:svc /home/svc/.venv  && \  # (10)!
    apt-get remove -y build-essential gcc && \  # (11)!
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER 1001  # (12)!

```

1. Let's start with the Ubuntu base
2. Copy the file listing the Python packages we want to install, see in the next section
3. Switch back to the admin user as we need to run priviledged commands
4. Refresh the system
5. We need the `curl` command to retrieve the Python package manager [PDM][pdm]
   used to install yopur packages. We also install the essentials to build
   extensions that require compilation. If your do not require it, you can
   usually safely remove `build-essential` and `gcc` to speed up the build
6. Fetch PDM
7. Install the `pdm` tool in the existing home directory
8. Switch to the Python environment created on the base image
9. Install your Python dependencies
10. Make everything we just installed owned by the `svc` user created in the
    base image
11. Tidy up
12. Switch bask to the `svc` user from now on

[pdm]: https://pdm-project.org/en/stable/

Before you can create your image, you now need to create a `pyproject.toml`
file listing the dependencies you wish to install. Here a basic one:

```toml title="pyproject.toml"
[project]
name = "my-experiment"  # (1)!
version = "0.1.0"  # (2)!
dependencies = []  # (3)!
requires-python = ">=3.11"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
distribution = false
```

1. Set any name you need, for the purpose of this file this name is not
relevant
2. Not relevant to our needs here so leave as-is
3. Contains the list of dependencies

To add dependencies, run the following command:

```bash
pdm add chaostoolkit-kubernetes
```

!!! tip
    Install `pdm` from [pdm][].

The first time this command is run, it generates the `pdm.lock` file
describing the specific version to install.

We're done!

You can now create the image with:

```bash
docker build -t my/chaostoolkit .
```

Once this image has been published to a container registry, it is available
to use by anyone with access or from other environments such as Kubernetes
or serverless providers.

## Run an Experiment

Let's assume you have this Chaos Toolkit experiment:

```json title="experiment.json"
{
    "version": "1.0.0",
    "title": "Hello world!",
    "description": "Say hello to the world.",
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
```

You can run this experiment as follows:

```bash
docker run -v `pwd`/experiment.json:/home/svc/experiment.json my/chaostoolkit run experiment.json
```
