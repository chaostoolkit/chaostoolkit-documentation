# How to Install the Chaos Toolkit

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/DoiUo45zZLvISEvnlfeh2Gjlb.js" id="asciicast-DoiUo45zZLvISEvnlfeh2Gjlb" async></script></div>

## Python Requirements

The [chaostoolkit CLI][cli] is implemented in Python 3 and this requires a
working Python installation to run. It officially supports Python 3.6+. It has
only been tested against [CPython][python].

[cli]: https://github.com/chaostoolkit/chaostoolkit
[python]: https://www.python.org/

### Install Python

Install Python for your system:

On MacOS X:

```
brew install python3
```

On Debian/Ubuntu:

```
sudo apt-get install python3 python3-venv
```

On Windows:

[Download the latest binary installer][pywin] from the Python website.

[pywin]: https://www.python.org/downloads/windows/

### Create a virtual environment

Dependencies can be installed for your system via its package management but,
more likely, you will want to install them yourself in a local virtual
environment.

```
python3 -m venv ~/.venvs/chaostk
```

Make sure to always activate your virtual environment before using it:

```
source  ~/.venvs/chaostk/bin/activate
```

!!! tip
    You may want to use [virtualenvwrapper][] to make this process much nicer.

[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/

## Install the CLI

Install `chaostoolkit` in the virtual environment as follows:

```
pip install -U chaostoolkit
```

You can verify the command was installed by running:

```
chaos --version
```

## Install Extensions

At this stage, you have installed the `chaos` command line and its core
library. To fully enjoy the Chaos Toolkit, you will also want to install
[extensions][ext] for the various facets of your journey into Chaos Engineering.

[ext]: https://github.com/search?utf8=%E2%9C%93&q=topic%3Achaostoolkit-extension&type=Repositories