# Authoring vs Operating

The Chaos Toolkit specifies an experimental protocol and format for your
chaos engineering capabilities. It is often interesting to distinguish, at
least in your mind, two roles.

## Author

The author of an experiment is responsible for defining the structure of the
experiment and its objective. The author does not have to be the one who
comes with the question the experiment tries to produce evidence for. Rather,
the author knows how to structure the experiment and ensures the outcome of an
experiment's execution can be interpreted in an objective way.

An author manipulates the following elements: steady-state hypothesis, method,
rollbacks.

## Operator

The operator of an experiment executes it. This role is not as clear cut as the
author's role and, quite often, both are the same person. However, it is
useful to keep in mind what an experiment requires to be operated.
Since you may end up with a fleet of Chaos Toolkit experiments
running concurrently, the operator should work to ensure the executions
happen in a safe and controlled manner.

An operator manipulates the following elements: controls, settings