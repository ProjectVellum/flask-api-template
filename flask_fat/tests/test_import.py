#!/usr/bin/python3
import unittest
import os
import sys
from pdb import set_trace


class TestImports(unittest.TestCase):

    def test_import_all(self):
        try:
            import flask_fat
            flask_fat.baseline
            flask_fat.blueprints
            flask_fat.Journal
            flask_fat.APIBaseline
            self.assertTrue(True)
        except Exception as err:
            self.assertTrue(False, err)

if __name__ == '__main__':
    unittest.main()
