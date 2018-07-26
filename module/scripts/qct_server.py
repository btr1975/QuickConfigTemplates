from flask import Flask, request
from flask_restful import Resource, Api
import logging
import json
from .template_engine import ServerTemplateEngine
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'dev'
__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger('qct_server')

DIRECTORIES = None


class PostBasicBuild(Resource):
    """
    Class for a basic build this receives full yaml and operates on the
    template in data.template
    """
    def post(self):
        if not request.headers.get('Qct'):
            error = 'Could not find Qct in request header!! Here are the headers found \n{}'.format(request.headers)
            LOGGER.critical('PostBasicBuild: {}'.format(error))
            return {'status_code': 400, 'error': error}, 400

        else:
            if request.headers.get('Qct') not in ['ApiVersion1']:
                error = 'Could not find ApiVersion1 in Qct request header!! ' \
                        'Here are the headers found \n{}'.format(request.headers)
                LOGGER.critical('PostBasicBuild: {}'.format(error))
                return {'status_code': 400, 'error': error}, 400

        template_engine_obj = ServerTemplateEngine(directories=DIRECTORIES, config=request.json)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            message = 'From: {} Received Data: {}'.format(request.remote_addr, request.json)
            print(message)
            LOGGER.debug('PostBasicBuild: {}'.format(message))

        return template_engine_obj.run_template_version()


class PostRemoteYamlBuild(Resource):
    """
    Class for a remote yaml build this receives vars, and a yaml template to build
    """
    def post(self):
        if not request.headers.get('Qct'):
            error = 'Could not find Qct in request header!! Here are the headers found \n{}'.format(request.headers)
            LOGGER.critical('PostRemoteYamlBuild: {}'.format(error))
            return {'status_code': 400, 'error': error}, 400

        else:
            if request.headers.get('Qct') not in ['ApiVersion1']:
                error = 'Could not find ApiVersion1 in Qct request header!! ' \
                        'Here are the headers found \n{}'.format(request.headers)
                LOGGER.critical('PostRemoteYamlBuild: {}'.format(error))
                return {'status_code': 400, 'error': error}, 400

        template_engine_obj = ServerTemplateEngine(directories=DIRECTORIES, config=request.json)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            message = 'From: {} Received Data: {}'.format(request.remote_addr, request.json)
            print(message)
            LOGGER.debug('PostRemoteYamlBuild: {}'.format(message))

        return template_engine_obj.get_remote_yaml_template()


def run_server(ip, port, base_api_uri, debug, directories):
    if debug:
        LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug('Starting server with the following ip: {}, '
                 'port: {}, base_api_uri: {}, server_debug: {}'.format(ip, port, base_api_uri, debug))
    global DIRECTORIES
    DIRECTORIES = directories
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PostBasicBuild, '{base_api_uri}/basic_build'.format(base_api_uri=base_api_uri))
    api.add_resource(PostRemoteYamlBuild, '{base_api_uri}/remote_yaml_build'.format(base_api_uri=base_api_uri))
    app.run(port=int(port), host=ip, debug=debug)


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful