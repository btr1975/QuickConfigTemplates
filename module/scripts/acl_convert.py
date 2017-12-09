import logging
import sys
import os
import persistentdatatools as pdt
from ..utils import clean_list
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'dev'
__version_info__ = (1, 0, 0, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class StandardAclData(object):

    def __init__(self, name):
        self.name = name
        self.lines = list()
        self.acl_type = 'standard'

    def __str__(self):
        return '<StandardAclData: ACL Name {}>'.format(self.name)

    def __repr__(self):
        return '<StandardAclData: ACL Name {}>'.format(self.name)

    def set_lines(self, line_data):
        line_data_split = line_data.split()
        self.lines.append({'sequence': line_data_split[0],
                           'permit_deny': line_data_split[1],
                           'source_network': ' '.join(line_data_split[2:])})

    def get_name(self):
        return self.name

    def get_acl_type(self):
        return self.acl_type

    def get_lines(self):
        return self.lines


class ExtendedAclData(object):

    def __init__(self, name):
        self.name = name
        self.lines = list()
        self.acl_type = 'standard'

    def __str__(self):
        return '<ExtendedAclData: ACL Name {}>'.format(self.name)

    def __repr__(self):
        return '<ExtendedAclData: ACL Name {}>'.format(self.name)

    def set_lines(self, line_data):
        pass

    def get_name(self):
        return self.name

    def get_acl_type(self):
        return self.acl_type

    def get_lines(self):
        return self.lines


def convert_acl_to_our_format(directories=None, input_file_name=None, output_file_name=None, display_only=False):
    """
    Function to convert a ACL to a YML format for QuickConfigTemplates
    :param directories:
    :param input_file_name: The input file name
    :param output_file_name: The output file name
    :param display_only: Boolean true = don't output to file
    :return:
        None

    """
    temp_list = list()
    acl_obj = None
    print(directories)
    print(input_file_name)
    print(output_file_name)
    print(display_only)

    try:
        acls = pdt.file_to_list(input_file_name, directories.get_yml_dir())
        acls = clean_list(acls)

        if len(acls) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(), input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for line in acls:
        critical_issue = False
        line_split = line.split()
        print(line_split)

        if line_split[0] == 'ip':

            try:
                if line_split[2] == 'standard':
                    print(line_split)
                    acl_obj = StandardAclData(line_split[3])
                elif line_split[2] == 'extended':
                    acl_obj = ExtendedAclData(line_split[3])

            except IndexError:
                error = 'Cannot find ACL name in this statement "{}"'.format(line)
                LOGGER.error(error)
                print(error)
                critical_issue = True

        elif int(line_split[0]):
            if acl_obj:
                acl_obj.set_lines(line)

            else:
                print('shit')

    temp_list.append('--- # Created from file: {} with acl_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')
    if acl_obj.get_acl_type() == 'standard':
        temp_list.append('            standard_acls:')
        temp_list.append('            -   acl_name: {}'.format(acl_obj.get_name()))
        temp_list.append('                sequences:')
        for line_data in acl_obj.get_lines():
            temp_list.append('                -   sequence: {}'.format(line_data.get('sequence')))
            temp_list.append('                    permit_deny: {}'.format(line_data.get('permit_deny')))
            temp_list.append('                    source_network: {}'.format(line_data.get('source_network')))
    """
--- # Test data to for ios
common:
    template: ios_base.jinja2
    ticket_number: CHG123456789
    devices:
    -   device:
        -   devicename: IOS-RTR02
            management_ip: 10.99.222.23
            standard_acls:
            -   acl_name: ACL-STANDARD-1
                sequences:
                -   permit_deny: permit
                    sequence: 10
                    source_network: 192.168.1.0 0.0.0.255

                -   permit_deny: deny
                    sequence: 20
                    source_network: 192.168.2.0 0.0.0.255

                -   permit_deny: permit
                    sequence: 30
                    source_network: 192.168.3.0 0.0.0.255
    """

    for acl_yml_line in temp_list:
        print(acl_yml_line)
