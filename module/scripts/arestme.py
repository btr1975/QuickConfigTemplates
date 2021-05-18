"""
REST API Interface
"""
import json
import requests


class ARestMe:
    """This class is used for a REST API
    """
    def __init__(self):
        self.username = None
        self.password = None
        self.auth_token = None
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json'}
        self.server_url = 'http://127.0.0.1:5000/'
        self.proxy = '127.0.0.1:8080'

    def __str__(self):
        return '<ARestMe>'

    def __get_data(self, api_url, post_data=None, put_data=None, params=None):
        """
        Method to retrieve data
        :param api_url: The API uri
        :param post_data: The dictionary for a request if required = post
        :param put_data: The dictionary for a request if required = put
        :param params: Any parameters needed for a get request
        :return:
            Dict of data
        """
        full_url = '{server_url}{api_url}'.format(server_url=self.server_url, api_url=api_url)

        if post_data:  # pylint: disable=no-else-return
            return requests.post(full_url, data=json.dumps(post_data), headers=self.headers).json()

        elif put_data:
            return requests.put(full_url, data=json.dumps(put_data), headers=self.headers).json()

        elif params:
            return requests.get(full_url, params=params, headers=self.headers).json()

        else:
            return requests.get(full_url, headers=self.headers).json()

    def get_headers(self):
        """
        Method to get the headers
        :return:
            Dict of headers
        """
        return self.headers

    def set_update_headers(self, key, value):
        """
        Method to set or update a header
        :param key: The header key
        :param value: The header value
        :return:
            None
        """
        self.headers.update({key: value})

    def set_user_and_pass(self, username, password):
        """
        Method to set the username and password
        :param username: The username
        :param password: The password
        :return:
            None
        """
        self.username = username
        self.password = password

    def set_auth_token(self, auth_token):
        """
        Method to set the authorization token
        :param auth_token: The token
        :return:
            None
        """
        self.auth_token = auth_token

    def set_proxy(self, protocol, proxy_ip, proxy_port):
        """
        Method to set the proxy information
        :param protocol: The protocol http or https
        :param proxy_ip: The proxy host
        :param proxy_port: The proxy port
        :return:
            None
        """
        if protocol in ('http', 'https'):
            self.proxy = "{prot}://{host}:{port}".format(prot=protocol, host=proxy_ip, port=proxy_port)

        else:
            raise Exception('{} not supported as a proxy protocol use http, or https!'.format(protocol))

    def set_server_and_port(self, protocol, server_ip, server_port=None):
        """
        Method to set the server information
        :param protocol: The protocol http or https
        :param server_ip: The server host
        :param server_port: The server port (optional)
        :return:
            None
        """
        if protocol in ('http', 'https'):
            if server_port:
                self.server_url = "{prot}://{host}:{port}/".format(prot=protocol, host=server_ip, port=server_port)

            else:
                self.server_url = "{prot}://{host}/".format(prot=protocol, host=server_ip)

        else:
            raise Exception('{} not supported as a server protocol use http, or https!'.format(protocol))

    def send_get(self, api, params=None):
        """
        Method to send a get request
        :param api: API URI
        :param params: Any Parameters to send
        :return:
            JSON
        """
        if params:
            if not isinstance(params, dict):
                raise TypeError('params argument must be a dictionary if supplied.')
        return self.__get_data(api, params=params)

    def send_post(self, api, data):
        """
        Method to send a post request
        :param api: API URI
        :param data: Any Data you want to send
        :return:
            JSON
        """
        if not isinstance(data, dict):  # pylint: disable=no-else-raise
            raise TypeError('data argument must be a dictionary if supplied.')

        elif len(data) == 0:
            raise Exception('data argument can not be empty.')

        return self.__get_data(api, post_data=data)

    def send_put(self, api, data):
        """
        Method to send a put request
        :param api: API URI
        :param data: Any Data you want to send
        :return:
            JSON
        """
        if not isinstance(data, dict):  # pylint: disable=no-else-raise
            raise TypeError('data argument must be a dictionary if supplied.')

        elif len(data) == 0:
            raise Exception('data argument can not be empty.')

        return self.__get_data(api, put_data=data)

    @staticmethod
    def print_pretty_json(json_data):
        """
        Method to print response JSON real pretty like
        :param json_data: JSON Data
        :return:
            None
        """
        print(json.dumps(json_data, sort_keys=True, indent=4))
