import logging
import sys
import os
import persistentdatatools as pdt
from ..utils import clean_list
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'prod'
__version_info__ = (1, 0, 0, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def convert_prefix_list_to_our_format(directories=None, input_file_name=None, output_file_name=None,
                                      display_only=False):
    """
    Function to convert a Prefix-List to a YML format for QuickConfigTemplates
    :param directories:
    :param input_file_name: The input file name
    :param output_file_name: The output file name
    :param display_only: Boolean true = don't output to file
    :return:
        None

    """
    temp_list = list()
    dict_of_prefix_lists = dict()

    try:
        prefix_lists = pdt.file_to_list(input_file_name, directories.get_yml_dir())
        prefix_lists = clean_list(prefix_lists)

        if len(prefix_lists) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(), input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for line in prefix_lists:
        critical_issue = False
        line_split = line.split()
        try:
            if not dict_of_prefix_lists.get(line_split[2]):
                dict_of_prefix_lists[line_split[2]] = list()

        except IndexError:
            error = 'Cannot find Prefix-List name in this statement "{}"'.format(line)
            LOGGER.error(error)
            print(error)
            critical_issue = True

        temp_dict = dict()
        try:
            temp_dict.update({'sequence': line_split[4]})

        except IndexError:
            error = 'Cannot find sequence in this statement "{}"'.format(line)
            LOGGER.error(error)
            print(error)
            critical_issue = True

        try:
            temp_dict.update({'network': line_split[6]})

        except IndexError:
            error = 'Cannot find network in this statement "{}"'.format(line)
            LOGGER.error(error)
            print(error)
            critical_issue = True

        if critical_issue:
            error = 'Your data in file {} does not all seem to be a Prefix-List, or ' \
                    'Prefix-Lists'.format(os.path.join(directories.get_yml_dir(), input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

        if 'permit' in line_split:
            temp_dict.update({'permit_deny': 'permit'})

        else:
            temp_dict.update({'permit_deny': 'deny'})

        if 'le' in line_split:
            temp_dict.update({'le_ge': 'le', 'le_ge_value': line_split[8]})

        elif 'ge' in line_split:
            temp_dict.update({'le_ge': 'ge', 'le_ge_value': line_split[8]})

        dict_of_prefix_lists[line_split[2]].append(temp_dict)

    temp_list.append('--- # Created from file: {} with pl_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')
    temp_list.append('            prefix_lists:')
    for prefix_list_name in dict_of_prefix_lists:
        temp_list.append('            -   prefix_list_name: {}'.format(prefix_list_name))
        temp_list.append('                sequences:')
        seq_list = dict_of_prefix_lists.get(prefix_list_name)
        for seq_dict in seq_list:
            temp_list.append('                -   sequence: {}'.format(seq_dict.get('sequence')))
            temp_list.append('                    permit_deny: {}'.format(seq_dict.get('permit_deny')))
            temp_list.append('                    network: {}'.format(seq_dict.get('network')))
            if seq_dict.get('le_ge'):
                temp_list.append('                    le_ge: {}'.format(seq_dict.get('le_ge')))
                temp_list.append('                    le_ge_value: {}'.format(seq_dict.get('le_ge_value')))

    if not display_only:
        file_name = pdt.file_name_increase(output_file_name, directories.get_output_dir())
        pdt.list_to_file(temp_list, file_name, directories.get_output_dir())

    for final_yml in temp_list:
        print(final_yml)
