import logging
from jinja2 import Environment, select_autoescape, FileSystemLoader
import yaml
import json
from module import pdt
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 3, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def run_template(directories=None, yml_data=None, output_file_name=None, display_only=False,
                 display_json=False, display_yml=False):
    """
    Function to build, and output the template
    :param directories: The directory the templates are in
    :param yml_data: The yaml data after pre processing
    :param output_file_name: name of the output file
    :param display_only: Do not output data
    :param display_json: Display data in JSON format
    :param display_yml: Display data in YML format
    :return:
        None

    """
    common_data = None
    file_name = None

    config = yaml.safe_load(yml_data)

    try:
        common_data = config.get('common')

    except Exception as e:
        LOGGER.critical('Error could not retrieve common_data {}'.format(e))
        exit(e)

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
            exit(e)

    print(template.render(common_data))

    if display_json:
        config_as_json(config, display_only, directories.get_output_dir(), file_name)

    if display_yml:
        config_as_yml(config, display_only, directories.get_output_dir(), file_name)

    if LOGGER.getEffectiveLevel() == logging.DEBUG:
        LOGGER.debug('config data: {}'.format(config))


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
            exit(e)


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
            exit(e)


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

    pre_run_env = Environment(autoescape=select_autoescape(enabled_extensions=('yml', 'yaml'), default_for_string=True),
                              loader=FileSystemLoader([input_dir]), lstrip_blocks=True, trim_blocks=True)

    if variables_file_name:
        try:
            temp = pdt.csv_to_dict(variables_file_name, input_dir)
            for key in temp.values():
                data[key.get('variable')] = key.get('value')

        except FileNotFoundError as e:
            LOGGER.critical('Error could not retrieve Variables file {}'.format(e))
            exit(e)

    yml_file = pre_run_env.get_template(yml_file_name)
    return yml_file.render(data)
