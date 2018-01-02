import logging
import sys
import os
import persistentdatatools as pdt
import ipaddresstools as ipv4
from ..utils import clean_list
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'dev'
__version_info__ = (1, 0, 1, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class StandardAclData(object):

    def __init__(self, name, reset_sequences=False):
        self.name = name
        self.reset_sequences = reset_sequences
        self.current_seq = 10
        self.lines = list()
        self.acl_type = 'standard'

    def __str__(self):
        return '<StandardAclData: ACL Name {}>'.format(self.name)

    def __repr__(self):
        return '<StandardAclData: ACL Name {}>'.format(self.name)

    def set_lines(self, line_data):
        line_data_split = line_data.split()
        temp_dict = dict()
        if line_data_split[0] == 'permit' or line_data_split[0] == 'deny':
            temp_dict.update({'sequence': self.current_seq,
                              'permit_deny': line_data_split[0],
                              'source_network': ' '.join(line_data_split[1:])})
            self.current_seq += 10

        elif line_data_split[0] == 'remark':
            pass

        else:
            try:
                int(line_data_split[0])
                if self.reset_sequences:
                    temp_dict.update({'sequence': self.current_seq})
                    self.current_seq += 10

                else:
                    temp_dict.update({'sequence': line_data_split[0]})

                temp_dict.update({'permit_deny': line_data_split[1],
                                  'source_network': ' '.join(line_data_split[2:])})

            except Exception as e:
                LOGGER.critical(e)
                sys.exit(e)

        self.lines.append(temp_dict)

    def get_name(self):
        return self.name

    def get_acl_type(self):
        return self.acl_type

    def get_lines(self):
        return self.lines


class ExtendedAclData(object):

    def __init__(self, name, reset_sequences=False):
        self.name = name
        self.reset_sequences = reset_sequences
        self.current_seq = 10
        self.lines = list()
        self.acl_type = 'extended'

    def __str__(self):
        return '<ExtendedAclData: ACL Name {}>'.format(self.name)

    def __repr__(self):
        return '<ExtendedAclData: ACL Name {}>'.format(self.name)

    def set_lines(self, line_data):
        temp_dict = dict()
        prev_enum = 0
        hit_once = False
        line_data_split = line_data.split()
        for enum, entry in enumerate(line_data_split):
            if ipv4.ip(entry, return_tuple=False):
                if not hit_once:
                    temp_network = None

                else:
                    temp_network = None

            elif ipv4.ip_mask(entry, return_tuple=False):
                if not hit_once:
                    temp_dict.update({'source_network': entry})
                    hit_once = True
                else:
                    temp_dict.update({'destination_network': entry})
                    print(temp_dict)

        if line_data_split[2] == 'ip':
            if ipv4.ip_mask(line_data_split[3], return_tuple=False):
                temp_dict.update({'sequence': line_data_split[0],
                                  'permit_deny': line_data_split[1],
                                  'protocol': line_data_split[2]})

            else:
                temp_dict.update({'sequence': line_data_split[0],
                                  'permit_deny': line_data_split[1],
                                  'protocol': line_data_split[2],
                                  'source_network': ' '.join(line_data_split[3:5]),
                                  'destination_network': ' '.join(line_data_split[5:7])})

            self.lines.append(temp_dict)

        elif line_data_split[2] != 'ip':
            if 'eq' or 'range' in line_data:
                if line_data.count('eq') == 2:
                    pass
                elif line_data.count('eq') == 1:
                    pass
                elif line_data.count('range') == 2:
                    pass
                elif line_data.count('range') == 1:
                    pass

            else:
                self.lines.append({'sequence': line_data_split[0],
                                   'permit_deny': line_data_split[1],
                                   'protocol': line_data_split[2],
                                   'source_network': ' '.join(line_data_split[3:5]),
                                   'destination_network': ' '.join(line_data_split[5:7])})

        else:
            self.lines.append({'sequence': line_data_split[0],
                               'permit_deny': line_data_split[1],
                               'protocol': line_data_split[2]})

    def get_name(self):
        return self.name

    def get_acl_type(self):
        return self.acl_type

    def get_lines(self):
        return self.lines


def convert_acl_to_our_format(directories=None, input_file_name=None, output_file_name=None, display_only=False,
                              reset_sequences=False):
    """
    Function to convert a ACL to a YML format for QuickConfigTemplates
    :param directories:
    :param input_file_name: The input file name
    :param output_file_name: The output file name
    :param display_only: Boolean true = don't output to file
    :param reset_sequences: Set True to recount sequences
    :return:
        None

    """
    temp_list = list()
    acl_obj = None

    try:
        acls = pdt.file_to_list(input_file_name, directories.get_yml_dir(input_file_name))
        acls = clean_list(acls)

        if len(acls) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(input_file_name),
                                                                   input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for line in acls:
        line_split = line.split()
        if directories.get_logging_level() == logging.DEBUG:
            print(line_split)

        if line_split[0] == 'ip':
            try:
                if line_split[2] == 'standard':
                    acl_obj = StandardAclData(line_split[3], reset_sequences)

                elif line_split[2] == 'extended':
                    acl_obj = ExtendedAclData(line_split[3], reset_sequences)

            except IndexError:
                error = 'Cannot find ACL name in this statement "{}"'.format(line)
                LOGGER.error(error)
                sys.exit(error)

        elif line_split[0] == 'permit' or line_split[0] == 'deny':
            if acl_obj:
                acl_obj.set_lines(line)

            else:
                error = 'Cannot find ACL Object'
                LOGGER.error(error)
                sys.exit(error)

        else:
            if acl_obj:
                acl_obj.set_lines(line)

            else:
                error = 'Cannot find ACL Object'
                LOGGER.error(error)
                sys.exit(error)

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

    elif acl_obj.get_acl_type() == 'extended':
        temp_list.append('            extended_acls:')
        temp_list.append('            -   acl_name: {}'.format(acl_obj.get_name()))
        temp_list.append('                sequences:')
        for line_data in acl_obj.get_lines():
            temp_list.append('                -   sequence: {}'.format(line_data.get('sequence')))
            temp_list.append('                    permit_deny: {}'.format(line_data.get('permit_deny')))
            temp_list.append('                    protocol: {}'.format(line_data.get('protocol')))
            temp_list.append('                    source_network: {}'.format(line_data.get('source_network')))
            temp_list.append('                    destination_network: {}'.format(line_data.get('destination_network')))
    """
--- # Test data to for ios
common:
    template: ios_base.jinja2
    ticket_number: CHG123456789
    devices:
    -   device:
        -   devicename: IOS-RTR02
            management_ip: 10.99.222.23
            extended_acls:
            -   acl_name: ACL-EXT-1
                sequences:
                -   destination_network: 192.168.5.0 0.0.0.255
                    permit_deny: permit
                    protocol: ip
                    sequence: 10
                    source_network: 192.168.1.0 0.0.0.255

                -   destination_network: 192.168.6.0 0.0.0.255
                    destination_port: 445
                    permit_deny: permit
                    protocol: tcp
                    sequence: 20
                    source_network: 192.168.4.0 0.0.0.255

                -   destination_network: 192.168.6.0 0.0.0.255
                    destination_port_range: 445 600
                    permit_deny: permit
                    protocol: tcp
                    sequence: 30
                    source_network: 192.168.4.0 0.0.0.255

                -   destination_network: 192.168.6.0 0.0.0.255
                    permit_deny: permit
                    protocol: tcp
                    sequence: 40
                    source_network: 192.168.4.0 0.0.0.255
                    source_port_range: 445 600
    """

    if not display_only:
        file_name = pdt.file_name_increase(output_file_name, directories.get_output_dir())
        pdt.list_to_file(temp_list, file_name, directories.get_output_dir())
        output_notify = 'Filename: {} output to directory {}'.format(file_name, directories.get_output_dir())
        print(output_notify)
        LOGGER.debug(output_notify)

    for final_yml in temp_list:
        print(final_yml)

    if directories.get_logging_level() == logging.DEBUG:
        print(acl_obj)
        for line in acl_obj.get_lines():
            print(line)
