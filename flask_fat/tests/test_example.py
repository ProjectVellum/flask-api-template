#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

import flask_fat


class FlaskBookshelfTests(unittest.TestCase):

    APP_NAME = 'flask_fat_test_example'
    MOCK_CFG = os.path.dirname(os.path.abspath(__file__)) + '/mock.cfg'
    BP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/mock_bp/'


    @classmethod
    def setUpClass(cls):
        cls.headers = {
            'Accept' : 'version=0.1',
            'content-type' : 'application/json'
        }


    @classmethod
    def tearDownClass(cls):
        pass


    def test_init_blueprints(self):
        app = flask_fat.APIBaseline(self.APP_NAME, cfg=self.MOCK_CFG, bp_path=self.BP_PATH)

        # check all the blueprints in the mock blueprint directory where loaded
        # into the flask_fat api.
        self.assertTrue('example/blueprint.py' in app.blueprints)
        self.assertTrue('example_parent.py' in app.blueprints)


    def test_root_endpoint(self):
        """ This should validate '/' endpoint with all the validation steps, e.g
            before_request, after_request, version validation and etc.
        """
        app = flask_fat.APIBaseline(self.APP_NAME, cfg=self.MOCK_CFG, bp_path=self.BP_PATH)
        app = app.app.test_client()

        response = app.get('/', headers=self.headers)

        self.assertTrue(response.status_code == 200)

        #error code without version in headers
        response = app.get('/')
        self.assertTrue(response.status_code >= 400)

        #version in headers, but no json. Response should be success.
        response = app.get('/', headers={ 'Accept' : self.headers['Accept']})
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()
