import logging
import sys
import os
import persistentdatatools as pdt
from ..utils import clean_list
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018 Ben Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'prod'
__version_info__ = (1, 0, 1, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class PrefixListData(object):
    """
    Class to hold 1 Prefix-Lists's Data
    """
    def __init__(self, name, reset_sequences=False):
        self.name = name
        self.reset_sequences = reset_sequences
        self.current_seq = 5
        self.lines = list()

    def __str__(self):
        return '<PrefixListData: Prefix-List Name {}>'.format(self.name)

    def __repr__(self):
        return '<PrefixListData: Prefix-List Name {}>'.format(self.name)

    def set_lines(self, line_data):
        """
        Method to set the sequences description
        :param line_data: String data
        :return:
            None
        """
        line_data_split = line_data.split()
        temp_dict = dict()
        if self.reset_sequences:
            temp_dict.update({'sequence': self.current_seq, 'network': line_data_split[6]})
            self.current_seq += 5
        else:
            temp_dict.update({'sequence': line_data_split[4], 'network': line_data_split[6]})

        if 'permit' in line_data:
            temp_dict.update({'permit_deny': 'permit'})

        else:
            temp_dict.update({'permit_deny': 'deny'})

        if 'le' in line_data:
            temp_dict.update({'le_ge': 'le', 'le_ge_value': line_data_split[8]})

        elif 'ge' in line_data:
            temp_dict.update({'le_ge': 'ge', 'le_ge_value': line_data_split[8]})

        self.lines.append(temp_dict)

    def get_name(self):
        """
        Method to get the Prefix-List name
        :return:
            String Prefix-List name
        """
        return self.name

    def get_lines(self):
        """
        Method to get a Prefix-List's sequences
        :return:
            List of dictionaries
        """
        return self.lines


def convert_prefix_list_to_our_format(directories=None, input_file_name=None, output_file_name=None,
                                      display_only=False, reset_sequences=False):
    """
    Function to convert a Prefix-List to a YML format for QuickConfigTemplates
    :param directories:
    :param input_file_name: The input file name
    :param output_file_name: The output file name
    :param display_only: Boolean true = don't output to file
    :param reset_sequences: Set True to recount sequences
    :return:
        None

    """
    temp_list = list()
    pl_obj = None

    try:
        prefix_lists = pdt.file_to_list(input_file_name, directories.get_yml_dir(input_file_name))
        prefix_lists = clean_list(prefix_lists)

        if len(prefix_lists) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(input_file_name),
                                                                   input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for line in prefix_lists:
        line_split = line.split()
        if not pl_obj:
            pl_obj = PrefixListData(line_split[2], reset_sequences=reset_sequences)
            pl_obj.set_lines(line)

        else:
            pl_obj.set_lines(line)

    temp_list.append('--- # Created from file: {} with pl_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')
    temp_list.append('            prefix_lists:')
    temp_list.append('            -   prefix_list_name: {}'.format(pl_obj.get_name()))
    temp_list.append('                sequences:')
    for seq_dict in pl_obj.get_lines():
        temp_list.append('                -   sequence: {}'.format(seq_dict.get('sequence')))
        temp_list.append('                    permit_deny: {}'.format(seq_dict.get('permit_deny')))
        temp_list.append('                    network: {}'.format(seq_dict.get('network')))
        if seq_dict.get('le_ge'):
            temp_list.append('                    le_ge: {}'.format(seq_dict.get('le_ge')))
            temp_list.append('                    le_ge_value: {}'.format(seq_dict.get('le_ge_value')))

    if not display_only:
        file_name = pdt.file_name_increase(output_file_name, directories.get_output_dir())
        pdt.list_to_file(temp_list, file_name, directories.get_output_dir())
        output_notify = 'Filename: {} output to directory {}'.format(file_name, directories.get_output_dir())
        print(output_notify)
        LOGGER.debug(output_notify)

    for final_yml in temp_list:
        print(final_yml)
