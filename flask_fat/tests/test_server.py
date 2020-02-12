#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

import flask_fat


class FatServer(unittest.TestCase):

    MOCK_CFG = os.path.dirname(os.path.abspath(__file__)) + '/mock/mock.conf'
    APP_NAME = 'flask_fat_test_server'
    BP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/mock/bp/'

    def test_server_init(self):
        cfg = {
            'TESTING' : True,
            'HOST' : '1.2.3.4',
            'PORT' : 1234
        }
        app = flask_fat.APIBaseline(self.APP_NAME, cfg=cfg, bp_path=self.BP_PATH)

        self.assertTrue(isinstance(app.config, dict))
        self.assertTrue(app.config['TESTING'] == cfg['TESTING'])
        self.assertTrue(app.config['HOST'] == cfg['HOST'])
        self.assertTrue(app.config['PORT'] == cfg['PORT'])


    def test_config_set(self):
        app = flask_fat.APIBaseline(self.APP_NAME, cfg=self.MOCK_CFG, bp_path=self.BP_PATH)

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


if __name__ == '__main__':
    unittest.main()
