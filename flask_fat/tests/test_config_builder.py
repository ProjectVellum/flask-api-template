#!/usr/bin/python3
import unittest
import os
import getpass
import sys
from pdb import set_trace

import flask_fat


class TestConfigBuilder(unittest.TestCase):

    HOME_DIR = '/home/%s' % getpass.getuser()
    APP_NAME = 'fat_tests'
    FAT_DIR = os.path.dirname(os.path.realpath(flask_fat.__file__))

    def test_import(self):
        try:
            from flask_fat import ConfigBuilder
            self.assertTrue(True)
        except Exception as err:
            self.assertTrue(False, err)


    def test_paths(self):
        from flask_fat import ConfigBuilder

        target_cfg_name = '%s.conf' % self.APP_NAME
        cfg = ConfigBuilder(self.APP_NAME,
                            self.FAT_DIR)

        home_dir = os.path.join(self.HOME_DIR, '.config', target_cfg_name)
        self.assertEqual(cfg.user_path, home_dir)
        self.assertEqual(cfg.global_path, '/etc/%s.conf' % self.APP_NAME)
        self.assertEqual(cfg.inproject_path, os.path.join(self.FAT_DIR, 'server.conf'))
        self.assertEqual(cfg.inproject_name_path, os.path.join(self.FAT_DIR, target_cfg_name))


    def test_priority(self):
        from flask_fat import ConfigBuilder
        fat_path = flask_fat.__file__

        cfg = ConfigBuilder(self.APP_NAME,
                            fat_path)

        expected = os.path.join(self.FAT_DIR, 'server.conf')
        self.assertEqual(cfg.priority_path, expected)


    def test_custom_path(self):
        from flask_fat import ConfigBuilder
        this_file = os.path.realpath(__file__)
        mock_cfg = os.path.dirname(this_file)
        mock_cfg = os.path.join(mock_cfg, 'mock/mock.conf')

        cfg = ConfigBuilder(self.APP_NAME, 'nothing', path=mock_cfg)

        self.assertEqual(cfg.priority_path, mock_cfg)


if __name__ == '__main__':
    unittest.main()
