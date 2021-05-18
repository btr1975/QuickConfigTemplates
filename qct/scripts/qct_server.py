"""
QCT Server
"""
import logging
from flask import Flask, request
from flask_restful import Resource, Api
from .template_engine import ServerTemplateEngine


LOGGER = logging.getLogger('qct_server')

DIRECTORIES = None


class PostBasicBuild(Resource):
    """
    Class for a basic build this receives full yaml and operates on the
    template in data.template
    """
    def post(self):  # pylint: disable=no-self-use
        """Method to receive a POST"""
        if not request.headers.get('Qct'):  # pylint: disable=no-else-return
            error = 'Could not find Qct in request header!! Here are the headers found \n{}'.format(request.headers)
            LOGGER.critical('PostBasicBuild: %s', error)
            return {'status_code': 400, 'error': error}, 400

        else:
            if request.headers.get('Qct') not in ['ApiVersion1']:
                error = 'Could not find ApiVersion1 in Qct request header!! ' \
                        'Here are the headers found \n{}'.format(request.headers)
                LOGGER.critical('PostBasicBuild: %s', error)
                return {'status_code': 400, 'error': error}, 400

        template_engine_obj = ServerTemplateEngine(directories=DIRECTORIES, config=request.json)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            message = 'From: {} Received Data: {}'.format(request.remote_addr, request.json)
            print(message)
            LOGGER.debug('PostBasicBuild: %s', message)

        return template_engine_obj.run_template_version()


class PostRemoteYamlBuild(Resource):
    """
    Class for a remote yaml build this receives vars, and a yaml template to build
    """
    def post(self):  # pylint: disable=no-self-use
        """Method to receive a POST"""
        if not request.headers.get('Qct'):  # pylint: disable=no-else-return
            error = 'Could not find Qct in request header!! Here are the headers found \n{}'.format(request.headers)
            LOGGER.critical('PostRemoteYamlBuild: %s', error)
            return {'status_code': 400, 'error': error}, 400

        else:
            if request.headers.get('Qct') not in ['ApiVersion1']:
                error = 'Could not find ApiVersion1 in Qct request header!! ' \
                        'Here are the headers found \n{}'.format(request.headers)
                LOGGER.critical('PostRemoteYamlBuild: %s', error)
                return {'status_code': 400, 'error': error}, 400

        template_engine_obj = ServerTemplateEngine(directories=DIRECTORIES, config=request.json)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            message = 'From: {} Received Data: {}'.format(request.remote_addr, request.json)
            print(message)
            LOGGER.debug('PostRemoteYamlBuild: %s', message)

        return template_engine_obj.get_remote_yaml_template()


def run_local_server(ip_addr, port, base_api_uri, debug, directories):
    """
    Function to run the local flask server
    :param ip_addr: The IP address to listen on
    :param port: The port to listen on
    :param base_api_uri: The base uri, for the server
    :param debug: True to turn on debug
    :param directories: A Directories object
    :return:
        None

    """
    if debug:
        LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug('Starting server with the following ip: %s, '
                 'port: %s, base_api_uri: %s, server_debug: %s', ip_addr, port, base_api_uri, debug)
    # TODO: Need to check on this global usage
    global DIRECTORIES  # pylint: disable=global-statement
    DIRECTORIES = directories
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PostBasicBuild, '{base_api_uri}/basic_build'.format(base_api_uri=base_api_uri))
    api.add_resource(PostRemoteYamlBuild, '{base_api_uri}/remote_yaml_build'.format(base_api_uri=base_api_uri))
    app.run(port=int(port), host=ip_addr, debug=debug)


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
