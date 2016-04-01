import os

from path import Path
from jujubigdata import utils
from subprocess import check_output
from charmhelpers.core import hookenv


# Main Notebook class for callbacks
class Notebook(object):
    def __init__(self):
        self.dist_config = utils.DistConfig()

    def install(self):
        self.dist_config.add_dirs()

        # Copy our start/stop scripts (preserving attrs) to $HOME
        start_source = 'scripts/start_notebook.sh'
        Path(start_source).chmod(0o755)
        Path(start_source).chown('ubuntu', 'hadoop')

        stop_source = 'scripts/stop_notebook.sh'
        Path(stop_source).chmod(0o755)
        Path(stop_source).chown('ubuntu', 'hadoop')

        target = os.environ.get('HOME', '/home/ubuntu')
        Path(start_source).copy2(target)
        Path(stop_source).copy2(target)

        # Create an IPython profile
        utils.run_as("ubuntu", 'ipython', 'profile', 'create', 'pyspark')

    def configure_notebook(self):
        # profile config created during install
        ipython_profile = "ipython_notebook_config.py"
        # find path to ipython_notebook_config.py
        pPath = "/home/ubuntu/.ipython/profile_pyspark"
        cmd = ['find', pPath, '-name', ipython_profile]
        profile_config = check_output(cmd, universal_newlines=True).strip()

        # update profile with standard opts and configured port
        port = self.dist_config.port('notebook')
        notebooks_dir = self.dist_config.path('notebooks')
        utils.re_edit_in_place(profile_config, {
            r'.*c.NotebookApp.ip *=.*':
            'c.NotebookApp.ip = "*"',

            r'.*c.NotebookApp.open_browser *=.*':
            'c.NotebookApp.open_browser = False',

            r'.*c.NotebookApp.port *=.*':
            'c.NotebookApp.port = {}'.format(port),

            r'.*c.NotebookManager.notebook_dir *=.*':
            "c.NotebookManager.notebook_dir = u'{}'".format(notebooks_dir),
        })

        spark_home = os.environ.get("SPARK_HOME", '/usr/lib/spark')
        py4j = "py4j-0.*.zip"
        cmd = "find {} -name {}".format(spark_home, py4j)
        # TODO: handle missing py4j
        py4j_path = check_output(cmd.split(), universal_newlines=True).strip()

        setup_source = 'scripts/00-pyspark-setup.py'
        Path(setup_source).chmod(0o755)
        Path(setup_source).chown('ubuntu', 'hadoop')
        utils.re_edit_in_place(setup_source, {
            r'py4j *=.*': 'py4j="{}"'.format(py4j_path),
        })
        home = Path(os.environ.get('HOME', '/home/ubuntu'))
        profile_dir = home / '.ipython/profile_pyspark'
        setup_target = profile_dir / 'startup/00-pyspark-setup.py'
        Path(setup_source).copy2(setup_target)

        # Our spark charm defaults to yarn-client, so that should
        # be a safe default here in case MASTER isn't set. Update the env
        # with our spark mode and py4j location.
        spark_mode = os.environ.get("MASTER", "yarn-client")
        spark_home = Path(os.environ.get("SPARK_HOME", "/usr/lib/spark"))
        with utils.environment_edit_in_place('/etc/environment') as env:
            env['PYSPARK_DRIVER_PYTHON_OPTS'] = "notebook"
            env['PYSPARK_SUBMIT_ARGS'] = "--master " + spark_mode
            env['PYTHONPATH'] = spark_home / py4j_path

    def open_ports(self):
        for port in self.dist_config.exposed_ports('notebook'):
            hookenv.open_port(port)

    def start(self):
        self.stop()
        home = Path(os.environ.get('HOME', '/home/ubuntu'))
        script_path = home / 'start_notebook.sh'
        # TODO: check for executable script; error without it
        utils.run_as("ubuntu", script_path)

    def stop(self):
        home = Path(os.environ.get('HOME', '/home/ubuntu'))
        script_path = home / 'stop_notebook.sh'
        # TODO: check for executable script; error without it
        utils.run_as("ubuntu", script_path)

    def cleanup(self):
        ipython_profile = Path("/home/ubuntu/.ipython")
        ipython_profile.rmtree()
        with utils.environment_edit_in_place('/etc/environment') as env:
            env['PYSPARK_DRIVER_PYTHON_OPTS'] = ""
