import logging
import sys
from jinja2 import Environment, select_autoescape, FileSystemLoader
import yaml
import json
import persistentdatatools as pdt
import ipaddresstools as ipv4
import os
# from .arestme import ARestMe
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018 Ben Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'dev'
__version_info__ = (2, 0, 3, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)
TEMPLATE_LOGGER = logging.getLogger('template')


def filter_check_u_ip_address(value):
    """
    Function to check for a unicast ipv4 address in a template
    :param value:
    :return:
    """
    if not value:
        return '{value} !!!! possible error this is required to be a unicast ipv4 address !!!!'.format(value=value)

    elif ipv4.ucast_ip(value, return_tuple=False):
        return value

    else:
        return '{value} !!!! possible error this is required to be a unicast ipv4 address !!!!'.format(value=value)


def filter_check_u_subnet(value):
    """
    Function to check for a subnet and mask combo in a template
    :param value:
    :return:
    """
    if not value:
        return '{value} !!!! possible error this is required to be a unicast ipv4 subnet !!!!'.format(value=value)

    elif ipv4.ip_mask(value, return_tuple=False):
        return value

    else:
        return '{value} !!!! possible error this is required to be a unicast ipv4 subnet !!!!'.format(value=value)


def filter_check_ip_mask_cidr(value):
    """
    Function to check to a CIDR mask number in a template
    :param value:
    :return:
    """
    if not value:
        return '{value} !!!! possible error this is required to be a ipv4 subnet mask in CIDR!!!!'.format(value=value)

    try:
        if ipv4.mask_conversion.get(int(value)):
            return value

        else:
            return '{value} !!!! possible error this is required to be a ipv4 subnet mask in CIDR!!!!'.format(
                value=value)

    except ValueError as e:
        TEMPLATE_LOGGER.info(e)
        return '{value} !!!! possible error this is required to be a ipv4 subnet mask in CIDR!!!!'.format(value=value)


def filter_check_ip_mask_standard(value):
    """
    Function to check for a standard mask in a template
    :param value:
    :return:
    """
    if not value:
        return '{value} !!!! possible error this is required to be a ipv4 standard subnet mask!!!!'.format(value=value)

    else:
        not_found = False
        for key in ipv4.mask_conversion:
            if ipv4.mask_conversion.get(key).get('MASK') == value:
                return value

            else:
                not_found = True

        if not_found:
            return '{value} !!!! possible error this is required to be a ipv4 standard subnet ' \
                   'mask!!!!'.format(value=value)


def filter_check_m_ip_address(value):
    """
    Function to check for a multicast ipv4 address in a template
    :param value:
    :return:
    """
    if not value:
        return '{value} !!!! possible error this is required to be a multicast ipv4 address !!!!'.format(value=value)

    elif ipv4.mcast_ip(value, return_tuple=False):
        return value

    else:
        return '{value} !!!! possible error this is required to be a multicast ipv4 address !!!!'.format(value=value)


class TemplateEngine(object):
    """
    Class to render, and clean Jinja2 templates
    """

    def __init__(self, directories=None, yml_file_name=None, output_file_name=None, display_only=False,
                 display_json=False, display_yml=False, package_name=None, variables_file_name=None, auto_build=None,
                 remote_build=False):
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

        env.filters['u_ip_address'] = filter_check_u_ip_address
        env.filters['m_ip_address'] = filter_check_m_ip_address
        env.filters['u_subnet'] = filter_check_u_subnet
        env.filters['mask_cidr'] = filter_check_ip_mask_cidr
        env.filters['mask_standard'] = filter_check_ip_mask_standard

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

    def server_rest(self):
        error = 'Remote build not implemented yet!!'
        print(error)
        LOGGER.critical(error)
        # server_config = yaml.safe_load(open(os.path.join(self.directories.get_data_dir(), 'config.yml'))).get('server_config')
        # server_api_uri = server_config.get('server_api_uri')
        # b = yaml.safe_load(self.yml_data)


        # a = ARestMe()
        # a.set_server_and_port(server_config.get('protocol'), server_config.get('server_host'), server_config.get('server_port'))
        # a.set_update_headers('QCT', 'ApiVersion1')
        # print(a.send_post('{server_api_uri}postinfo'.format(server_api_uri=server_api_uri), b))
