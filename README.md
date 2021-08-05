# The Chaos Toolkit documentation

[![Build](https://github.com/chaostoolkit/chaostoolkit-documentation/actions/workflows/build.yaml/badge.svg)](https://github.com/chaostoolkit/chaostoolkit-documentation/actions/workflows/build.yaml)
[![Requirements Status](https://requires.io/github/chaostoolkit/chaostoolkit-documentation/requirements.svg?branch=gh-pages)](https://requires.io/github/chaostoolkit/chaostoolkit-documentation/requirements/?branch=gh-pages)

Get to the [documentation][live] of the Chaos Toolkit.

[live]: http://docs.chaostoolkit.org/

## Contribute to the documentation

This project is based on [MkDocs][], a Python documentation generator based on
[Markdown][].

To get started, install Python 3 on your machine, a [virtual environment][venv]
and install the dependencies using [pip][] as follows:

```
pip install -r requirements.txt
```

[MkDocs]: http://www.mkdocs.org/
[Markdown]: https://daringfireball.net/projects/markdown/syntax
[venv]: https://virtualenv.pypa.io/en/stable/
[pip]: https://pip.pypa.io/en/stable/installing/

Once the dependencies are installed you need to ensure you have also installed
 any submodules (i.e. source code for the docs is in a separate submodule) 
using:

```
git submodule update --init
```

Finally you can start a local server to view the docs:

```
mkdocs serve
```

If you wish to contribute to this documentation, please submit a PR with your
changes for review.