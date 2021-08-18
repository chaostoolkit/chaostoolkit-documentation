# Running Chaos Toolkit from an EC2 instance

It is common when using AWS for hosting your infrastructure that you'll have
strict security policies in place. These policies will usually only allow for
internal traffic within AWS, amongst various other things. A question we're
asked a lot is `can I run Chaos Toolkit from AWS, to run against AWS?`. 
The answer is simply, yes, you can.

## Why EC2?

The reasons for providing a guide on running Chaos Toolkit from an EC2
instance are simple enough:

* Most AWS users are comfortable with EC2
* It is the most analogous service to running something on your own workstation

## The Steps

There are a few pre-requisites required to be able to follow this guide:

* You'll need access to the AWS Console (We're assuming you're comfortable here)
* You'll need to be able to create EC2 instances (Or have someone do this for
you)
* You'll need to be able to create IAM Roles and Policies (Or have someone do 
this for you)
* You'll need to be able to use [Systems Manager - Session Manager][]

[Systems Manager - Session Manager]: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html

### 1. Create your instance

* Navigate to the EC2 console and select `Launch Instance`
* For this guide, we'll select the `Amazon Linux 2 AMI` at the top of the list
* For this guide, we'll select a `t2.micro` (But you can choose a larger one)
* Go onto `Configure Instance Details`
* Select the VPC to deploy into via the `Network` dropdown
* Select the Subnet to deploy into via the `Subnet` dropdown
* To the right of `IAM role`, select `Create a new IAM role`
    * Create an instance profile as per the `Creating an instance profile with 
    minimal Session Manager permissions (console)` in this [Session Manager 
    Documentation][]
    * Go back to the EC2 wizard and select the newly created role in the 
    dropdown (You may have to click the refresh button)
* Go onto `Add Storage` - For now, the defaults will be fine
* Go onto `Add Tags` - We recommend at minimum, adding a tag `{"OWNER": 
"your-name"}`
* Go onto `Configure Security Group`
* Click the `X` to the right of the SSH rule, you won't need this
* Go onto `Review and Launch` - Select `Launch`
* Select `Proceed without a key pair`, check the tickbox, and click `Launch 
Instances`

[Session Manager Documentation]: https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-create-iam-instance-profile.html

### 2. Connect to your instance

* Navigate to the Systems Manager console and select `Session Manager`
* Select `Start Session`
* Select your instance from the `Target instances` table
* Select `Start session`
* A new tab will open with a terminal session open in the browser

### 3. Setup Chaos Toolkit

You'll see a prompt like:

```console
sh-4.2$
```

Change to the home directory with:

```console
cd ~
```

Create a new directory for your experimentation and navigate inside:

```console
mkdir my-experiments && cd my-experiments
```

Create a virtual environment for the Chaos Toolkit dependencies:

```console
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install --upgrade pip
```

Install `chaostoolkit` and its AWS extension `chaostoolkit-aws`:

```console
pip3 install chaostoolkit chaostoolkit-aws
```

### 4. Create an experiment

For the purpose of this guide, we will just create an experiment with a
Steady State Hypothesis that interrogates EC2 and checks that our **current**
instance, is in the `running` state. We don't have a method, we're merely showing
that we can talk to AWS from within AWS.

Create a file named `experiment.json` with the following contents:

```json
{
    "title": "Running Chaos Toolkit from an EC2 instance",
    "description": "N/A",
    "tags": [],
    "steady-state-hypothesis": {
        "title": "Current EC2 is RUNNING",
        "probes": [
            {
                "type": "probe",
                "name": "instance_state",
                "provider": {
                    "type": "python",
                    "module": "chaosaws.ec2.probes",
                    "func": "instance_state",
                    "arguments": {
                        "state": "running",
                        "instance_ids": [
                            "<INSTANCE_ID>"
                        ],
                        "filters": []
                    }
                },
                "tolerance": true
            }
        ]
    },
    "method": [],
    "configuration": {
        "aws_region": "<REGION>"
    }
}
```

Replace the value of `<INSTANCE_ID>` with the value of the id of the current
instance. Replace `<REGION>` with the name of the region the instance is deployed
in.

You can then run the experiment with:

```console
chaos run ./experiment.json
```

```
[2021-08-18 10:12:29 INFO] Validating the experiment's syntax
[2021-08-18 10:12:29 INFO] Experiment looks valid
[2021-08-18 10:12:29 INFO] Running experiment: Running Chaos Toolkit from an EC2 instance
[2021-08-18 10:12:29 INFO] Steady-state strategy: default
[2021-08-18 10:12:29 INFO] Rollbacks strategy: default
[2021-08-18 10:12:29 INFO] Steady state hypothesis: Current EC2 is RUNNING
[2021-08-18 10:12:29 INFO] Probe: instance_state
[2021-08-18 10:12:29 ERROR]   => failed: botocore.exceptions.ClientError: An error occurred 
(UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to 
perform this operation.
[2021-08-18 10:12:29 WARNING] Probe terminated unexpectedly, so its tolerance could not be validated
[2021-08-18 10:12:29 CRITICAL] Steady state probe 'instance_state' is not in the given tolerance so 
failing this experiment
[2021-08-18 10:12:29 INFO] Experiment ended with status: failed
```

You'll notice the error you just received:

```
failed: botocore.exceptions.ClientError: An error occurred 
(UnauthorizedOperation) when calling the DescribeInstances operation: You are not
authorized to perform this operation.
```

This is because your instance profile role you created earlier doesn't have a 
suitable policy statement allowing you to describe EC2 instances.

Navigate to the IAM console and find the Policy you created earlier, add the
following statement to it:

```json
{
    "Effect": "Allow",
    "Action": [
        "ec2:DescribeInstance*"
    ],
    "Resource": "*"
}
```

Run your experiment again:

```console
chaos run ./experiment.json
```

```
[2021-08-18 10:24:56 INFO] Validating the experiment's syntax
[2021-08-18 10:24:56 INFO] Experiment looks valid
[2021-08-18 10:24:56 INFO] Running experiment: Running Chaos Toolkit from an EC2 
instance
[2021-08-18 10:24:56 INFO] Steady-state strategy: default
[2021-08-18 10:24:56 INFO] Rollbacks strategy: default
[2021-08-18 10:24:56 INFO] Steady state hypothesis: Current EC2 is RUNNING
[2021-08-18 10:24:56 INFO] Probe: instance_state
[2021-08-18 10:24:56 INFO] Steady state hypothesis is met!
[2021-08-18 10:24:56 INFO] Playing your experiment's method now...
[2021-08-18 10:24:56 INFO] No declared activities, let's move on.
[2021-08-18 10:24:56 INFO] Steady state hypothesis: Current EC2 is RUNNING
[2021-08-18 10:24:56 INFO] Probe: instance_state
[2021-08-18 10:24:56 INFO] Steady state hypothesis is met!
[2021-08-18 10:24:56 INFO] Let's rollback...
[2021-08-18 10:24:56 INFO] No declared rollbacks, let's move on.
[2021-08-18 10:24:56 INFO] Experiment ended with status: completed
```

As you'll notice, your EC2 profile now has the suitable permissions. This should
ultimately give you a good sense on how IAM allows you to give specific permissions
to the instances running your Chaos Toolkit experiments.

## Summary

Whilst the experiment within this guide was simple, the guide was not meant to
teach you how to write experiments. The purpose of the guide was to show you how
you might run Chaos Toolkit **from** AWS to interact with your AWS infrastructure.

You should now have an appreciation and the ability to:

* Create an EC2 instance within your AWS network
* Securely connect to that instance via Session Manager
    * Negating the need for Security Group policies or SSH access
* Setup and run Chaos Toolkit from an EC2 instance
* Modify the IAM policies for your instance to increase/decrease the experiments
ability to interact with your systems.

### Notes

It should be noted that several things could be done differently in this guide to
suit your own setup, they could be as follows:

* Using a containerised setup like [prescribed in this guide][] within your
instance
* Using a git repository (whether pulled or created) to use version control on the
instance and keep your experiments in version control
* Storing experiments/experiment journals/experiment logs in S3 so they're
accessible to others in your organisation
* Connecting via SSH (if your organisation is less concerned about allowing
traffic from your local IP)

[prescribed in this guide]: ../containerising/
