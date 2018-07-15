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


class PostInfo(Resource):

    def post(self):
        if not request.headers.get('Qct'):
            error = 'Could not find Qct in request header!! Here are the headers found \n{}'.format(request.headers)
            LOGGER.critical(error)
            return {'status_code': 400, 'error': error}, 400

        else:
            if request.headers.get('Qct') not in ['ApiVersion1']:
                error = 'Could not find ApiVersion1 in Qct request header!! ' \
                        'Here are the headers found \n{}'.format(request.headers)
                LOGGER.critical(error)
                return {'status_code': 400, 'error': error}, 400


        print(json.dumps(request.json, sort_keys=True, indent=4))
        # print(request.data)
        a = ServerTemplateEngine()
        print(type(a))
        print(type(request.json))
        return {'status_code': 200, 'config': 'some_config'}, 200


def run_server(ip, port, base_api_uri, debug):
    LOGGER.debug('Starting server with the following ip: {}, '
                 'port: {}, base_api_uri: {}, server_debug: {}'.format(ip, port, base_api_uri, debug))
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PostInfo, '{base_api_uri}/postinfo'.format(base_api_uri=base_api_uri))
    app.run(port=int(port), host=ip, debug=debug)


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful