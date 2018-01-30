# How to Install the Chaos Toolkit

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/DoiUo45zZLvISEvnlfeh2Gjlb.js" id="asciicast-DoiUo45zZLvISEvnlfeh2Gjlb" async></script></div>

## Python Requirements

The [chaostoolkit CLI][cli] is implemented in Python 3 and this requires a
working Python installation to run. It officially supports Python 3.5+. It has
only been tested against [CPython][python].

[cli]: https://github.com/chaostoolkit/chaostoolkit

### Install Python

Install Python for your system:

On MacOS X:

```
$ brew install python3
```

On Debian/Ubuntu:

```
$ sudo apt-get install python3 python3-venv
```

On CentOS:

```
$ sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
$ sudo yum -y install python35u
```

Notice, on CentOS, the Python 3.5 binary is named `python3.5` rather than
`python3` as other systems.

On Windows:

[Download the latest binary installer][pywin] from the Python website.

[pywin]: https://www.python.org/downloads/windows/

### Create a virtual environment

Dependencies can be installed for your system via its package management but,
more likely, you will want to install them yourself in a local virtual
environment.

```
$ python3 -m venv ~/.venvs/chaostk
```

Make sure to always activate your virtual environment before using it:

```
$ source  ~/.venvs/chaostk/bin/activate
```

!!! tip
    You may want to use [virtualenvwrapper][] to make this process much nicer.

[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/

## Install the CLI

Install `chaostoolkit` in the virtual environment as follows:

```
(chaostk) $ pip install chaostoolkit
```

You can verify the command was installed by running:

```
(chaostk) $ chaos --version
```
