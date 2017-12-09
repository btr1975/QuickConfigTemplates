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
    dict_of_acls = dict()
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
        # print(line_split)

        if line_split[0] == 'ip':

            try:
                if not dict_of_acls.get(line_split[3]):
                    if line_split[2] == 'standard':
                        acl_type = 'standard'
                        current_acl_name = line_split[3]
                        dict_of_acls[current_acl_name] = {acl_type: list()}

                    elif line_split[2] == 'extended':
                        acl_type = 'extended'
                        current_acl_name = line_split[3]
                        dict_of_acls[current_acl_name] = {acl_type: list()}

            except IndexError:
                error = 'Cannot find ACL name in this statement "{}"'.format(line)
                LOGGER.error(error)
                print(error)
                critical_issue = True

        elif int(line_split[0]) and acl_type == 'standard':
            dict_of_acls.get(current_acl_name).get(acl_type).append({'sequence': line_split[0],
                                                                     'permit_deny': line_split[1],
                                                                     'source_network': ' '.join(line_split[2:])})

    temp_list.append('--- # Created from file: {} with acl_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')

    for acl_name in dict_of_acls:
        acl = dict_of_acls.get(acl_name)
        for acl_type in acl:
            acl_list = acl.get(acl_type)
            if acl_type == 'standard':
                temp_list.append('            standard_acls:')
            temp_list.append('            -   acl_name: {}'.format(acl_name))
            temp_list.append('                sequences:')
            for dict_acl in acl_list:
                temp_list.append('                -   sequence: {}'.format(dict_acl.get('sequence')))
                temp_list.append('                    permit_deny: {}'.format(dict_acl.get('permit_deny')))
                temp_list.append('                    source_network: {}'.format(dict_acl.get('source_network')))


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

    print(dict_of_acls)