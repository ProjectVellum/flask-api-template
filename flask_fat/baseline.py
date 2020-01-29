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
import logging
import logging.config
import yaml
from pdb import set_trace

#pip install -U flask-cors (module is in current dir)
# import addons.flask_cors as flask_cors
import flask_cors
from .config_builder import ConfigBuilder

class APIBaseline:

    def __init__(self, name, **kwargs):
        """
        @param name: name for the running server and its PID.
        @param **kwargs:
            @key bp_path: path to a blueprints/ folder. default=./blueprints/
            @key verbose: <bool> make it talk (or not).
            @key ignore: list of blueprint names to be ignored during init.
            @key config: Flask config properties.
            @key loggin_cfg: path to yaml or a dict obj that logging understands.
        """
        # When inheriting APIBaseline, user must provide a unique name for the
        # application. This name will be used for finding ~/.config/NAME cfg file.
        self.kwargs = kwargs
        self.name = name
        self._setup_logging(kwargs.get('logging_cfg', None))

        bp_path = kwargs.get('bp_path', None)

        # Getting the right pass to the config file for this server.
        self.config_builder = ConfigBuilder(self.name, self.__file__)
        cfg = kwargs.get('cfg', None)
        if cfg is None:
            cfg = self.config_builder.priority_cfg_path

        if cfg is None:
            err_msg = 'Couldn\'t find config file at any of the following locations: %s'
            err_msg = err_msg % self.config_builder.cfg_priority_order
            self.logging.error(err_msg, exc_info=True)
            raise RuntimeError(err_msg)

        self.logging.critical('Config file used: %s' % cfg)

        if bp_path is None:
            bp_path = 'blueprints/'

        self.bp_path = bp_path.rstrip('/')
        # self.path = self.root_dir + '/' + self.path

        # all registered blueprints path relative to blueprints dir path:
        # (e.g. example/blueprint.py)
        self.blueprints = []
        self.verbose = kwargs.get('verbose', True)

        self.app = flask.Flask(kwargs.get('server_name', self.name),
                                static_folder='static',
                                static_url_path='/static')

        flask_cors.CORS(self.app, supports_credentials=True) # to allow authentication
        self.app.url_map.strict_slashes = False

        self.SetConfig(cfg)
        self.RegisterBlueprints(self.bp_path, kwargs.get('ignore', None))


    # TODO: ignore_bp arg parser!
    def RegisterBlueprints(self, bp_path, ignore_bp=None):
        """ Add all blueprint scripts found in the blueprints/ folder (by default)
        or set in constructor through bp_path param.
        """
        ignore_bp = ignore_bp if ignore_bp is not None else []
        ignore_bp.append('__pycache__')

        # list of all blueprints scripts (not imported as module yet)
        bp_list = []
        things_in_bp_dir = glob.glob(bp_path + '/*')
        for path in things_in_bp_dir:
            if path.endswith('__pycache__'):
                continue
            if not path.endswith('.py'):
                path = os.path.join(path, 'blueprint.py')

            bp_list.extend([path for path in glob.glob(path)])
            # bp_list.extend([path for path in glob.glob(path + '/*.bp') ])

        #get rid of .py and .bp extension in the path name to make it importable
        #bp_list = [path.rstrip('.py') for path in bp_list]
        for bp in bp_list:
            module_name = bp.replace('/', '.')
            bp_name = module_name.split('.')[-3]
            if(bp_name in ignore_bp):
                if self.verbose:
                    logging.info('!! Ignoring to load blueprint "%s" !!' % bp_name)
                continue

            try:
                imported_bp = SourceFileLoader(module_name, bp).load_module()
                imported_bp.Journal.register(self)
            except Exception as err:
                msg = 'Something went wrong while importing blueprints...:' + \
                      '\n --> [ %s ]' % err

                if self.config.get('PEDANTIC_INIT', True):
                    logging.error(msg)
                    raise RuntimeError(msg)
                else:
                    logging.warning('[PEDANTIC_INIT is off]: \n %s' % msg)
                continue

            imported_bp.Journal.on_post_register()
            self.app.register_blueprint(imported_bp.Journal.BP)
            self.blueprints.append(bp.split(bp_path)[1].lstrip('/'))

            if self.verbose:
                logging.info('-> Regestring bluerpint "%s"...' % imported_bp.Journal.name)

        if self.verbose:
            logging.info('-> RestAPI reporting for duty.')


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
            err_msg = 'Error while running! [ %s : %s ]' % (type(error), error)
            self.logging.error(err_msg, exc_info=True)


    def _setup_logging(self, cfg):
        """
         Sets the config obj of the logging from the yaml path or a dict obj.
        If no cfg was parsed - no config will be set and default logging will be
        used.
        """
        if not isinstance(cfg, dict):
            cfg = self._read_logging_yaml(cfg)
        if cfg is not None:
            logging.config.dictConfig(cfg)


    def _read_logging_yaml(self, path):
        """
            Opens the yaml filr at the path and parse it into a dictionary.

        @param path: a string path to a yaml or None to use a default path at
                    at this_file_dir_/logging.yaml is used.
        @return: a dict object of parsed yaml file.
        """
        if path is None:
            path = os.path.dirname(__file__)
            path = os.path.join(path, 'logging.yaml')

        if not os.path.exists(path):
            return {}

        with open(path, 'r') as file_obj:
            config = yaml.safe_load(file_obj)
        return config


    @property
    def pid_file(self):
        return '/var/run/%s.pid' % self.server_name

    @property
    def config(self):
        """ Returns the flask's app config file which also contains the values of
        the passed cfg file into the constructor on object instantiation.
        """
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


    @property
    def logging(self):
        """
            Returns a logger set by the logging.yaml config file with hardcoded
        logger name "FlaskFatLog". It will also set verbosity levels of the stdout
        logger handlers based of the "verbosity" argument set in constructor.

        If you want a different logger name, override this property and do
        whatever with it.
        """
        verbosity = self.kwargs.get('verbosity', 3) #default is Warning level
        log_level = verbosity * 10
        if log_level >= 0:
            log_level = 60 - log_level
            log_level = 0 if log_level < 0 else log_level

        for log in logging.root.handlers:
            if not isinstance(log, logging.handlers.RotatingFileHandler):
                log.setLevel(log_level)
        return logging.getLogger('FlaskFatLog')


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
