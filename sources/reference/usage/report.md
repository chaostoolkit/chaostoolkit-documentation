# The `chaos report` command

You use the `chaos report` command to take the journal produced by the 
[`chaos run`](run.md) command and produce a report in a specified format.

Due to the many operating system-dependent features that the `chaos report` 
command relies upon, the `chaos report` command is not installed with the 
Chaos Toolkit CLI. To install the `chaos report` command you need to [install 
the `chaostoolkit-reporting` plugin and the dependencies appropriate to your 
own operating system](https://github.com/chaostoolkit/chaostoolkit-reporting).

Once the plugin is installed you can see the options available to you by 
executing:

```
(chaostk) $ chaos report --help
```

<div style="margin: 0 auto; text-align: center;"><script src="https://asciinema.org/a/CEBXHpfHDMKEvlxgJED8TfaHn.js" id="asciicast-CEBXHpfHDMKEvlxgJED8TfaHn" async></script></div>

A tutorial on how to use the `chaos report` command is available as part of the 
[Chaos Toolkit's Getting Started tutorials.](https://www.katacoda.com/chaostoolkit/courses/01-chaostoolkit-getting-started)

### Generating a report

When an experiment completes after using the `chaos run` command a journal is 
generated and stored in the `chaos-report.json` file. A PDF or HTML report may 
be generated from this journal using the [chaostoolkit-reporting][chaosreport] 
library.

[chaosreport]: https://github.com/chaostoolkit/chaostoolkit-reporting

The `chaos report` command expects the path to the `chaos-report.json` file 
and a path to the actual report file that you require.

You can export various formats of report by specifying what you want using the 
`--export-format` option.

For example, to generate a PDF report you can run the following command:

```
$ chaos report --export-format=pdf chaos-report.json report.pdf
```

An HTML report can be produced using:

```
$ chaos report --export-format=html5 chaos-report.json report.html
```
