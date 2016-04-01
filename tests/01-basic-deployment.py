#!/usr/bin/env python3

import unittest
import amulet


class TestDeploy(unittest.TestCase):
    """
    Trivial deployment test for Apache Spark Notebook.

    This charm cannot do anything useful by itself, so integration testing
    is done in the bundle.
    """

    def test_deploy(self):
        self.d = amulet.Deployment(series='trusty')
        self.d.load({
            'services': {
                'spark': {'charm': 'apache-spark'},
                'notebook': {'charm': 'apache-spark-notebook'},
            },
            'relations': [('spark', 'notebook')],
        })
        self.d.setup(timeout=900)
        self.d.sentry.wait(timeout=1800)
        self.unit = self.d.sentry['notebook'][0]


if __name__ == '__main__':
    unittest.main()
