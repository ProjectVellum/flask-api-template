#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

import flask_api_template as FAT


class FlaskBookshelfTests(unittest.TestCase):

    MOCK_CFG = os.path.dirname(os.path.abspath(__file__)) + '/mock.cfg'

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_server_init(self):
        cfg = {
            'TESTING' : True,
            'HOST' : '1.2.3.4',
            'PORT' : 1234
        }
        app = FAT.APIBaseline(cfg)

        self.assertTrue(isinstance(app.config, dict))
        self.assertTrue(app.config['TESTING'] == cfg['TESTING'])
        self.assertTrue(app.config['HOST'] == cfg['HOST'])
        self.assertTrue(app.config['PORT'] == cfg['PORT'])
        self.assertTrue('example/blueprint.py' in app.blueprints)


    def test_config_set(self):
        app = FAT.APIBaseline(self.MOCK_CFG, server_name='APITesting')

        self.assertTrue(app.config['TESTING'])
        self.assertTrue(app.config['PORT'] == 5555)

        cfg = {
            'HOST' : '1.2.3.4',
            'PORT' : 1234
        }

        app.SetConfig(cfg)
        self.assertTrue(app.config['HOST'] == cfg['HOST'])
        self.assertTrue(app.config['PORT'] == cfg['PORT'])

        cfg = {
            'TESTING' : False,
            'PORT' : 4321
        }

        app.SetConfig(cfg)
        self.assertTrue(app.config['TESTING'] == cfg['TESTING'])
        self.assertTrue(app.config['PORT'] == cfg['PORT'])


    def test_run(self):
        app = FAT.APIBaseline(self.MOCK_CFG, server_name='APITesting')


if __name__ == '__main__':
    unittest.main()
