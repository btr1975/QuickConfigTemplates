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


def convert_route_map_to_our_format(directories=None, input_file_name=None, output_file_name=None, display_only=False):
    temp_list = list()
    dict_of_route_maps = dict()

    print(directories)
    print(input_file_name)
    print(output_file_name)
    print(display_only)

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
        print(rm_line_split)

        if rm_line_split[0] == 'route-map':
            try:
                if not dict_of_route_maps.get(rm_line_split[1]):
                    dict_of_route_maps[rm_line_split[1]] = list()
                    current_rmap_name = rm_line_split[1]
                    current_rmap_seq = rm_line_split[3]
                    dict_current_seq = {current_rmap_seq: dict()}
                    dict_current_seq.get(current_rmap_seq).update({'permit_deny': rm_line_split[2]})

                else:
                    current_rmap_name = rm_line_split[1]
                    current_rmap_seq = rm_line_split[3]
                    dict_current_seq = {current_rmap_seq: dict()}
                    dict_current_seq.get(current_rmap_seq).update({'permit_deny': rm_line_split[2]})

            except IndexError:
                error = 'Cannot find Route-Map name in this statement "{}"'.format(rm_line)
                LOGGER.error(error)
                print(error)
                critical_issue = True

        elif rm_line_split[0] == 'description':
            dict_current_seq.get(current_rmap_seq).update({'description': ' '.join(rm_line_split[1:])})

        elif rm_line_split[0] == 'match':
            dict_current_seq.get(current_rmap_seq).update({'match': list()})

        elif rm_line_split[0] == 'set':
            dict_current_seq.get(current_rmap_seq).update({'set': list()})

            dict_of_route_maps.get(current_rmap_name).append(dict_current_seq)

    temp_list.append('--- # Created from file: {} with rm_create'.format(input_file_name))
    temp_list.append('common:')
    temp_list.append('    template: <replace>')
    temp_list.append('    devices:')
    temp_list.append('    -   device:')
    temp_list.append('        -   devicename: <replace>')
    temp_list.append('            management_ip: <replace>')
    temp_list.append('            route_maps:')



    """
--- # Test data to for ios
common:
    template: ios_base.jinja2
    ticket_number: CHG123456789
    devices:
    -   device:
        -   devicename: IOS-RTR01
            management_ip: 10.99.222.22
            route_maps:
            -   route_map_name: RM-TEST-1
                sequences:
                -   description: test description
                    match:
                    -   match_item: access-list
                        match_item_name: ACL-A-in
                    -   match_item: access-list
                        match_item_name: ACL-B-in
                    permit_deny: permit
                    sequence: 10
                    set:
                    -   set_item: local preference
                        set_item_to: 200

                -   description: test description
                    match:
                    -   match_item: ip address prefix-list
                        match_item_name: PL-TEST-1
                    permit_deny: deny
                    sequence: 20
                    set:
                    -   set_item: local preference
                        set_item_to: 500

                -   match:
                    -   match_item: access-list
                        match_item_name: ACL-C-in
                    permit_deny: permit
                    sequence: 30
                    set:
                    -   set_item: local preference
                        set_item_to: 200

Notes:

match_item options

ip address prefix-list
as-path
ip address
community
extcommunity

set_item options

local-preference
weight
community
as-path prepend
as-path prepend last-as
    
    """

    for thing in temp_list:
        print(thing)

    print(dict_of_route_maps)