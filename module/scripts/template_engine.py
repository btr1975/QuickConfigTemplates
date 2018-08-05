import logging
import sys
from jinja2 import Environment, select_autoescape, FileSystemLoader
from jinja2 import exceptions as j2_exceptions
import yaml
import json
import persistentdatatools as pdt
import os
import re
from .arestme import ARestMe
from ..utils import custom_filters
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018 Ben Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'prod'
__version_info__ = (2, 0, 6, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)
TEMPLATE_LOGGER = logging.getLogger('qct_template')
SERVER_LOGGER = logging.getLogger('qct_server')


class TemplateEngine(object):
    """
    Class to render, and clean Jinja2 templates from the client side
    """
    custom_filters = custom_filters

    def __init__(self, directories=None, yml_file_name=None, output_file_name=None, display_only=False,
                 display_json=False, display_yml=False, package_name=None, variables_file_name=None, auto_build=None,
                 remote_build=False, begin_string=None, include_string=None):
        self.directories = directories
        if auto_build:
            yml_file_name = self.__auto_build_template(variables_file_name)
        self.yml_data = self.__pre_run_yml_input_file(yml_file_name, variables_file_name)
        self.yml_file_name = yml_file_name
        self.output_file_name = output_file_name
        self.display_only = display_only
        self.display_json = display_json
        self.display_yml = display_yml
        self.package_name = package_name
        self.template_version = None
        self.begin_string = begin_string
        self.include_string = include_string
        if not remote_build:
            self.version_runner()
        else:
            self.server_rest()

    def version_runner(self):
        try:
            config = yaml.safe_load(self.yml_data)

        except Exception as e:
            error = 'Error retrieving yml yaml.safe_load(yml_data) {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        if config.get('common'):
            self.template_version = 1
            self.__run_template_v1()

        elif config.get('version'):
            if config.get('version') == 2:
                self.template_version = 2
                self.__run_template_v2()

        else:
            error = 'Error method version_runner could not retrieve common, or version.'
            LOGGER.critical(error)
            Exception(error)

    def __run_template_v1(self):
        """
        Method to build, and output the template

        """
        try:
            config = yaml.safe_load(self.yml_data)

        except Exception as e:
            error = 'Error retrieving yml yaml.safe_load(yml_data) {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        try:
            common_data = config.get('common')

        except Exception as e:
            LOGGER.critical('Error could not retrieve common_data {}'.format(e))
            sys.exit(e)

        env = Environment(autoescape=select_autoescape(enabled_extensions=('html', 'xml', 'jinja2'),
                                                       default_for_string=True),
                          loader=FileSystemLoader(self.directories.get_templates_dir()), lstrip_blocks=True,
                          trim_blocks=True)

        self.output_file_name = pdt.file_name_increase(self.output_file_name, self.directories.get_output_dir())
        template = env.get_template(common_data.get('template'))

        if not self.display_only:
            try:
                pdt.list_to_file(template.render(common_data).splitlines(), self.output_file_name,
                                 self.directories.get_output_dir())

            except FileNotFoundError as e:
                LOGGER.critical('Can not write output {}'.format(self.directories.get_output_dir()))
                sys.exit(e)

        print(template.render(common_data))

        if self.display_json:
            self.__config_as_json(config)

        if self.display_yml:
            self.__config_as_yml(config)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            zip_file_name = pdt.file_name_increase('debug.zip', self.directories.get_output_dir())
            try:
                self.directories.collect_and_zip_files(self.__collect_templates(env), zip_file_name,
                                                       file_extension_list=['jinja2'], file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_yml_dir(self.yml_file_name)],
                                                       zip_file_name, file_extension_list=['yml', 'yaml'],
                                                       file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_data_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['config.yml'])
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])
                self.directories.collect_and_zip_files([self.directories.get_output_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=[self.output_file_name])

            except Exception as e:
                LOGGER.critical(e)
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])

            LOGGER.debug('config data: {}'.format(config))

        if self.package_name:
            self.__create_zip_package(env, self.output_file_name)

    def __run_template_v2(self):
        """
        Method to build, and output the template

        """
        try:
            config = yaml.safe_load(self.yml_data)

        except Exception as e:
            error = 'Error retrieving yml yaml.safe_load(yml_data) {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        try:
            common_data = config.get('data')

        except Exception as e:
            LOGGER.critical('Error could not retrieve common_data {}'.format(e))
            sys.exit(e)

        env = Environment(autoescape=select_autoescape(enabled_extensions=('html', 'xml', 'jinja2'),
                                                       default_for_string=True),
                          loader=FileSystemLoader(self.directories.get_templates_dir()), lstrip_blocks=True,
                          trim_blocks=True)

        env.filters.update(self.custom_filters)

        self.output_file_name = pdt.file_name_increase(self.output_file_name, self.directories.get_output_dir())

        for group in common_data:
            template = env.get_template(group.get('template'))

            if not self.display_only:
                try:
                    pdt.list_to_file(template.render(group).splitlines(), self.output_file_name,
                                     self.directories.get_output_dir())

                except FileNotFoundError as e:
                    LOGGER.critical('Can not write output {}'.format(self.directories.get_output_dir()))
                    sys.exit(e)

            print(template.render(group))
            if self.begin_string or self.include_string:
                self.__get_found_data(template.render(group))

        if self.display_json:
            self.__config_as_json(config)

        if self.display_yml:
            self.__config_as_yml(config)

        if LOGGER.getEffectiveLevel() == logging.DEBUG:
            zip_file_name = pdt.file_name_increase('debug.zip', self.directories.get_output_dir())
            try:
                self.directories.collect_and_zip_files(self.__collect_templates(env), zip_file_name,
                                                       file_extension_list=['jinja2'], file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_yml_dir(self.yml_file_name)],
                                                       zip_file_name, file_extension_list=['yml', 'yaml'],
                                                       file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_data_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['config.yml'])
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])
                self.directories.collect_and_zip_files([self.directories.get_output_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=[self.output_file_name])

            except Exception as e:
                LOGGER.critical(e)
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])

            LOGGER.debug('config data: {}'.format(config))

        if self.package_name:
            self.__create_zip_package(env, self.output_file_name)

    def __config_as_json(self, config_yml):
        """
        Method to see or output config as JSON data
        :param config_yml: A yml file
        :return
            None

        """
        json_data = json.dumps(config_yml, sort_keys=True, indent=4)
        print(json_data)
        if not self.display_only:
            try:
                if not self.output_file_name:
                    file_name = pdt.file_name_increase('config.json', self.directories.get_output_dir())

                else:
                    file_name = self.output_file_name

                pdt.list_to_file(json_data.splitlines(), file_name, self.directories.get_output_dir())

            except FileNotFoundError as e:
                LOGGER.critical('Can not write output {}'.format(self.directories.get_output_dir()))
                sys.exit(e)

    def __config_as_yml(self, config_yml):
        """
        Method to see or output config as YML data
        :param config_yml: A yml file
        :return
            None

        """
        yml_data = yaml.dump(config_yml, default_flow_style=False, indent=4)
        print(yml_data)
        if not self.display_only:
            try:
                if not self.output_file_name:
                    file_name = pdt.file_name_increase('config.json', self.directories.get_output_dir())

                else:
                    file_name = self.output_file_name

                pdt.list_to_file(yml_data.splitlines(), file_name, self.directories.get_output_dir())

            except FileNotFoundError as e:
                LOGGER.critical('Can not write output {}'.format(self.directories.get_output_dir()))
                sys.exit(e)

    def __variable_dict_builder(self, variables_file_name):
        """
        Method to create the variables dictionary
        :param variables_file_name: The name of the variable csv
        :return:
            A Dictionary of variables

        """
        data = dict()
        try:
            temp = pdt.csv_to_dict(variables_file_name, self.directories.get_yml_dir(variables_file_name))
            for key in temp.values():
                data[key.get('variable')] = key.get('value')

            return data

        except FileNotFoundError as e:
            LOGGER.critical('Error could not retrieve Variables file {}'.format(e))
            sys.exit(e)

    def __yml_variable_pre_run_environment(self, yml_file_name, variable_data):
        """
        Method to run the pre run Jinja2 environment
        :param yml_file_name: The yml file name
        :param variable_data: The variables csv file
        :return:
            A rendered yml file with variables filled in

        """
        pre_run_env = Environment(
            autoescape=select_autoescape(enabled_extensions=('yml', 'yaml'), default_for_string=True),
            loader=FileSystemLoader([self.directories.get_yml_dir(yml_file_name)]), lstrip_blocks=True,
            trim_blocks=True)

        pre_run_env.filters.update(self.custom_filters)

        try:
            temp_file = pre_run_env.get_template(yml_file_name)
            vars_yml_dict = self.__check_for_vars_section_in_yml(temp_file.render())
            if vars_yml_dict:
                variable_data.update(vars_yml_dict)

        except Exception as e:
            error = 'Error when running __yml_variable_pre_run_environment file name {} looking for vars'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        try:
            yml_file = pre_run_env.get_template(yml_file_name)
            return yml_file.render(variable_data)

        except Exception as e:
            error = 'Error when running __yml_variable_pre_run_environment file name {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

    def __pre_run_yml_input_file(self, yml_file_name=None, variables_file_name=None):
        """
        Method to pre run the yaml file to replace variables
        :param yml_file_name: The name of the input yml file
        :param variables_file_name: The name of the csv with variables
        :return
            A yml file with variables filled

        """
        data = dict()
        if variables_file_name:
            data = self.__variable_dict_builder(variables_file_name)

        return self.__yml_variable_pre_run_environment(yml_file_name, data)

    def __collect_templates(self, env):
        """
        Method to collect and zip all current templates in a a build run
        :param env: A Jinja2 Environment object
        :return:
            A list of directories

        """
        temp_set = set()
        for template_dir_name in self.directories.get_templates_dir():
            for a in env.list_templates():
                if os.path.isfile(os.path.join(template_dir_name, os.path.dirname(a), os.path.basename(a))):
                    temp_set.add(os.path.join(template_dir_name, os.path.dirname(a)))

        return list(temp_set)

    def __create_zip_package(self, env, output_file_name):
        """
        Method to create a zip package for reference
        :param env: A Jinja2 Environment object
        :param output_file_name: The out file name
        :return
            None

        """
        if len(self.package_name.split('.')) == 2:
            name, ext = self.package_name.split('.')
            if ext != 'zip':
                LOGGER.warning('Changed the extension of zip_file_name={} to be zip'.format(self.package_name))
                self.package_name = '{}.{}'.format(name, 'zip')

        else:
            error = 'Function create_zip_package expected zip_file_name to only contain one . ' \
                    'but received {}'.format(self.package_name)
            LOGGER.critical(error)
            raise NameError(error)

        self.package_name = pdt.file_name_increase(self.package_name, self.directories.get_output_dir())

        self.directories.collect_and_zip_files(self.__collect_templates(env), self.package_name,
                                               file_extension_list=['jinja2'], file_name_list=None)

        self.directories.collect_and_zip_files([self.directories.get_output_dir()], self.package_name,
                                               file_extension_list=None, file_name_list=[output_file_name])

    def __auto_build_template(self, variables_file_name):
        """
        Method to build a config using auto build
        :param variables_file_name: The Variables file name
        :return:
            The name of the yml template to use

        """
        try:
            data = self.__variable_dict_builder(variables_file_name)

            if data.get('yml_template'):
                return data.get('yml_template')

            else:
                raise KeyError('KeyError: There is no "yml_template" variable in the csv!')

        except Exception as e:
            LOGGER.critical(e)
            sys.exit(e)

    @staticmethod
    def __check_for_vars_section_in_yml(yml_data):
        """
        Method to retrieve vars in a yml file
        :param yml_data: The yml data to search for vars
        :return:
            A Dictionary of vars

        """
        try:
            config = yaml.safe_load(yml_data)

        except Exception as e:
            error = 'Error retrieving yml yaml.safe_load(yml_data) Method __check_for_vars_section_in_yml {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        return config.get('vars')

    def __get_found_data(self, config):
        """
        Method to search the config text, like a Cisco device
        :param config: The text to search
        :return:
            None

        """
        regex_device_config_start = re.compile(r'^<.*>$')
        regex_device_config_end = re.compile(r'^</.*>$')
        if self.include_string:
            regex_include = re.compile(r'.*{}'.format(' '.join(self.include_string)))
            print('\n!!!!!-- Include "{}"--!!!!!'.format(' '.join(self.include_string)))
            for line in config.splitlines():
                if re.match(regex_device_config_start, line):
                    print(line)

                elif re.match(regex_include, line):
                    print(line)

                elif re.match(regex_device_config_end, line):
                    print(line)

        if self.begin_string:
            regex_begin = re.compile(r'.*{}'.format(' '.join(self.begin_string)))
            print('\n!!!!!-- Begin "{}"--!!!!!'.format(' '.join(self.begin_string)))
            found_match = False
            for line in config.splitlines():
                if re.match(regex_begin, line):
                    found_match = True
                if re.match(regex_device_config_start, line):
                    print(line)

                elif found_match:
                    print(line)

                elif re.match(regex_device_config_end, line):
                    print(line)

    def server_rest(self):
        """
        Method to send a restful request to build on a remote server
        :return:
            Nothing yet

        """
        server_config = yaml.safe_load(open(os.path.join(self.directories.get_data_dir(),
                                                         'config.yml'))).get('remote_build_server_config')

        error = 'Missing parameter in remote_build_server_config: {}'.format(server_config)
        if not server_config.get('protocol'):
            LOGGER.critical(error)
            raise EnvironmentError(error)

        elif not server_config.get('server_host'):
            LOGGER.critical(error)
            raise EnvironmentError(error)

        elif not server_config.get('server_api_uri'):
            LOGGER.critical(error)
            raise EnvironmentError(error)

        elif not server_config.get('server_port'):
            LOGGER.critical(error)
            raise EnvironmentError(error)

        server_api_uri = server_config.get('server_api_uri')
        yaml_data = yaml.safe_load(self.yml_data)

        rest_object = ARestMe()
        rest_object.set_server_and_port(server_config.get('protocol'), server_config.get('server_host'),
                                        server_config.get('server_port'))
        rest_object.set_update_headers('Qct', 'ApiVersion1')
        rest_object.set_update_headers('Qct-Te', __version__)

        if yaml_data.get('remote_build_server_yaml_template'):
            response_data = rest_object.send_post('{server_api_uri}remote_yaml_'
                                                  'build'.format(server_api_uri=server_api_uri), yaml_data)

        else:
            response_data = rest_object.send_post('{server_api_uri}basic_build'.format(server_api_uri=server_api_uri),
                                                  yaml_data)

        if response_data.get('status_code') == 200:
            config = response_data.get('config')
            print(config)
            if self.begin_string or self.include_string:
                self.__get_found_data(config)

            if not self.display_only:
                self.output_file_name = pdt.file_name_increase(self.output_file_name, self.directories.get_output_dir())
                try:
                    pdt.list_to_file(config.splitlines(), self.output_file_name,
                                     self.directories.get_output_dir())

                except FileNotFoundError as e:
                    LOGGER.critical('Can not write output {}'.format(self.directories.get_output_dir()))
                    sys.exit(e)

            if self.display_json:
                self.__config_as_json(yaml_data)

            if self.display_yml:
                self.__config_as_yml(yaml_data)

        else:
            print(response_data.get('error'))


class ServerTemplateEngine(object):
    """
    Class to render, and clean Jinja2 templates from the server side
    """
    custom_filters = custom_filters

    def __init__(self, directories=None, config=None):
        self.directories = directories
        self.config = config
        self.yml_file_name = None
        self.output_file_name = None
        self.display_only = True
        self.display_json = False
        self.display_yml = False
        self.package_name = None
        self.template_version = None

    def run_template_version(self):
        """
        Method to check the version of yaml, and build a config
        :return:
            A Tuple with the following
            (dict, int)

        """
        if self.config.get('common'):
            error = 'Error method version_runner could not retrieve common, or version.'
            SERVER_LOGGER.critical(error)
            return {'status_code': 400, 'error': error}, 400

        elif self.config.get('version'):
            if int(self.config.get('version')) == 2:
                return self.__run_template_v2(self.config)

            else:
                error = 'Error template version {} is not supported.'.format(self.config.get('version'))
                SERVER_LOGGER.critical(error)
                return {'status_code': 400, 'error': error}, 400

        else:
            error = 'Error method version_runner could not retrieve common, or version.'
            SERVER_LOGGER.critical(error)
            return {'status_code': 400, 'error': error}, 400

    def __run_template_v2(self, config):
        """
        Method to build, and output the template
        :param config: A dict from a yaml, or json
        :return:
            A Tuple with the following
            (dict, int)

        """
        try:
            common_data = config.get('data')

        except Exception as e:
            SERVER_LOGGER.critical('Error could not retrieve common_data {}'.format(e))
            sys.exit(e)

        try:
            env = Environment(autoescape=select_autoescape(enabled_extensions=('html', 'xml', 'jinja2'),
                                                           default_for_string=True),
                              loader=FileSystemLoader(self.directories.get_templates_dir()), lstrip_blocks=True,
                              trim_blocks=True)

            env.filters.update(self.custom_filters)

            rendered = str()
            for group in common_data:
                template = env.get_template(group.get('template'))
                rendered += template.render(group)
            return {'status_code': 200, 'config': rendered}, 200

        except j2_exceptions.TemplateNotFound as e:
            error = 'Error can not find template {} in any of these {}.'.format(e, self.directories.get_templates_dir())
            SERVER_LOGGER.critical(error)
            return {'status_code': 400, 'error': error}, 400

    def get_remote_yaml_template(self):
        """
        Method to build, a yaml file to then run a jinja2 template
        :return:
            A Tuple with the following
            (dict, int)

        """
        if self.config.get('remote_build_server_yaml_template'):
            try:
                env = Environment(autoescape=select_autoescape(enabled_extensions=('html', 'xml', 'jinja2'),
                                                               default_for_string=True),
                                  loader=FileSystemLoader(self.directories.get_templates_dir()), lstrip_blocks=True,
                                  trim_blocks=True)

                env.filters.update(self.custom_filters)

                template = env.get_template(self.config.get('remote_build_server_yaml_template'))

                config = yaml.safe_load(template.render(self.config.get('vars')))

                return self.__run_template_v2(config)

            except j2_exceptions.TemplateNotFound as e:
                error = 'Error can not find template {} in any of these ' \
                        '{}.'.format(e, self.directories.get_templates_dir())
                SERVER_LOGGER.critical(error)
                return {'status_code': 400, 'error': error}, 400
