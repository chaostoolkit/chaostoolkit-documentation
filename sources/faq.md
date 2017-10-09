## FAQ

### What is the Chaos Toolkit?

It is an open-source software that runs an experiment against your system to
confirm or infirm an hypothesis. Colloquially this refers to the 
C[haos Engineering Principles][principles].

[principles]: http://principlesofchaos.org/

### Why do I need to run experiments?

Systems do not live in a vacuum, they are subjected to real world events, some
expected and tolerated, others considered as attacks. Waiting for those
conditions arise does not give the time your team needs to handle, learn and
adapt to the situation at hand.

In many countries, fire alarm tests are conducted at random in offices so 
people learn how to react well for the benefit of everyone. Software systems
should go through the same exercises . The Chaos Toolkit hopes to make it 
simple and safe to run experiments like these.

### Why a toolkit?

Currently, running experiments is not an easy task because the ecosystem is 
still fairly young. Complex cases have been demonstrated at large corporations
such as Netflix or LinkedIn. Tools such as [ChAP][chap] or [Simoorg][simoorg]
are powerful but quite involved.


[chap]: https://medium.com/netflix-techblog/chap-chaos-automation-platform-53e6d528371f
[simoorg]: https://engineering.linkedin.com/blog/2016/03/deep-dive-Simoorg-open-source-failure-induction-framework

The Chaos Toolkit aims at providing a more straightforward initial user
experience to gain confidence in doing Chaos Engineering experiments. The
simpler it gets the greater our cognitive capacity to understand what is going
on.

Ultimately, the Chaos Toolkit should lead you on the path to using richer tools
such as those cited above.

### What does the Chaos Toolkit do?

The Chaos Toolkit user-interface is a command line that takes a JSON-encoded
file describing the experiment to run. It consists of a sequence of activities
the toolkit executes in order to produce a final report. 

The activities are of two kinds. Probes observe the system at various point of
the experiment. Actions interact with the system to change its state. Usually
the action represents the hypothesis you are trying to learn from.

### Who is behind the Chaos Toolkit?

The effort was initiated by [Russ Miles][russ] and
[Sylvain Hellegouarch][sylvain], two engineers passionate about fluidity in
complex systems. However, their vision is really to build a
[strong community][community] of engineer experiences to feedback
into the Chaos Toolkit.

[russ]: http://www.russmiles.com/
[sylvain]: http://www.defuze.org/
[community]: https://join.chaostoolkit.org/

### What is the license of the Chaos Toolkit?

[Apache 2.0][apache].

[apache]: https://github.com/chaostoolkit/chaostoolkit/blob/master/LICENSE 

### How can I contribute?

The Chaos Toolkit welcomes contributors! To help the project, please go to
the right project on [GitHub][gh] and create an issue. If you feel like it,
do not hesitate to fork the repository, make a change and submit a 
pull-request to the upstream project for review.

[gh]: https://github.com/chaostoolkit