# Technology Choices

## Python 3

The Chaos Toolkit is implemented in [Python 3][py3k]. A high-level language with
a long successfuly story for writing great software. It's a common choice for
tooling purpose.

The language supports readbility well and has a large ecosystem of libraries. It
is also well-spread and easy to install. The choice to not support Python 2 is
a look at Python's present and future.

The choice for a dynamic language was also motivated because the Chaos Toolkit
manipulates a lot of strings and that task is made straightforward with Python.

Although Python natively does not generate (though [it can be done][pyinst])
standalone binaries like [golang][go] would. We do not believe this will harm
the project and hope that package managers will eventually provide native
installers.

[py3k]: https://www.python.org/
[go]: https://golang.org/
[pyinst]: http://www.pyinstaller.org/

## Functional

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

## JSON

The experiment description and structure is encoded using JSON. The choice for
JSON over YAML is because it leaves less room for ambiguity and is marginally
less readable for a structure with a shallow depth like Chaos Toolkit
experiments.