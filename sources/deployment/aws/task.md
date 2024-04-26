# Run Chaos Toolkit as a Task

AWS offers a range of services suitable to run a Chaos Toolkit experiments.
Here we will explore [AWS ECS Tasks][ecstask] to achieve this.

[ecstask]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html


!!! info
    We will be using [copilot][copilot] to generate all the necessary AWS
    resources. Please ensure you have installed the tool.

    [copilot]: https://aws.github.io/copilot-cli/

## Create the Task Definition

The Task definition describes all the information required to run the
process contained in the container image associated with the task. To create
the stask and all its resources, run the following commands:

```bash
copilot init \
    --app chaostoolkit \ # (1)!
    --name my-chaos \ # (2)!
    --image "chaostoolkit/chaostoolkit:basic" \ # (3)!
    --retries 0 \ # (4)!
    --schedule "@hourly" \ # (5)!
    --env "team-1" \ # (6)!
    --type "Scheduled Job"
    --deploy
```

1. Name the stack, make it relatable but unique to your organization and team
2. The name of the task
3. Container image to use
4. Don't retry the experiment when it fails
5. Schedule the task repeatedly
6. Create an environment specific for this task

!!! warning
    copilot does not currently support one-off jobs so you need to set
    a schedule during the creation of the stack.

    However, once the stack is created you can edit it and change it to:

    ```yaml title="./copilot/my-chaos/manifest.yaml"
    on:
      schedule: none
    ```

!!! tip

    Every change made to the manifest requires the stack to be deployed with:

    ```bash
    copilot deploy
    ```

## Configure the Experiment Location

The task created previously does not specify the experiment to be executed.

You can make it available in various fashion to the task:

1. Create a container image that contains that file. The issue here is that
   you will have to build the image for every change in the experiment and
   store as many images as you have experiments to run.
2. Store the experiment somewhere it can be served over HTTP since the
   Chaos Toolkit knows how to automatically read over HTTP. In this case,
   make the following [change][cmd] into the task definition file:

    ```yaml title="./copilot/my-chaos/manifest.yaml"
    command: ["run", "https://..."]
    ```

3. Mount a volume into the task so that the experiment file is dynamically
   made available to the Chaos Toolkit. You can use [EFS][efs] to achieve this.
   In this case, make the following change into the task definition file:

    ```yaml title="./copilot/my-chaos/manifest.yaml"
    command: ["run", "/home/svc/experiments/experiment.json"]
    storage:
      volumes:
        myManagedEFSVolume:
          efs: true
          path: /home/svc/experiments
          read_only: true
    ```

[cmd]: https://aws.github.io/copilot-cli/docs/manifest/scheduled-job/#command
[efs]: https://aws.github.io/copilot-cli/docs/developing/storage/#managed-efs

4. A final approach is to change the entry point of the base image so that
   it knows how to fetch the experiment before making it available to the
   `chaos` command. For instance, you could have a script that fetches the
   experiment from an S3 bucket and stores it into the
   `/home/svc/experiment.json`.

## Run the Task Definition

Run the task definition as follows:

```bash
copilot job run
```

## Schedule the Task Definition

Schedule the task definition by setting the [schedule][sched] property
in your task definition file.

[sched]: https://aws.github.io/copilot-cli/docs/manifest/scheduled-job/#on-schedule

## View the Task Run Logs

View the most recent logs:

```bash
copilot job log
```

## Delete the Task Definition

When the tasks and its resources are not necessary any longer, you can
remove them with:

```bash
copilot app delete --name chaostoolkit
```
