# Containerising Chaos Toolkit

You may find yourself in a situation that requires you to run your Chaos Toolkit
Experiments from within a container. This may be to encapsulate the dependencies
required or to run CTK in a different environment, for whichever reason you have,
containerising CTK is straightforward.

## Using the vanilla `chaostoolkit` image

Chaos Toolkit builds and pushes a Docker Image upon every release of a new
version of the [chaostoolkit][] package. This can then be used out of the box
by referring to it locally on the command line with:

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```console
docker run chaostoolkit/chaostoolkit:latest info core
```

```console
Unable to find image 'chaostoolkit/chaostoolkit:latest' locally
latest: Pulling from chaostoolkit/chaostoolkit
Digest: sha256:3801eda37de7e8f00fb556220fff7935fea45d248881f4253cd9c29b4d3023f3
Status: Downloaded newer image for chaostoolkit/chaostoolkit:latest
NAME                VERSION   
CLI                 1.9.2     
Core library        1.19.0
```

It should be noted that this **only** contains vanilla `chaostoolkit`.

You could then mount a directory containing your experiments (if they are only
using vanilla `chaostoolkit`) and run them:

```console
docker run \
-v $PWD/experiments:/experiments \
chaostoolkit/chaostoolkit:latest \
--log-file /experiments/chaostoolkit.log \
run /experiments/experiment.json \
--journal-path /experiments/journal.json
```

You'd then find in `$PWD/experiments`:

```console
ls $PWD/experiments
```

```
chaostoolkit.log experiment.json  journal.json
```

## Containerising with extensions

More commonly you'll find that vanilla `chaostoolkit` doesn't have the activities
you need to interact with your services. For this kind of scenario, we recommend
that you build your own custom image, with `chaostoolkit/chaostoolkit:latest` as
the base.

### `chaostoolkit-aws` example

If for example, you needed certain [AWS activities][] for your chaos experiments,
you could create a Dockerfile like so:

[AWS activities]: https://chaostoolkit.org/drivers/aws/

```dockerfile
FROM chaostoolkit/chaostoolkit:latest

RUN pip install chaostoolkit-aws
```

To then use this, you'd first build the image:

```console
docker build -t ctk-aws .
```

```console
[+] Building 2.1s (6/6) FINISHED                                                                                                                                                            
 => [internal] load build definition from Dockerfile                                                                                0.0s
 => => transferring dockerfile: 114B                                                                                                0.0s
 => [internal] load .dockerignore                                                                                                   0.0s
 => => transferring context: 2B                                                                                                     0.0s
 => [internal] load metadata for docker.io/chaostoolkit/chaostoolkit:latest                                                         2.0s
 => [1/2] FROM docker.io/chaostoolkit/chaostoolkit:latest@sha256:3801eda37de7e8f00fb556220fff7935fea45d248881f4253cd9c29b4d3023f3   0.0s
 => => resolve docker.io/chaostoolkit/chaostoolkit:latest@sha256:3801eda37de7e8f00fb556220fff7935fea45d248881f4253cd9c29b4d3023f3   0.0s
 => CACHED [2/2] RUN pip install chaostoolkit-aws                                                                                   0.0s
 => exporting to image                                                                                                              0.0s
 => => exporting layers                                                                                                             0.0s
 => => writing image sha256:84f4579bee5ff42881a226643dbe37c8bc1e0ecb60e153c46395f9dc62a8f256                                        0.0s
 => => naming to docker.io/library/ctk-aws                                                                                          0.0s
```

Then you'd confirm `chaostoolkit-aws` is available with:

```console
docker run ctk-aws info extensions
```

```
NAME                                    VERSION   LICENSE                       DESCRIPTION
chaostoolkit-aws                        0.16.0    Apache License Version 2.0    AWS
```
