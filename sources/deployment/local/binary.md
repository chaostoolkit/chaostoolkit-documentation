# Run Chaos Toolkit as binary

Chaos Toolkit is a Python package and therefore adopts a deployment suitable
for Python environments.

However, the Chaos Toolkit project also provides read-y-to-do binaries that
can be downloaded and executed as-is on supported environments such as
Linux, MacOSX or Windows.

You can find these binaries on the [bundler][bundler] project.

[bundler]: https://github.com/chaostoolkit/chaostoolkit-bundler/releases/latest

Simply download the appropriate file for your architecture, rename it to `chaos`
make it executable and run as-is.

It contains a set of common extensions.

!!! warning

    The binary cannot see extensions that you have already on your machine. It
    only knows about the ones bundled within. Therefore the binary may be
    of limited use depending on your use case.
