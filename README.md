## Overview

IPython Notebook is a web-based notebook that enables interactive data analytics
for Spark. The developers of Apache Spark have given thoughtful consideration to
Python as a language of choice for data analysis. They have developed the
PySpark API for working with RDDs in Python, and further support using the
powerful IPythonshell instead of the builtin Python REPL.

The developers of IPython have invested considerable effort in building the
IPython Notebook, a system inspired by Mathematica that allows you to create
"executable documents." IPython Notebooks can integrate formatted text
(Markdown), executable code (Python), mathematical formulae (LaTeX), and
graphics/visualizations (matplotlib) into a single document that captures the
flow of an exploration and can be exported as a formatted report or an
executable script.


## Usage

This is a subordinate charm that requires the `apache-spark` interface. This
means that you will need to deploy a base Apache Spark cluster to use
the Notebook. An easy way to deploy the recommended environment is to use the
[apache-hadoop-spark-notebook](https://jujucharms.com/apache-hadoop-spark-notebook)
bundle. This will deploy the Apache Hadoop platform with an Apache Spark +
Notebook unit that communicates with the cluster by relating to the
`apache-hadoop-plugin` subordinate charm:

    juju-quickstart apache-hadoop-spark-notebook

Once deployment is complete, expose the Notebook:

    juju expose notebook

You may now access the web interface at
http://{spark_unit_ip_address}:9090. The ip address can be found by running
`juju status spark | grep public-address`.


## Verify the deployment

### Status

The services provide extended status reporting to indicate when they are ready:

    juju status --format=tabular

This is particularly useful when combined with `watch` to track the on-going
progress of the deployment:

    watch -n 0.5 juju status --format=tabular

The message for each unit will provide information about that unit's state.


## Contact Information

- <bigdata@lists.ubuntu.com>


## Help

- [Juju mailing list](https://lists.ubuntu.com/mailman/listinfo/juju)
- [Juju community](https://jujucharms.com/community)
