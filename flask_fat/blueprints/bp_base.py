#!/usr/bin/python3
"""
    Base class to be used\inherited by all the blueprints that lives in this
directory space. The main reason for this "base" is to incapsulate the steps
taken by all the blueprints to regester it with Flask. Also, adds some other
usefull functions that will be used in most blueprints "as-is" or with slight
modifications, such as make_request(), handle_bad_response(), requestor_wants_json(),
validate_request(), validate_version...
"""
__author__ = "Zakhar Volchak"
__copyright__ = "Copyright 2018 Hewlett Packard Enterprise Development LP"
__maintainer__ = "Zakhar Volchak"
__email__ = "zakhar.volchak@hpe.com"

from collections import namedtuple
import os
import re   #used to extract version=N; from header
import requests
import json
from flask import Blueprint, make_response, jsonify
from pdb import set_trace


class Journal():
    """
        A Journal in this context is a class that contains Flask Blueprints and
    Routes. Couldn't come up with better alternative the the word "blueprint"
    and using the same word as Flask's class Blueprint is "context confusing".
    """

    def __init__(self, name, **args):
        """
            @param name: pass __file__ to assign blueprint's dirname as Journal
                        name, or pass non empty string to set a custom name.
            @param url_prefix: <str> path to us before the actual route defined one,
                                e.g. http://localhost:1111/<url_prefix>/ROUTE_PATH
            @args mainapp: a Flask server that is using this jouranl/blueprint.
        """
        self.json_model = {}
        self.mainapp = args.get('mainapp', None)

        self.name = os.path.dirname(name).split('/')[-1]
        if not self.name:
            self.name = name

        named_tuple_keys = 'json response status_code reason'
        self.last_response = namedtuple('CustomResponse', named_tuple_keys)
        self.last_response.__new__.__defaults__ = (None,) * \
                                                len(self.last_response._fields)

        self.BP = Blueprint(self.name, __name__,
                            url_prefix=args.get('url_prefix', ''),
                            static_url_path='/static/')


    def register(self, mainapp, name=None):
        """ Save reference to Flask server in this journel. """
        self.mainapp = mainapp


    def make_request(self, url, custom_headers=None, timeout_cfg=None):
        ''' A simple wrapper around requests.get() function to help catch errors
        that are occuring during the request. It will use Headers defined in the
        server.cfg file by default, but can be modded by the caller.
         @param <str> url: endpoint to make a 'get' request to.
         @param <dict> custom_headers: any additional headers to be used for this
                call. Passing existed in the config file keys will override it.
         @return <namedtuple>: object with json, status_code fields taken from
                            <Response> object returned by requests.get() which
                            is also saved into 'resposnse' field.
        '''
        response = None
        error = None
        all_headers={}
        all_headers.update(self.mainapp.config['HTTP_HEADERS'])
        #add/update headers passed by caller
        if custom_headers is not None:
            all_headers.update(custom_headers)

        try:
            #API call to the URL
            if timeout_cfg is None:
                timeout_cfg = self.mainapp.config['TIMEOUT']
            response = requests.get(url, headers=all_headers, timeout=timeout_cfg)
            error = None
        except requests.exceptions.RequestException as e:
            #if you get here, result obj is not set. Thus, make it empy Response
            #so that it can be handled properly further down the code.
            response = requests.Response()
            response.status_code = 500
            response.reason = 'Failed to get response from %s' % url
            response._content = b'{}'

        response = self.handle_bad_response(response)

        return response


    def handle_bad_response(self, response):
        ''' Check status code of the response to parse it with the same pattern
        of actions during each http request. When status code is not in 200s
        range - make_response() object will be created with the self.json_model
        default or spoofed(when enabled in the server.cfg) values.

        @param <Response> response: returned object from request.get() call.
        @return: make_response() object when status is not good. None - otherwise.
        '''
        resp_json = {} # json data that will be returned
        if response.status_code == requests.codes.ok:
            return response

        if self.mainapp.config['ALLOW_SPOOF']:
            response.status_code = 303 #partial content - because spoofed.
            resp_json = self.spoofed
        else:
            response.status_code = response.status_code
            resp_json = self.json_model

        response._content = str.encode(json.dumps(resp_json))
        return response


    @property
    def spoofed(self):
        """ Return some data (random?) when the expected API does not respond.
        This is usefull when you need to "recover" and show at least some data
        to present.
        Note: this must be overwritten by the child class.
        """
        raise NotImplemented("You have you overwrite this property!")


    ''' --- Request handles. Validation and Response makers.... --- '''

    def requestor_wants_json(self, headers):
        """ Check if 'application/json' is in the requestor header. Return
        True if so. Also, catching ANY exception on getting request.headers will
        return True.

            @param headers: dict of headers passed in the requested header.
        """
        try:
            return 'application/json' in headers['Accept'] or \
                    'application/json' in headers['Content-type']
        except Exception:
            return True


    def validate_request(self, request):
        """ Take all the steps needed to validate the Request from the client,
        e.g. "Accept" in the headers.
        This function is called at Flask's ".before_request" stage.
        """
        # This function expected to grow a bit. Could be validating more than
        # just the version.
        if request.headers.get('Accept', None) is None:
            return self.make_error_response('No [Accept] header found!')
        is_valid_version = self.validate_version(request.headers)
        return is_valid_version


    def validate_version(self, headers):
        """ Validate requestor version passed in the header matches this API
        serving version. """
        if not self.requestor_wants_json(headers):  # Ignore versioning for HTML
            return None
        if not self.mainapp.config.get('VERSION_CHECK', True):
            return None

        hdr_accept = headers.get('Accept', '')
        version = re.search('version=(.+)', hdr_accept)

        if version is None:
            return self.make_error_response('No version sent')

         # group(0) returns 'version=1.0'. group(1) is just '1.0'
        version = float(version.group(1).strip(';'))
        expected = self.mainapp.config['VERSION']
        if version != expected:
            return self.make_error_response('Bad version: %s != %s' % \
                                            (version, expected))
        return None #Success


    def after_request(self, response):
        response.headers['Content-Type'] += ';charset=utf-8'
        response.headers['Content-Type'] += ';version=%s' % self.mainapp.config['VERSION']
        return response


    def make_error_response(self, error_msg, code=400):
        return make_response(jsonify({ 'error' : error_msg}), code)


    def on_post_register(self):
        pass