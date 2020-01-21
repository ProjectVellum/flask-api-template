#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

import flask_fat


class FlaskBookshelfTests(unittest.TestCase):

    MOCK_CFG = os.path.dirname(os.path.abspath(__file__)) + '/mock.cfg'

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(cls):
        app = flask_fat.APIBaseline('flask_fat_test', cfg=cls.MOCK_CFG)
        cls.app = app.app.test_client()
        cls.headers = {
            'Accept' : 'version=0.1',
            'content-type' : 'application/json'
        }


    def tearDown(self):
        pass


    def test_root_endpoint(self):
        """ This should validate '/' endpoint with all the validation steps, e.g
            before_request, after_request, version validation and etc.
        """
        response = self.app.get('/', headers=self.headers)

        self.assertTrue(response.status_code == 200)

        #error code without version in headers
        response = self.app.get('/')
        self.assertTrue(response.status_code >= 400)

        #version in headers, but no json. Response should be success.
        response = self.app.get('/', headers={ 'Accept' : self.headers['Accept']})
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()
