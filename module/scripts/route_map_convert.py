"""
Route-Map conversion
"""
import logging
import sys
import os
import persistentdatatools as pdt
from ..utils import clean_list


LOGGER = logging.getLogger(__name__)


class RouteMapData:
    """Class to hold 1 Route-Map Data

    :type name: String
    :param name: The ACL name
    :type reset_sequences: Boolean
    :param reset_sequences: Reset ACL sequences default: False

    """
    def __init__(self, name, reset_sequences=False):
        self.name = name
        self.reset_sequences = reset_sequences
        self.current_seq = 10
        self.lines = list()
        self.temp_dict = dict()

    def __str__(self):
        return 'RouteMapData: Route-Map {}'.format(self.name)

    def __repr__(self):
        return 'RouteMapData: Route-Map {}'.format(self.name)

    def set_sequence_info(self, sequence, permit_deny):
        """Method to create a single sequences dictionary

        :type sequence: Integer
        :param sequence: The sequence number
        :type permit_deny: String
        :param permit_deny: permit, or deny

        :rtype: None
        :return:  None
        """
        if self.reset_sequences:
            self.temp_dict.update({'sequence': self.current_seq})
            self.current_seq += 10
        else:
            self.temp_dict.update({'sequence': sequence})
        self.temp_dict.update({'permit_deny': permit_deny})
        self.temp_dict.update({'description': None})
        self.temp_dict.update({'match': list()})
        self.temp_dict.update({'set': list()})

    def set_description(self, line_data):
        """Method to set the sequences description

        :type: String
        :param line_data: String data

        :rtype: None
        :return: None
        """
        line_data_split = line_data.split()
        self.temp_dict['description'] = ' '.join(line_data_split[1:])

    def set_matches(self, line_data):
        """Method to add a match statement

        :type line_data: String
        :param line_data: String data

        :rtype: None
        :return: None
        """
        line_data_split = line_data.split()
        if 'address' in line_data_split:
            if 'prefix-list' in line_data_split:
                self.temp_dict['match'].append({'match_item': ' '.join(line_data_split[1:4]),
                                                'match_item_name': line_data_split[4]})

            else:
                self.temp_dict['match'].append({'match_item': ' '.join(line_data_split[1:3]),
                                                'match_item_name': line_data_split[3]})

        else:
            self.temp_dict['match'].append({'match_item': line_data_split[1], 'match_item_name': line_data_split[2]})

    def set_sets(self, line_data):
        """Method to add a set statement

        :type line_data: String
        :param line_data: String data

        :rtype: None
        :return: None
        """
        line_data_split = line_data.split()
        if 'as-path' in line_data_split:
            if 'last-as' in line_data_split:
                self.temp_dict['set'].append({'set_item': ' '.join(line_data_split[1:4]),
                                              'set_item_to': line_data_split[4]})

            else:
                self.temp_dict['set'].append({'set_item': ' '.join(line_data_split[1:3]),
                                              'set_item_to': line_data_split[3]})

        else:
            self.temp_dict['set'].append({'set_item': line_data_split[1], 'set_item_to': line_data_split[2]})

    def get_name(self):
        """Method to get the Route-Map name

        :rtype: String
        :returns: The Route-Map name
        """
        return self.name

    def get_current_sequence(self):
        """Method to get the Route-Map's current sequence

        :rtype: Integer
        :return: Integer
        """
        return self.temp_dict.get('sequence')

    def set_new_sequence(self):
        """Method to create a new Route-Map sequence

        :rtype: None
        :return: None
        """
        self.lines.append(self.temp_dict.copy())
        self.temp_dict.clear()

    def get_sequences(self):
        """Method to get a Route-Map's sequences

        :rtype: List
        :return: List of dictionaries
        """
        return self.lines


def convert_route_map_to_our_format(directories=None, input_file_name=None,  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
                                    output_file_name=None, display_only=False, reset_sequences=False):
    """
    Function to convert a Route-Map to a YML format for QuickConfigTemplates
    :param directories:
    :param input_file_name: The input file name
    :param output_file_name: The output file name
    :param display_only: Boolean true = don't output to file
    :param reset_sequences: Set True to recount sequences
    :return:
        None

    """
    temp_list = list()
    rmap_obj = None

    try:
        route_maps = pdt.file_to_list(input_file_name, directories.get_yml_dir(input_file_name))
        route_maps = clean_list(route_maps)

        if len(route_maps) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(input_file_name),
                                                                   input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:  # pylint: disable=invalid-name
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for rm_line in route_maps:
        rm_line_split = pdt.remove_extra_spaces(rm_line).split()

        if rm_line_split[0] == 'route-map':
            try:
                if not rmap_obj:
                    rmap_obj = RouteMapData(rm_line_split[1], reset_sequences)
                    rmap_obj.set_sequence_info(rm_line_split[3], rm_line_split[2])

                elif rmap_obj:
                    rmap_obj.set_new_sequence()
                    rmap_obj.set_sequence_info(rm_line_split[3], rm_line_split[2])

            except IndexError:
                error = 'Cannot find Route-Map name in this statement "{}"'.format(rm_line)
                LOGGER.error(error)
                print(error)
                error = 'Your data in file {} does not all seem to be a ' \
                        'Route-Map'.format(os.path.join(directories.get_yml_dir(input_file_name), input_file_name))
                LOGGER.critical(error)
                sys.exit(error)

        elif rm_line_split[0] == 'description':
            rmap_obj.set_description(rm_line)

        elif rm_line_split[0] == 'match':
            rmap_obj.set_matches(rm_line)

        elif rm_line_split[0] == 'set':
            rmap_obj.set_sets(rm_line)

    if not rmap_obj:
        error = 'Your data in file {} does not all seem to be a ' \
                'Route-Map'.format(os.path.join(directories.get_yml_dir(input_file_name), input_file_name))
        LOGGER.critical(error)
        sys.exit(error)

    else:
        rmap_obj.set_new_sequence()

    temp_list.append('--- # Created from file: {} with rm_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')
    temp_list.append('            route_maps:')
    temp_list.append('            -   route_map_name: {}'.format(rmap_obj.get_name()))
    temp_list.append('                sequences:')
    for line in rmap_obj.get_sequences():
        temp_list.append('                -   sequence: {}'.format(line.get('sequence')))
        if line.get('description'):
            temp_list.append('                    description: {}'.format(line.get('description')))
        temp_list.append('                    permit_deny: {}'.format(line.get('permit_deny')))
        if line.get('match'):
            temp_list.append('                    match:')
            for enum, match_line in enumerate(line.get('match')):  # pylint: disable=unused-variable
                temp_list.append('                    -   match_item: {}'.format(match_line.get('match_item')))
                temp_list.append('                        match_item_name: '
                                 '{}'.format(match_line.get('match_item_name')))

        if line.get('set'):
            temp_list.append('                    set:')
            for enum, set_line in enumerate(line.get('set')):
                temp_list.append('                    -   set_item: {}'.format(set_line.get('set_item')))
                temp_list.append('                        set_item_to: {}'.format(set_line.get('set_item_to')))

    if not display_only:
        file_name = pdt.file_name_increase(output_file_name, directories.get_output_dir())
        pdt.list_to_file(temp_list, file_name, directories.get_output_dir())
        output_notify = 'Filename: {} output to directory {}'.format(file_name, directories.get_output_dir())
        print(output_notify)
        LOGGER.debug(output_notify)

    for final_yml in temp_list:
        print(final_yml)
