# Run Chaos Toolkit with a Google Cloud Platform Cloud Run Job

Google Cloud Platform Cloud Run Job is an ideal candidate when you need to
run a Chaos Toolkit experiment once or recurringly.

## Overview

This page describe the basics for running an experiment as a Cloud Run Job. It
should provide the skeleton for your own requirements.

In a nutshell, you will need:

* a container image with the Chaos Toolkit and the right extensions
* an experiment file. For the purpose of this documentation, we will host
  the experiment in a Google Cloud Storage bucket. It can be stored anywhere
  else that can be access over HTTP otherwise

## Create a Cloud Run Job

Below is an example of a Cloud Run Job manifest to run an experiment:

```yaml title="job.yaml"
apiVersion: run.googleapis.com/v1
kind: Job
metadata:
  name: chaostoolkit-experiment
  annotations:
    run.googleapis.com/client-name: chaostoolkit
    run.googleapis.com/launch-stage: BETA # (1)!
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
    spec:
      template:
        spec:
          serviceAccountName: chaostoolkit-cloud-run-job
          maxRetries: 0 # (2)!
          timeoutSeconds: 3600 # (3)!
          containers:
            - image: chaostoolkit/chaostoolkit:full # (8)!
              args:
                - --verbose
                - run
                - /home/svc/experiment/experiment.json
              resources:
                limits:
                  memory: 512Mi
                  cpu: "1"
              volumeMounts:
              - mountPath: /home/svc/experiment  # (4)!
                name: experiments
                subPath: experiment.json  # (5)!
          volumes:
          - name: experiments
            csi:
              driver: gcsfuse.run.googleapis.com  # (6)!
              readOnly: true
              volumeAttributes:
                bucketName: my_bucket  # (7)!
```


1. Required only to mount the Cloud Storage as a volume
2. A good idea to not retry automatically to run the experiment
3. Not strictly necessary but a good habit to control your bills
4. This is the directory we mount into the container to hold our experiment
   from the volume
5. The name of the Cloud Storage object in our bucket
6. Specific to Cloud Storage
7. Name of the bucket containing the experiment
8. Let's use a base image that contains a list of extensions

To create the job, we then run the following commands. First we create the
necessary service account and bind the appropriate role to mount the Cloud
Storage to it:

```bash
export PROJECT_ID=  # (1)!
export REGION=

gcloud config set run/region $REGION  # (2)!

gcloud iam service-accounts create chaostoolkit-cloud-run-job \  # (3)!
    --description="Runs Chaos Toolkit Experiments" \
    --display-name="Dedicated service account to run Chaos Toolkit experiments"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \  # (4)!
    --member="serviceAccount:chaostoolkit-cloud-run-job@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer" \
    --condition=None
```

1. Set the project identifier to your project
2. Set the correct region where to create and run the job
3. This is the service account associated with the job
4. We only need the `"roles/storage.objectViewer"` to mount the cloud storage
   as a volume

We now need a space to store our experiment file.

```bash
export REGION=
export BUCKET=my_bucket

gcloud storage buckets create gs://$BUCKET --location $REGION  # (1)!

gcloud storage cp ./experiment.json gs://$BUCKET  # (2)!
```

1. The bucket name is the one we set in the job configuration above
2. Copy the `experiment.json` file at the root of the bucket

Next, we can can now create the Cloud Run job:

```bash
gcloud run jobs replace job.yaml
```

You can view your job as well:

```bash
gcloud run jobs describe chaostoolkit-experiment
```

## Run the Experiment Once

Once you have created a job, you can run it at will as follows:

```bash
gcloud run jobs execute --wait chaostoolkit-experiment
```

This will run and wait for the job to complete and will output the URL
of the execution.

## Schedule the Experiment Repeatedly

To schedule the job to run recurringly, you will need another Google Cloud
service named the Scheduler.

Here is an example on how to schedule the experiment to run every Monday at
9am:

```bash
export PROJECT_ID=  # (1)!
export REGION= # (2)!

gcloud iam service-accounts create chaostoolkit-job-sched \
    --description="Schedules Chaos Toolkit Experiments" \
    --display-name="Dedicated service account to schedule Chaos Toolkit experiments"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:chaostoolkit-job-sched@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.invoker" \  # (3)!
    --condition=None

gcloud scheduler jobs create http my-experiment-schedule \
  --location ${REGION} \
  --http-method POST \
  --schedule="0 9 * * 1" \
  --time-zone "Etc/UTC" \  # (4)!
  --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/chaostoolkit-experiment:run" \
  --oauth-service-account-email chaostoolkit-job-sched@${PROJECT_ID}.iam.gserviceaccount.com
```

1. Set the project identifier to your project
2. Set the appropriate region where to run the scheduler from. The scheduler
   and the job do not need to reside in the same region
3. This role is required so the service account used to trigger the job is
   allowed to do it
4. A good idea to set the correct timezone

You can test the schedule without waiting for the first instance:

```bash
gcloud scheduler jobs run --location=${REGION} my-experiment-schedule
```

