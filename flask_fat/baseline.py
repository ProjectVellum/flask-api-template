#!/usr/bin/python3
"""
    TODO: docs.

    Inherite from APIBaseline. RegisterBlueprints() is called from constructor.
    BP pass assumed at blueprints/ by default.
"""
__author__ = "Zakhar Volchak"
__copyright__ = "Copyright 2018 Hewlett Packard Enterprise Development LP"
__maintainer__ = "Zakhar Volchak"
__email__ = "zakhar.volchak@hpe.com"

import argparse
import flask
from importlib.machinery import SourceFileLoader
import glob
import os
import sys
import time
from pdb import set_trace

#pip install -U flask-cors (module is in current dir)
# import addons.flask_cors as flask_cors
import flask_cors


class APIBaseline:

    def __init__(self, cfg, **kwargs):
        """
        @param **kwargs:
            @key server_name: name for the running server and its PID.
            @key bp_path: path to a blueprints/ folder. default=./blueprints/
            @key verbose: <bool> make it talk (or not).
            @key ignore: list of blueprint names to be ignored during init.
            @key config: Flask config properties.
        """
        bp_path = kwargs.get('bp_path', None)
        if bp_path is None:
            bp_path = 'blueprints/'

        # trip trailing slash from path
        self.path = bp_path.rstrip('/') if bp_path.endswith('/') else bp_path
        self.path = self.root_dir + '/' + self.path

        #all registered blueprints path relative to blueprints dir path:
        #(e.g. example/blueprint.py)
        self.blueprints = []
        self.verbose = kwargs.get('verbose', True)
        self.server_name = kwargs.get('server_name', 'CustomAPIServer')

        self.app = flask.Flask(kwargs.get('server_name', self.server_name),
                                static_folder='static',
                                static_url_path='/static')

        flask_cors.CORS(self.app, supports_credentials=True) # to allow authentication
        self.app.url_map.strict_slashes = False

        self.SetConfig(cfg)
        self.RegisterBlueprints(kwargs.get('ignore', None))


    # TODO: ignore_bp arg parser!
    def RegisterBlueprints(self, ignore_bp=None):
        """ Add all blueprint scripts found in the blueprints/ folder to the
        flask routine. """
        ignore_bp = ignore_bp if ignore_bp is not None else []
        ignore_bp.append('__pycache__')

        # list of all blueprints scripts (not imported as module yet)
        bp_list = []
        things_in_bp_dir = glob.glob(self.path + '/*')
        for bp_path in things_in_bp_dir:
            if bp_path.endswith('__pycache__'):
                continue
            bp_list.extend([path for path in glob.glob(bp_path + '/*.bp') ])
            bp_list.extend([path for path in glob.glob(bp_path + '/blueprint.py') ])
        #get rid of .py and .bp extension in the path name to make it importable
        #bp_list = [path.rstrip('.py') for path in bp_list]
        for bp in bp_list:
            module_name = bp.replace('/', '.')
            bp_name = module_name.split('.')[-3]
            if(bp_name in ignore_bp):
                if self.verbose:
                    print('!! Ignoring to load blueprint "%s" !!' % bp_name)
                continue

            try:
                imported_bp = SourceFileLoader(module_name, bp).load_module()
                imported_bp.Journal.register(self)
            except Exception as err:
                msg = 'Something went wrong while importing blueprints...:' + \
                      '\n --> [ %s ]' % err

                if self.config.get('PEDANTIC_INIT', True):
                    raise RuntimeError(msg)
                else:
                    print(' --- WARNING ----\n %s' % msg)
                    print(' ----------------')
                continue

            imported_bp.Journal.on_post_register()
            self.app.register_blueprint(imported_bp.Journal.BP)
            self.blueprints.append(bp.split(self.path)[1].lstrip('/'))

            if self.verbose:
                print('-> Regestring bluerpint "%s"...' % imported_bp.Journal.name)

        if self.verbose:
            print('-> RestAPI reporting for duty.')


    def SetConfig(self, path_or_dict, override=False):
        """ Update current Flask config values with new props.
        @param path_or_dict: can be path to a config file or a dict of values.
        @param override: <default=False> whether to use .update() function when
                    override=False or a strict assignment (curr_cfg = new_cfg).
        """
        config_dict = {}
        if isinstance(path_or_dict, str):
            path = os.path.abspath(path_or_dict)
            flask_obj = flask.Flask(time.ctime())   # dummy name
            flask_obj.config.from_pyfile(path_or_dict)
            config_dict.update(flask_obj.config)
        elif isinstance(path_or_dict, dict):
            config_dict.update(path_or_dict)

        if not override:
            self.app.config.update(config_dict)
        else:
            self.app.config = config_dict


    def run(self, cfg=None):
        """ Run Flask application. """
        if cfg is not None:
            self.SetConfig(cfg)

        try:
            self.app.run(host=self.config['HOST'],
                            port=self.config['PORT'],
                            debug=self.config['DEBUG'])
        except Exception as error:
            print('Error while running! [ %s : %s ]' % (type(error), error))


    @property
    def pid_file(self):
        return '/var/run/%s.pid' % self.server_name

    @property
    def config(self):
        return self.app.config

    @property
    def root_dir(self):
        """ Absolute path/location of this (web_server.py) file """
        return os.path.dirname(os.path.abspath(self.__file__)) + '/'

    @property
    def static_dir(self):
        return os.path.abspath(os.path.dirname(self.__file__) + "/static/")

    @property
    def templates_dir(self):
        return os.path.abspath(os.path.dirname(self.__file__) + "/templates/")

    @property
    def __file__(self):
        """ When inherited, __file__ returns path to This file, not the one that
        is actually calling. Thus, this function will return a path to an actual
        inherited file.
         """
        real_file = sys.modules[self.__class__.__module__].__file__
        return os.path.abspath(real_file)

    @property
    def test_client(self):
        return self.app.test_client


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore',
                        help='blueprints to be ignored/not-loaded by server. ' +\
                            '--ignore "bp1,bp2,bp2"', default=None)

    parsed = parser.parse_args()
    if parsed.ignore is not None:
        parsed.ignore = parsed.ignore.replace(' ', '').split(',')
    return vars(parsed)


def main(args=None):
    args = {} if args is None else args
    cmd = parse_cmd()
    args.update(cmd)

    mainapp = APIBaseline('./server.cfg', **args)
    if not args.get('dont_run', False):
        mainapp.run()
    return mainapp


if __name__ == '__main__':
    main()
