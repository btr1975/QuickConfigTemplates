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


class RouteMapData(object):

    def __init__(self, name):
        self.name = name
        self.lines = list()
        self.temp_dict = dict()

    def __str__(self):
        return 'RouteMapData: Route-Map {}'.format(self.name)

    def __repr__(self):
        return 'RouteMapData: Route-Map {}'.format(self.name)

    def set_sequence_info(self, sequence, permit_deny):
        self.temp_dict.update({'sequence': sequence})
        self.temp_dict.update({'permit_deny': permit_deny})
        self.temp_dict.update({'description': None})
        self.temp_dict.update({'match': list()})
        self.temp_dict.update({'set': list()})

    def set_description(self, line_data):
        line_data_split = line_data.split()
        self.temp_dict['description'] = ' '.join(line_data_split[1:])

    def set_matches(self, line_data):
        line_data_split = line_data.split()
        if 'prefix-list' in line_data_split:
            self.temp_dict['match'].append({'match_item': ' '.join(line_data_split[1:4]),
                                            'match_item_name': line_data_split[4]})

        elif 'address' in line_data_split:
            self.temp_dict['match'].append({'match_item': ' '.join(line_data_split[1:3]),
                                            'match_item_name': line_data_split[3]})

        else:
            self.temp_dict['match'].append({'match_item': line_data_split[1], 'match_item_name': line_data_split[2]})

    def set_sets(self, line_data):
        line_data_split = line_data.split()
        if 'as-path' in line_data_split:
            if 'last-as' in line_data_split:
                self.temp_dict['set'].append({'set_item': ' '.join(line_data_split[1:4]),
                                              'set_item_name': line_data_split[4]})

            else:
                self.temp_dict['set'].append({'set_item': ' '.join(line_data_split[1:3]),
                                              'set_item_name': line_data_split[3]})

        else:
            self.temp_dict['set'].append({'set_item': line_data_split[1], 'set_item_name': line_data_split[2]})

    def get_name(self):
        return self.name

    def get_current_sequence(self):
        return self.temp_dict.get('sequence')

    def get_temp_dict(self):
        return self.temp_dict

    def set_new_sequence(self):
        self.lines.append(self.temp_dict.copy())
        self.temp_dict.clear()

    def get_sequences(self):
        return self.lines


def convert_route_map_to_our_format(directories=None, input_file_name=None, output_file_name=None, display_only=False):
    temp_list = list()
    rmap_obj = None

    try:
        route_maps = pdt.file_to_list(input_file_name, directories.get_yml_dir())
        route_maps = clean_list(route_maps)

        if len(route_maps) == 0:
            error = 'No data found in file {}'.format(os.path.join(directories.get_yml_dir(), input_file_name))
            LOGGER.critical(error)
            sys.exit(error)

    except FileNotFoundError as e:
        error = '{error}'.format(error=e)
        LOGGER.critical(error)
        sys.exit(error)

    for rm_line in route_maps:
        rm_line_split =  pdt.remove_extra_spaces(rm_line).split()

        if rm_line_split[0] == 'route-map':
            try:
                if not rmap_obj:
                    rmap_obj = RouteMapData(rm_line_split[1])
                    rmap_obj.set_sequence_info(rm_line_split[3], rm_line_split[2])

                elif rmap_obj:
                    rmap_obj.set_new_sequence()
                    rmap_obj.set_sequence_info(rm_line_split[3], rm_line_split[2])

            except IndexError:
                error = 'Cannot find Route-Map name in this statement "{}"'.format(rm_line)
                LOGGER.error(error)
                print(error)
                critical_issue = True

        elif rm_line_split[0] == 'description':
            rmap_obj.set_description(rm_line)

        elif rm_line_split[0] == 'match':
            rmap_obj.set_matches(rm_line)

        elif rm_line_split[0] == 'set':
            rmap_obj.set_sets(rm_line)

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
            for enum, match_line in enumerate(line.get('match')):
                if enum == 0:
                    temp_list.append('                    -   match_item: {}'.format(match_line.get('match_item')))

                else:
                    temp_list.append('                        match_item: {}'.format(match_line.get('match_item')))
                temp_list.append('                        match_item_name: {}'.format(match_line.get('match_item_name')))

        if line.get('set'):
            temp_list.append('                    set:')
            for enum, set_line in enumerate(line.get('set')):
                if enum == 0:
                    temp_list.append('                    -   set_item: {}'.format(set_line.get('set_item')))

                else:
                    temp_list.append('                        set_item: {}'.format(set_line.get('set_item')))

                temp_list.append('                        set_item_name: {}'.format(set_line.get('set_item_name')))

    for thing in temp_list:
        print(thing)
