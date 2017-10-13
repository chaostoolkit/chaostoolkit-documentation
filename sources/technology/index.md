## Technology

### Key values

The following key values of the Chaos Toolkit reflect the mindset the community
has when engineering the Chaos Toolkit project.

#### Simplicity

The Chaos Toolkit aims at being a simple piece of technology both from a user
and developer perspective.

To achieve simplicity, the Chaos Toolkit comes as a command line interface
driven by a description file. As a user, this means no code and no need to 
learn a programming language. As a developer, this reduces the functional
surface area to consider.

#### Extensibility

The Chaos Toolkit does not wish to be a monolith and strives to be extended to
fully reach its goal through community driven efforts.

By using a description file, the implementation is not prescribed by the Chaos
Toolkit project. Although we fully expect the community to eventually settle on
certain implementations of probes and actions.

#### Readability

We believe code readbility is a factor for positive maintenance and evolutivity.

Readable code never goes out of fashion. As the code of the Chaos Toolkit is
mostly written in Python, best practices such as defined in [PEP8][pep8].

[pep8]: https://www.python.org/dev/peps/pep-0008/

#### Diversity

Although not strictly speaking referring to the technological aspect of the 
project, having diversity in the community will contribute to a better project
overall.

### Core Projects

The Chaos Toolkit is made of several projects that work together to provide its
service.

#### chaostoolkit

The [chaostoolkit][] project is the command-line interface (CLI), in other words
the command executed by users to run their experiments.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

That project tries to remain as shallow as possible, only providing the user
interface commands by gluing other projects together.

This project is implemented in Python 3.

#### chaostoolkit-lib

The [chaostoolkit-lib][chaoslib] project is the core library which implements
the [core concepts][concepts] of the Chaos Toolkit.

[chaoslib]: https://github.com/chaostoolkit/chaostoolkit-lib
[concepts]: ../overview/concepts.md

This project is implemented in Python 3.

#### chaostoolkit-documentation

The [chaostoolkit-documehtation][chaosdoc] is the documentation source and
renderer of the Chaos Toolkit. Namely, that project generates the website you
are currently reading.

[chaosdoc]: https://github.com/chaostoolkit/chaostoolkit-documentation

This project is implemented in Python 3 by generating HTML from Markdown
documents.

### Extension Projects

In addition to the core projects, the Chaos Toolkit manages some extension
projects which provide probes and/or actions for experiments.

#### chaostoolkit-kubernetes

The [chaostoolkit-kubernetes][chaoskube] implements probes and actions
for experiments targetting a [Kubernetes][kubernetes] cluster. Those activities
are implemented as Python functions.

[chaoskube]: https://github.com/chaostoolkit/chaostoolkit-kubernetes
[kubernetes]: https://kubernetes.io/

This project is implemented in Python 3.

#### chaostoolkit-gremlin

The [chaostoolkit-gremlin][chaosgremlin] implements actions
for experiments exploring resource failures (CPU, Memory, Network...) in their
system through the [Gremlin, Inc.][gremlin] services. Those activities
are implemented as Python functions talking to the [Gremlin API][gremlinapi].

[chaosgremlin]: https://github.com/chaostoolkit/chaostoolkit-gremlin
[gremlin]: https://gremlininc.com/
[gremlinapi]: https://help.gremlininc.com/api/

This project is implemented in Python 3.

### Technical Choices

#### Python 3

The Chaos Toolkit is implemented in [Python 3][py3k]. A high-level language with
a long successfuly story for writing great software. It's a common choice for
tooling purpose.

The language supports readbility well and has a large ecosystem of libraries. It
is also well-spread and easy to install. The choice to not support Python 2 is
a look at Python's present and future.

The choice for a dynamic language was also motivated because the Chaos Toolkit
manipulates a lot of strings and that task is made straightforward with Python.

Although Python cannot generate (well, not easily) standalone binaries like
[golang][go] would. We do not believe this will harm the project and hope that
package managers will eventually provide native installers.

[py3k]: https://www.python.org/
[go]: https://golang.org/

#### Functional

Well, this project is not truly a functional piece of code but the code relies
as little as possible on stateful constructions as provided by classes.

Mutable data structures are used but mostly created and returned from functions
rather than modified.

Generally speaking, the project draws inspirations from certain ideas of 
[functional paradigms][funcpara] but does not enforce them strictly. One notable
area where the code strays away from these principles is the use of exceptions
rather than returning error codes. This may change if the community expresses
such an intention.

[funcpara]: https://en.wikipedia.org/wiki/Functional_programming

#### JSON

The experiment description and structure is encoded using JSON. The choice for
JSON over YAML is because it leaves less room for ambiguity and is marginally
less readable for a structure with a shallow depth like Chaos Toolkit
experiments.