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
chaos report --help
```
```
Usage: chaos report [OPTIONS] [JOURNAL]... REPORT

  Generate a report from the run journal(s).

Options:
  --export-format TEXT  Format to export the report to: html, markdown, pdf.
  --help                Show this message and exit.
```


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
chaos report --export-format=pdf chaos-report.json report.pdf
```

An HTML report can be produced using:

```
chaos report --export-format=html5 chaos-report.json report.html
```
