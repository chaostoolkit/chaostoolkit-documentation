# Running Chaos Toolkit experiments as AWS Batch Jobs

It is common when using AWS for hosting your infrastructure that you'll have
strict security policies in place. These policies will usually only allow for
internal traffic within AWS, amongst various other things. A question we're
asked a lot is `can I run Chaos Toolkit from AWS, to run against AWS?`.
The answer is simply, yes, you can.

## Why Batch?

You may have followed our [Running Chaos Toolkit from an EC2 instance][] guide
and wonder why we would write a guide for Batch - Batch has some benefits
over EC2:

* Your infrastructure isn't running all the time
* You can use Docker images to encapsulate your experiment environment
* You can submit multiple jobs to run different experiments rather than blocking
on one experiment in an EC2 instance

## Why not ECS and Fargate?

We sometimes get asked about how to run Chaos Toolkit **on** ECS with Fargate,
whilst we understand why you might want to do this, Chaos Toolkit experiments
aren't analogous to something like a microservice. We don't run Chaos Toolkit
continuously and request it to run jobs, rather we invoke Chaos Toolkit when we
want to use it.

Because of this difference in thinking, we recommend you use Batch (With Fargate
as the compute provider) to invoke Chaos Toolkit experiments.

## The Steps

For the purposes of this guide, we'll run you through setting up your Chaos Toolkit
experiments manually. If however, you're familiar with [the AWS Cloud Development
Kit (CDK)][], we have an example repository deploying the same infrastructure
using CDK [here][].

[the AWS Cloud Development Kit (CDK)]: https://docs.aws.amazon.com/cdk/latest/guide/home.html

[here]: https://github.com/chaostoolkit/chaostoolkit-aws-batch-example

There are a few pre-requisites required to be able to follow this guide:

* You'll need access to the AWS Console (We're assuming you're comfortable here)
* You'll need [AWS CLI][] installed and configured
* You'll need to be able to create EC2 instances (Or have someone do this for
you)
* You'll need to be able to create IAM Roles and Policies (Or have someone do
this for you)
* You'll need to be able to create Batch Compute Environments, Jobs, and Queues
(Or have someone do this for you)
* You'll need to be able to create ECR Repositories and push to them (Or have
someone to do this for you)

[AWS CLI]: https://aws.amazon.com/cli/

### 1. Create your system (an EC2 instance)

Similar to our [Running Chaos Toolkit from an EC2 instance][] guide, we'll be
using an EC2 instance as our 'system' to run our experiment against. We'll setup
our SSH to ensure that the EC2 instance is in a `running` state.

[Running Chaos Toolkit from an EC2 instance]: ../ec2/

* Navigate to the EC2 console and select `Launch Instance`
* For this guide, we'll select the `Amazon Linux 2 AMI` at the top of the list
* For this guide, we'll select a `t2.micro` (But you can choose a larger one)
* Go onto `Configure Instance Details`
* Select the VPC to deploy into via the `Network` dropdown
* Select the Subnet to deploy into via the `Subnet` dropdown
* Go onto `Add Storage` - For now, the defaults will be fine
* Go onto `Add Tags` - We recommend at minimum, adding a tag `{"OWNER":
"your-name"}`
* Go onto `Configure Security Group`
* Click the `X` to the right of the SSH rule, you won't need this
* Go onto `Review and Launch` - Select `Launch`
* Select `Proceed without a key pair`, check the tickbox, and click `Launch
Instances`

You can leave this instance up for the duration of this guide.

### 2. Create your experiment

In an empty directory, create a folder named `experiments`:

```console
mkdir experiments
```

Create a file named `experiment-1.json` inside `experiments/` with the following
contents:

```json
{
    "title": "Running Chaos Toolkit from AWS Batch",
    "description": "N/A",
    "tags": [],
    "steady-state-hypothesis": {
        "title": "EC2 is RUNNING",
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

Replace the value of `<INSTANCE_ID>` with the value of the id of the deployed
instance. Replace `<REGION>` with the name of the region the instance is deployed
in.

### 3. Setup your Docker image

AWS Batch requires us to have a Docker image within the Job definition, this
container will be _what_ does the work for our Batch Job.

Make a file named `Dockerfile` alongside `experiments/` with the following
contents:

```Dockerfile
FROM chaostoolkit/chaostoolkit:latest

RUN pip install chaostoolkit-aws

RUN mkdir /home/svc/experiments

COPY experiments /home/svc/experiments

WORKDIR /home/svc/experiments
```

### 4. Create your ECR repository and push the image

* Navigate to the ECR console and select `Repositories`
* Select `Create Repository`
* Leave the repository set to `Private` and enter a name for your repository
    * For the purpose of this guide, we'll be using `ctk-batch`
* Select `Create Repository`
* Select `<repository-name>` from the table
* Select `View push commands`
* Follow the commands outlined there (We'll show you them below as an example)

**Logging in to ECR with Docker**
```console
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.eu-west-2.amazonaws.com
```

```console
Login Succeeded
```

**Building the image**
```console
docker build -t ctk-batch .
```

```console
[+] Building 1.8s (10/10) FINISHED
 => [internal] load build definition from Dockerfile        0.0s
 => => transferring dockerfile: 220B                        0.0s
 => [internal] load .dockerignore                           0.0s
 => => transferring context: 2B                             0.0s
 => [internal] load metadata for docker.io/chaostoolkit/chaostoolkit:latest                                                         1.5s
 => [1/5] FROM docker.io/chaostoolkit/chaostoolkit:latest@sha256:3801eda37de7e8f00fb556220fff7935fea45d248881f4253cd9c29b4d3023f3   0.0s
 => => resolve docker.io/chaostoolkit/chaostoolkit:latest@sha256:3801eda37de7e8f00fb556220fff7935fea45d248881f4253cd9c29b4d3023f3   0.0s
 => [internal] load build context                           0.0s
 => => transferring context: 959B                           0.0s
 => CACHED [2/5] RUN pip install chaostoolkit-aws           0.0s
 => CACHED [3/5] RUN mkdir /home/svc/experiments            0.0s
 => [4/5] COPY experiments /home/svc/experiments            0.0s
 => [5/5] WORKDIR /home/svc/experiments                     0.0s
 => exporting to image                                      0.1s
 => => exporting layers                                     0.0s
 => => writing image sha256:4a3ce8f2824518bffa47ff3d293488f18f83e25711bedc32e13611a5c7e7e0af                                        0.0s
 => => naming to docker.io/library/ctk-batch                0.0s
```

**Tagging the image**
```console
docker tag ctk-batch:latest <your-aws-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ctk-batch:latest
```

**Pushing the image**
```console
docker push <your-aws-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ctk-batch:latest
```

```console
The push refers to repository [<your-aws-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ctk-batch]
5f70bf18a086: Pushed
ed804ed04ee1: Pushed
8ac8250b5bff: Pushed
65bb6a66824b: Pushed
381a8a9c329b: Pushed
7a767cefe1f5: Pushed
011386fb6049: Pushed
ac4086fc0a4e: Pushed
065eb9ef9cc4: Pushed
93ee5bc36b87: Pushed
9cc956b239dd: Pushed
bc276c40b172: Pushed
latest: digest: sha256:9702b9cf63a6e4961689a661340fc0573d28d0e7f506b90fa5d080e4e7c9d275 size: 2826
```

### 5. Create your Batch Compute environment

To actually run your Jobs, Batch needs a Compute environment configured. This is
where you tell AWS _what_ runs the jobs (i.e EC2 instances/Fargate/etc.).

* Navigate to the Batch console and select `Compute environments`
* Select `Create`
* Leave `Managed` selected and provide a name
    * For the purpose of this guide we'll use `ctk-batch-comp-env`
* Leave `Fargate` selected under `Instance configuration` but set `Maximum vCPUs`
to `1`
* If you want to use a specific VPC, Subnets, and Security Group, select those
in `Networking`
    * For this guide, we'll use the values AWS filled in
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Create compute environment`


### 6. Create your Batch Job queue

When you submit Jobs, Batch uses a Job queue to manage what is and needs to be
running and where it needs to run.

* Navigate to the Batch console and select `Job queues`
* Select `Create`
* Give a name for the Job queue
    * For the purpose of this guide we'll use `ctk-batch-job-queue`
* Leave priority as `1`
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* In the `Connected compute environments` section, select your Compute environment
from the dropdown
* Select `Create`

### 7. Create your Batch Job execution role

Because you've set up an ECR repository with your Docker image in, you need to
provide Batch with an execution role that will allow it to pull the image from
ECR. It will also enable Batch to output the logs of the container to CloudWatch.

Don't be confused when we refer to `Elastic Container Service`, Batch is using
it under the hood.

* Navigate to the IAM console and select `Roles`
* Select `Create role`
* Select `Elastic Container Service` from the list
* Select `Elastic Container Service Task` from the `Select your use case` list
* Select `Next: Permissions`
* In the search bar, type `AmazonECSTaskExecutionRolePolicy` and select it
* Select `Next: Tags`
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Next: Review`
* Provide a name for the Role
    * For the purpose of this guide we'll use `ctk-batch-execution-role`
* Select `Create Role`

### 8. Create your Batch Job job role

The nature of `chaostoolkit-aws` means that we use `boto3` to make AWS requests
within our experiment. To be able to make these calls, the container that is
running our experiment needs credentials and permissions to do so.

By creating a job role for our Job, we can:

* Provide our Job with credentials with AWS
* Outline exactly _what_ our Job is allowed to do

* Navigate to the IAM console and select `Roles`
* Select `Create role`
* Select `Elastic Container Service` from the list
* Select `Elastic Container Service Task` from the `Select your use case` list
* Select `Next: Permissions`
* Select `Create policy`
* Move to the `JSON` tab and paste the following:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstance*"
            ],
            "Resource": "*"
        }
    ]
}
```
* Select `Next: Tags`
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Next: Review`
* Provide a name for the Policy
    * For the purpose of this guide we'll use `ctk-batch-job-policy`
* Select `Create Policy`
* Navigate back to the Role tab
* In the search bar, type `ctk-batch-job-policy` and select it (You may have to
click the refresh button)
* Select `Next: Tags`
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Next: Review`
* Provide a name for the Role
    * For the purpose of this guide we'll use `ctk-batch-job-role`
* Select `Create Role`

### 9. Create your Batch Job definition

This is where we tell AWS _what_ our Job is and needs.

* Navigate to the Batch console and select `Job definitions`
* Select `Create`
* Provide a name
    * For the purpose of this guide we'll use `ctk-batch-job-def`
* Leave `Fargate` selected
* Scroll down to `Container properties`
* For `Image`, provide the URI of your ECR image from earlier
    * For example, when writing this guide, ours is:
 `<our-aws-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ctk-batch:latest`
* Leave `Bash` selected and inside command put: `run experiment-1.json`
* Select `0.25` for `vCpus` and `0.5 GB` for `Memory`
* Select `ctk-batch-execution-role` from the `Execution role` dropdown
* If your Compute environment is using **Public** subnets, select `Assign public
IP`
    * If you're using **Private** subnets, please follow [this StackOverflow post][]
    on what best setup to have to enable your jobs to communicate with ECR
* Select `Additional configuration`
* Select `ctk-batch-job-role` from the `Job role` dropdown
* Scroll down to the `Log configuration` section
* Select `awslogs` from the `Log driver` dropdown
* Scroll down to the `Tags` section
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Enable` under `Propagate Tags`
* Select `Create`

[this StackOverflow post]: https://stackoverflow.com/a/66802973

### 10. Run your experiment

Now that you have:

* Setup your 'system'
* Setup your container with its dependencies and experiments
* Setup your ECR repository
* Setup your required IAM Roles and Policies
* Setup your Batch Job Compute Environment, Queue, and Definition

It's a great time to try and run it!

* Navigate to the Batch console and select `Jobs`
* Select `ctk-batch-job-queue` from the `Please select a job queue` dropdown
* Select `Submit new job`
* Enter a name (This can be anything)
* Select `ctk-batch-job-def` from the `Job definition` dropdown
* Select `ctk-batch-job-queue` from the `Job queue` dropdown
* Scroll down to the `Tags` section
* Add a tag - We recommend at minimum, adding a tag `{"OWNER": "your-name"}`
* Select `Submit`
* Select `ctk-batch-job-queue` from the `Please select a job queue` dropdown
* You can see your job, select it
* Under `Job status` you'll see the different states move along (Hit the refresh
button)
* Once `Succeeded` is reached, you can select the link under `Log stream name`

Here you'll find the CloudWatch logs of the experiment:

```console
No older events at this moment. Retry
[2021-08-19 14:02:42 INFO] Validating the experiment's syntax
[2021-08-19 14:02:42 INFO] Experiment looks valid
[2021-08-19 14:02:42 INFO] Running experiment: Running Chaos Toolkit from AWS Batch
[2021-08-19 14:02:42 INFO] Steady-state strategy: default
[2021-08-19 14:02:42 INFO] Rollbacks strategy: default
[2021-08-19 14:02:42 INFO] Steady state hypothesis: EC2 is RUNNING
[2021-08-19 14:02:42 INFO] Probe: instance_state
[2021-08-19 14:02:43 INFO] Steady state hypothesis is met!
[2021-08-19 14:02:43 INFO] Playing your experiment's method now...
[2021-08-19 14:02:43 INFO] No declared activities, let's move on.
[2021-08-19 14:02:43 INFO] Steady state hypothesis: EC2 is RUNNING
[2021-08-19 14:02:43 INFO] Probe: instance_state
[2021-08-19 14:02:43 INFO] Steady state hypothesis is met!
[2021-08-19 14:02:43 INFO] Let's rollback...
[2021-08-19 14:02:43 INFO] No declared rollbacks, let's move on.
[2021-08-19 14:02:43 INFO] Experiment ended with status: completed
No newer events at this moment. Auto retry paused. Resume
```

## Summary

Like our [Running Chaos Toolkit from an EC2 instance][] guide, our experiment
was extremely simple. Again, this guide was not meant to teach you to write
experiments. The purpose of the guide was to show you how you might run
Chaos Toolkit **from** AWS to interact with your AWS infrastructure, in a more
reactive process.

Rather than having an EC2 instance running and not doing any work, you have the
ability now to fire off Chaos Toolkit experiments and only use the compute you
need.

You should now have an appreciation and the ability to:

* Create a containerised setup for Chaos Toolkit
* Setup IAM Roles and Policies to restrict and enable your Batch Jobs to run
* Create and run Batch Jobs which will carry out your Chaos Toolkit experiments
    * More importantly, within your infrastructures networking limits

## Extras

Whilst the above guide will tell you all you need to know to get started with
AWS Batch and running Chaos Toolkit experiments with jobs, it is very manual and
has a few shortcomings that are easily fixed with some more work.

### AWS Cloud Development Kit (CDK)

As mentioned near the start of this guide, we have [this repository][] which
contains an AWS CDK project which deploys almost the same infrastructure as
this guide.

The infrastructure differs slightly in:

* We create our own new VPC
* We specifically place our Compute environment in private subnets
* AWS CDK auto-magically sets up networking infrastructure for us to communicate
with ECR without having to give our Jobs public IP addresses

We also modify the `experiment-1.json` file to accept an environment variable for
the EC2 instance ID as this will be provided by CDK.

If you wish to try this project out, clone the repository and ensure you install
[all of the requirements][] first.

Once you're setup with the requirements, you can check what infrastructure will
be deployed with:

```console
make diff
```

```console
...
Resources
[+] AWS::S3::Bucket journal-bucket-your-name-dev journalbucketyour-namedev58D204DE
[+] AWS::S3::BucketPolicy journal-bucket-your-name-dev/Policy journalbucketyour-namedevPolicyDFBFADE1
[+] Custom::S3AutoDeleteObjects journal-bucket-your-name-dev/AutoDeleteObjectsCustomResource journalbucketyour-namedevAutoDeleteObjectsCustomResourceB5FE1104
[+] AWS::IAM::Role Custom::S3AutoDeleteObjectsCustomResourceProvider/Role CustomS3AutoDeleteObjectsCustomResourceProviderRole3B1BD092
[+] AWS::Lambda::Function Custom::S3AutoDeleteObjectsCustomResourceProvider/Handler CustomS3AutoDeleteObjectsCustomResourceProviderHandler9D90184F
[+] AWS::EC2::VPC vpc-your-name-dev vpcyour-namedev8A672852
[+] AWS::EC2::Subnet vpc-your-name-dev/PublicSubnet1/Subnet vpcyour-namedevPublicSubnet1Subnet4E80B3F7
[+] AWS::EC2::RouteTable vpc-your-name-dev/PublicSubnet1/RouteTable vpcyour-namedevPublicSubnet1RouteTable3BA26768
[+] AWS::EC2::SubnetRouteTableAssociation vpc-your-name-dev/PublicSubnet1/RouteTableAssociation vpcyour-namedevPublicSubnet1RouteTableAssociationF3D844E7
[+] AWS::EC2::Route vpc-your-name-dev/PublicSubnet1/DefaultRoute vpcyour-namedevPublicSubnet1DefaultRouteD7E793DD
[+] AWS::EC2::EIP vpc-your-name-dev/PublicSubnet1/EIP vpcyour-namedevPublicSubnet1EIP712EAA5B
[+] AWS::EC2::NatGateway vpc-your-name-dev/PublicSubnet1/NATGateway vpcyour-namedevPublicSubnet1NATGatewayCC6D84C6
[+] AWS::EC2::Subnet vpc-your-name-dev/PublicSubnet2/Subnet vpcyour-namedevPublicSubnet2Subnet3E3E0046
[+] AWS::EC2::RouteTable vpc-your-name-dev/PublicSubnet2/RouteTable vpcyour-namedevPublicSubnet2RouteTable1AB520E0
[+] AWS::EC2::SubnetRouteTableAssociation vpc-your-name-dev/PublicSubnet2/RouteTableAssociation vpcyour-namedevPublicSubnet2RouteTableAssociation2FEAAF25
[+] AWS::EC2::Route vpc-your-name-dev/PublicSubnet2/DefaultRoute vpcyour-namedevPublicSubnet2DefaultRouteC103C9D2
[+] AWS::EC2::EIP vpc-your-name-dev/PublicSubnet2/EIP vpcyour-namedevPublicSubnet2EIP6AD92B60
[+] AWS::EC2::NatGateway vpc-your-name-dev/PublicSubnet2/NATGateway vpcyour-namedevPublicSubnet2NATGatewayA09AEBA1
[+] AWS::EC2::Subnet vpc-your-name-dev/PrivateSubnet1/Subnet vpcyour-namedevPrivateSubnet1SubnetB315A65A
[+] AWS::EC2::RouteTable vpc-your-name-dev/PrivateSubnet1/RouteTable vpcyour-namedevPrivateSubnet1RouteTableA5FAAF1C
[+] AWS::EC2::SubnetRouteTableAssociation vpc-your-name-dev/PrivateSubnet1/RouteTableAssociation vpcyour-namedevPrivateSubnet1RouteTableAssociationE3B5D7DD
[+] AWS::EC2::Route vpc-your-name-dev/PrivateSubnet1/DefaultRoute vpcyour-namedevPrivateSubnet1DefaultRoute9152FB24
[+] AWS::EC2::Subnet vpc-your-name-dev/PrivateSubnet2/Subnet vpcyour-namedevPrivateSubnet2Subnet414716F0
[+] AWS::EC2::RouteTable vpc-your-name-dev/PrivateSubnet2/RouteTable vpcyour-namedevPrivateSubnet2RouteTable225072CD
[+] AWS::EC2::SubnetRouteTableAssociation vpc-your-name-dev/PrivateSubnet2/RouteTableAssociation vpcyour-namedevPrivateSubnet2RouteTableAssociationF9EA82A2
[+] AWS::EC2::Route vpc-your-name-dev/PrivateSubnet2/DefaultRoute vpcyour-namedevPrivateSubnet2DefaultRoute7BE0AFBF
[+] AWS::EC2::InternetGateway vpc-your-name-dev/IGW vpcyour-namedevIGW70FB840E
[+] AWS::EC2::VPCGatewayAttachment vpc-your-name-dev/VPCGW vpcyour-namedevVPCGWB8F53F81
[+] AWS::EC2::SecurityGroup instance-your-name-dev/InstanceSecurityGroup instanceyour-namedevInstanceSecurityGroup50C02701
[+] AWS::IAM::Role instance-your-name-dev/InstanceRole instanceyour-namedevInstanceRoleF653EE93
[+] AWS::IAM::InstanceProfile instance-your-name-dev/InstanceProfile instanceyour-namedevInstanceProfile6799F951
[+] AWS::EC2::Instance instance-your-name-dev instanceyour-namedev8DD0F85A
[+] AWS::IAM::Role batch-service-role-your-name-dev batchserviceroleyour-namedevB064BF84
[+] AWS::IAM::Role batch-execution-role-your-name-dev batchexecutionroleyour-namedev39DE3188
[+] AWS::IAM::Policy batch-execution-policy-your-name-dev batchexecutionpolicyyour-namedev8BCEF321
[+] AWS::IAM::Role batch-job-role-your-name-dev batchjobroleyour-namedevAC17F802
[+] AWS::IAM::Policy batch-job-role-your-name-dev/DefaultPolicy batchjobroleyour-namedevDefaultPolicy44B9665C
[+] AWS::IAM::Policy batch-job-policy-your-name-dev batchjobpolicyyour-namedev9C329AAB
[+] AWS::Batch::ComputeEnvironment compute-env-your-name-dev computeenvyour-namedev
[+] AWS::Batch::JobQueue job-queue-your-name-dev jobqueueyour-namedev
[+] AWS::Batch::JobDefinition job-def-your-name-dev jobdefyour-namedev
```

To deploy the infrastructure, run:

```console
make deploy
```

```
...
ChaosToolkitBatchExampleStack-your-name-dev: creating CloudFormation changeset...
[███████████████████████████████████████████████▏··········] (35/43)
09:24:07 | CREATE_IN_PROGRESS   | AWS::CloudFormation::Stack            | ChaosToolkitBatchExampleStack-your-name-dev
09:24:52 | CREATE_IN_PROGRESS   | AWS::IAM::InstanceProfile             | instance-your-name-dev/InstanceProfile
09:25:13 | CREATE_IN_PROGRESS   | AWS::EC2::NatGateway                  | vpc-your-name-dev/PublicSubnet2/NATGateway
09:25:13 | CREATE_IN_PROGRESS   | AWS::EC2::NatGateway                  | vpc-your-name-dev/PublicSubnet1/NATGateway
...
```

You can then navigate to the Batch console and run jobs as previously outlined
in the guide above.

[this repository]: https://github.com/chaostoolkit/chaostoolkit-aws-batch-example

[all of the requirements]: https://github.com/chaostoolkit/chaostoolkit-aws-batch-example#requirements-

### Storing your journal

You might have noticed that being able to view the Chaos Toolkit experiment
journal presents a pickle of a situation. As Batch Job containers are ephemeral,
once the Job has run and terminated (either successfully or not), the place your
experiment just ran in is destroyed for good.

There are likely several ways you could get around this issue, you could implement
an extension to upload journals somewhere, you could extend [chaostoolkit-aws][]
to upload journal runs to S3 or to an EBS volume (if you'd deployed that too).

In the [CDK](#aws-cloud-development-kit-cdk) example, we actually snuck in a way
to store journals; we use a wrapper script which calls `chaostoolkit` and then
uses `boto3` in a Python script to upload the journal to S3, into a bucket we
also deploy in the stack.

Take a look at our `Dockerfile` compared to the one in the guide above:

```Dockerfile
FROM chaostoolkit/chaostoolkit:latest

RUN pip install chaostoolkit-aws

RUN mkdir /home/svc/experiments

COPY experiments /home/svc/experiments
COPY run_experiment.sh /home/svc/experiments/
COPY upload_journal.py /home/svc/experiments/

WORKDIR /home/svc/experiments

ENTRYPOINT [ "sh", "run_experiment.sh" ]
```

We've added two new `COPY` statements, moving our wrapper script and our upload
script into the container. We've also added an override to the containers
`ENTRYPOINT` value, which in `chaostoolkit/chaostoolkit:latest` is `chaos`.

The wrapper script is very simple, it just looks like:

```bash
#!/bin/bash

chaos run $1 --journal-path=/home/svc/experiments/journal.json

python3 upload_journal.py
```

Our upload script is also very basic:

```python
import os
from datetime import datetime

import boto3


def upload_journal():
    s3 = boto3.client("s3")
    with open("/home/svc/experiments/journal.json", "rb") as journal:
        s3.upload_fileobj(
            journal,
            os.environ["JOURNAL_BUCKET"],
            f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
        )


if __name__ == "__main__":
    upload_journal()
```

With these changes and a small modification to the `command` of our Job definition,
we can now invoke our experiment, specify a location for our journal, and then
upload the journal with a suitable name - we set our journal name to the current
`datetime`. You could also include your experiment name if you have many of them.


[chaostoolkit-aws]: https://github.com/chaostoolkit-incubator/chaostoolkit-aws
