import logging
import sys
from jinja2 import Environment, select_autoescape, FileSystemLoader
import yaml
import json
import persistentdatatools as pdt
import os
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'prod'
__version_info__ = (1, 0, 5, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class TemplateEngine(object):

    def __init__(self, directories=None, yml_file_name=None, output_file_name=None, display_only=False,
                 display_json=False, display_yml=False, package_name=None, variables_file_name=None):
        self.directories = directories
        self.yml_data = self.__pre_run_yml_input_file(yml_file_name, variables_file_name)
        self.output_file_name = output_file_name
        self.display_only = display_only
        self.display_json = display_json
        self.display_yml = display_yml
        self.package_name = package_name
        self.version_runner()

    def version_runner(self):
        try:
            config = yaml.safe_load(self.yml_data)

        except Exception as e:
            error = 'Error retrieving yml yaml.safe_load(yml_data) {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

        if config.get('common'):
            self.run_template_v1()

        elif config.get('version'):
            pass

        else:
            error = 'Error method version_runner could not retrieve common, or version.'
            LOGGER.critical(error)
            Exception(error)

    def run_template_v1(self):
        """
        Method to build, and output the template

        """
        file_name = None
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

        template = env.get_template(common_data.get('template'))

        if not self.display_only:
            try:
                file_name = pdt.file_name_increase(self.output_file_name, self.directories.get_output_dir())
                pdt.list_to_file(template.render(common_data).splitlines(), file_name,
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
                self.directories.collect_and_zip_files(collect_templates(env, self.directories), zip_file_name,
                                                       file_extension_list=['jinja2'], file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_yml_dir()], zip_file_name,
                                                       file_extension_list=['yml', 'yaml'], file_name_list=None)
                self.directories.collect_and_zip_files([self.directories.get_data_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['config.yml'])
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])
                self.directories.collect_and_zip_files([self.directories.get_output_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=[file_name])

            except Exception as e:
                LOGGER.critical(e)
                self.directories.collect_and_zip_files([self.directories.get_logging_dir()], zip_file_name,
                                                       file_extension_list=None, file_name_list=['logs.txt'])

            LOGGER.debug('config data: {}'.format(config))

        if self.package_name:
            self.__create_zip_package(env, file_name)

    def __config_as_json(self, config_yml):
        """
        Method to see or output config as JSON data

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


        :param variables_file_name: The name of the variable csv
        :return:
            A Dictionary of variables

        """
        data = dict()
        try:
            temp = pdt.csv_to_dict(variables_file_name, self.directories.get_yml_dir())
            for key in temp.values():
                data[key.get('variable')] = key.get('value')

            return data

        except FileNotFoundError as e:
            LOGGER.critical('Error could not retrieve Variables file {}'.format(e))
            sys.exit(e)

    def __yml_variable_pre_run_environment(self, yml_file_name, variable_data):
        """

        :param yml_file_name: The yml file name
        :param variable_data: The variables csv file
        :return:
            A rendered yml file with variables filled in

        """
        pre_run_env = Environment(
            autoescape=select_autoescape(enabled_extensions=('yml', 'yaml'), default_for_string=True),
            loader=FileSystemLoader([self.directories.get_yml_dir()]), lstrip_blocks=True, trim_blocks=True)

        try:
            yml_file = pre_run_env.get_template(yml_file_name)
            return yml_file.render(variable_data)

        except Exception as e:
            error = 'Error when running yml_variable_pre_run_environment file name {}'.format(e)
            LOGGER.critical(error)
            sys.exit(error)

    def __pre_run_yml_input_file(self, yml_file_name=None, variables_file_name=None):
        """
        Method to pre run the yaml file to replace variables

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


def run_template(directories=None, yml_data=None, output_file_name=None, display_only=False,
                 display_json=False, display_yml=False, package_name=None):
    """
    Function to build, and output the template
    :param directories: The directory the templates are in
    :param yml_data: The yaml data after pre processing
    :param output_file_name: name of the output file
    :param display_only: Do not output data
    :param display_json: Display data in JSON format
    :param display_yml: Display data in YML format
    :param package_name: The name of the zip file package
    :return:
        None

    """
    file_name = None
    try:
        config = yaml.safe_load(yml_data)

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
                      loader=FileSystemLoader(directories.get_templates_dir()), lstrip_blocks=True, trim_blocks=True)

    template = env.get_template(common_data.get('template'))

    if not display_only:
        try:
            file_name = pdt.file_name_increase(output_file_name, directories.get_output_dir())
            pdt.list_to_file(template.render(common_data).splitlines(), file_name, directories.get_output_dir())

        except FileNotFoundError as e:
            LOGGER.critical('Can not write output {}'.format(directories.get_output_dir()))
            sys.exit(e)

    print(template.render(common_data))

    if display_json:
        config_as_json(config, display_only, directories.get_output_dir(), file_name)

    if display_yml:
        config_as_yml(config, display_only, directories.get_output_dir(), file_name)

    if LOGGER.getEffectiveLevel() == logging.DEBUG:
        zip_file_name = pdt.file_name_increase('debug.zip', directories.get_output_dir())
        try:
            directories.collect_and_zip_files(collect_templates(env, directories), zip_file_name,
                                              file_extension_list=['jinja2'], file_name_list=None)
            directories.collect_and_zip_files([directories.get_yml_dir()], zip_file_name,
                                              file_extension_list=['yml', 'yaml'], file_name_list=None)
            directories.collect_and_zip_files([directories.get_data_dir()], zip_file_name, file_extension_list=None,
                                              file_name_list=['config.yml'])
            directories.collect_and_zip_files([directories.get_logging_dir()], zip_file_name, file_extension_list=None,
                                              file_name_list=['logs.txt'])
            directories.collect_and_zip_files([directories.get_output_dir()], zip_file_name, file_extension_list=None,
                                              file_name_list=[file_name])

        except Exception as e:
            LOGGER.critical(e)
            directories.collect_and_zip_files([directories.get_logging_dir()], zip_file_name, file_extension_list=None,
                                              file_name_list=['logs.txt'])

        LOGGER.debug('config data: {}'.format(config))

    if package_name:
        create_zip_package(env, directories, package_name, file_name)


def config_as_json(config_yml, display_only, dir_out, output_file_name):
    """
    Function to see or output config as JSON data
    :param config_yml: The yml data
    :param display_only: Do not output data
    :param dir_out: The output directory
    :param output_file_name: The output file name
    :return:
        None

    """
    json_data = json.dumps(config_yml, sort_keys=True, indent=4)
    print(json_data)
    if not display_only:
        try:
            if not output_file_name:
                file_name = pdt.file_name_increase('config.json', dir_out)

            else:
                file_name = output_file_name

            pdt.list_to_file(json_data.splitlines(), file_name, dir_out)

        except FileNotFoundError as e:
            LOGGER.critical('Can not write output {}'.format(dir_out))
            sys.exit(e)


def config_as_yml(config_yml, display_only, dir_out, output_file_name):
    """
    Function to see or output config as YML data
    :param config_yml: The yml data
    :param display_only: Do not output data
    :param dir_out: The output directory
    :param output_file_name: The output file name
    :return:
        None

    """
    yml_data = yaml.dump(config_yml, default_flow_style=False, indent=4)
    print(yml_data)
    if not display_only:
        try:
            if not output_file_name:
                file_name = pdt.file_name_increase('config.json', dir_out)

            else:
                file_name = output_file_name

            pdt.list_to_file(yml_data.splitlines(), file_name, dir_out)

        except FileNotFoundError as e:
            LOGGER.critical('Can not write output {}'.format(dir_out))
            sys.exit(e)


def variable_dict_builder(input_dir, variables_file_name):
    """

    :param input_dir: The yaml input directory
    :param variables_file_name: The name of the variable csv
    :return:
        A Dictionary of variables

    """
    data = dict()
    try:
        temp = pdt.csv_to_dict(variables_file_name, input_dir)
        for key in temp.values():
            data[key.get('variable')] = key.get('value')

        return data

    except FileNotFoundError as e:
        LOGGER.critical('Error could not retrieve Variables file {}'.format(e))
        sys.exit(e)


def yml_variable_pre_run_environment(input_dir, yml_file_name, variable_data):
    """

    :param input_dir: The input directory of the yml file
    :param yml_file_name: The yml file name
    :param variable_data: The variables csv file
    :return:
        A rendered yml file with variables filled in

    """
    pre_run_env = Environment(autoescape=select_autoescape(enabled_extensions=('yml', 'yaml'), default_for_string=True),
                              loader=FileSystemLoader([input_dir]), lstrip_blocks=True, trim_blocks=True)

    try:
        yml_file = pre_run_env.get_template(yml_file_name)
        return yml_file.render(variable_data)

    except Exception as e:
        error = 'Error when running yml_variable_pre_run_environment file name {}'.format(e)
        LOGGER.critical(error)
        sys.exit(error)


def pre_run_yml_input_file(input_dir=None, yml_file_name=None, variables_file_name=None):
    """
    Function to pre run the yaml file to replace variables
    :param input_dir: The yaml input directory
    :param yml_file_name: The name of the yaml file
    :param variables_file_name: The name of the variable csv
    :return:
        A yaml file with variables replaced

    """
    data = dict()
    if variables_file_name:
        data = variable_dict_builder(input_dir, variables_file_name)

    return yml_variable_pre_run_environment(input_dir, yml_file_name, data)


def auto_build_template(directories=None, variables_file_name=None):
    """
    Function to build a config using auto build
    :param directories: The Directory object
    :param variables_file_name: The Variables file name
    :return:
        The name of the yml template to use

    """
    try:
        data = variable_dict_builder(directories.get_yml_dir(), variables_file_name)

        if data.get('yml_template'):
            return data.get('yml_template')

        else:
            raise KeyError('KeyError: There is no "yml_template" variable in the csv!')

    except Exception as e:
        LOGGER.critical(e)
        sys.exit(e)


def create_zip_package(env, directories, zip_file_name, output_file_name):
    """
    Function to create a zip package for reference
    :param env: A Jinja2 Environment object
    :param directories: Directories object
    :param zip_file_name: The name of the zip file
    :param output_file_name: The name of the output config file
    :return:
        None

    """
    if len(zip_file_name.split('.')) == 2:
        name, ext = zip_file_name.split('.')
        if ext != 'zip':
            LOGGER.warning('Changed the extension of zip_file_name={} to be zip'.format(zip_file_name))
            zip_file_name = '{}.{}'.format(name, 'zip')

    else:
        error = 'Function create_zip_package expected zip_file_name to only contain one . ' \
                'but received {}'.format(zip_file_name)
        LOGGER.critical(error)
        raise NameError(error)

    zip_file_name = pdt.file_name_increase(zip_file_name, directories.get_output_dir())

    directories.collect_and_zip_files(collect_templates(env, directories), zip_file_name,
                                      file_extension_list=['jinja2'], file_name_list=None)

    directories.collect_and_zip_files([directories.get_output_dir()], zip_file_name, file_extension_list=None,
                                      file_name_list=[output_file_name])


def collect_templates(env, directories):
    """
    Function to collect and zip all current templates in a a build run
    :param env: A Jinja2 Environment object
    :param directories: Directories object
    :return:
        A list of directories

    """
    temp_set = set()
    for template_dir_name in directories.get_templates_dir():
        for a in env.list_templates():
            if os.path.isfile(os.path.join(template_dir_name, os.path.dirname(a), os.path.basename(a))):
                temp_set.add(os.path.join(template_dir_name, os.path.dirname(a)))

    return list(temp_set)
