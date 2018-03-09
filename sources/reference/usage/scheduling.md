# Scheduling your Experiments

Scheduling is not built into the Chaos Toolkit itself. However it is common 
to want to run an experiment periodically when you may not be at the keyboard.

In these cases we recommend using a system such as 
[`cron`](https://en.wikipedia.org/wiki/Cron) to schedule your experiment 
executions. You can also use a [Kubernetes job](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) 
 to give you full control over the lifecycle of that job using the 
 common Kubernetes features.
