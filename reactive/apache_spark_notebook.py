# pylint: disable=unused-argument
from charms.reactive import when, when_not
from charms.reactive import set_state, remove_state
from charmhelpers.core import hookenv
from charms.layer.apache_spark_notebook import Notebook


@when('spark.ready')
@when_not('notebook.installed')
def install_notebook(spark):
    notebook = Notebook()
    hookenv.status_set('maintenance', 'Installing Notebook')
    notebook.install()
    set_state('notebook.installed')


@when('notebook.installed', 'spark.ready')
@when_not('notebook.started')
def configure_notebook(spark):
    hookenv.status_set('maintenance', 'Setting up Notebook')
    notebook = Notebook()
    notebook.configure_notebook()
    notebook.start()
    notebook.open_ports()
    set_state('notebook.started')
    hookenv.status_set('active', 'Ready')


@when('notebook.started')
@when_not('spark.ready')
def stop_notebook():
    hookenv.status_set('maintenance', 'Stopping Notebook')
    notebook = Notebook()
    notebook.close_ports()
    notebook.stop()
    remove_state('notebook.started')


@when_not('spark.joined')
def report_blocked():
    hookenv.status_set('blocked', 'Waiting for relation to Apache Spark')


@when('spark.joined')
@when_not('spark.ready')
def report_waiting(spark):
    hookenv.status_set('waiting', 'Waiting for Apache Spark to become ready')
