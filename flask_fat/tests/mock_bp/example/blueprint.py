#!/usr/bin/python3
"""
    Blueprint to provide information about the api, options and etc.
"""
__author__ = "Zakhar Volchak"
__copyright__ = "Copyright 2018 Hewlett Packard Enterprise Development LP"
__maintainer__ = "Zakhar Volchak"
__email__ = "zakhar.volchak@hpe.com"

import os
import flask
from pdb import set_trace

import flask_fat

Journal = self = flask_fat.Journal(__file__)


""" ----------------- ROUTES ----------------- """

@Journal.BP.before_request
def validate_request(*args, **kwargs):
    return Journal.validate_request(flask.request)


@Journal.BP.after_request
def salt_the_response(response):
    return Journal.after_request(response)


@Journal.BP.route('/', methods=['GET'])
@Journal.BP.route('/example', methods=['GET'])
def example_api():
    if Journal.requestor_wants_json(flask.request.headers):
        return flask.make_response(flask.jsonify({
            "this_is_an_example_key" : "example_value_here"
        }), 200)

    return flask.make_response(flask.jsonify({
        "this_is_key_in_html_request" : "example_value_here_as_html_response"
    }), 200)
