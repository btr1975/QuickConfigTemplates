import ipaddresstools as ipv4
import re
import logging
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'prod'
__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'


J2_FILTER_LOGGER = logging.getLogger('qct_template_filter')


def filter_check_u_ip_address(value):
    """
    Function to check for a unicast ipv4 address in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a unicast ipv4 address !!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_u_ip_address {}'.format(error))
        return error

    elif ipv4.ucast_ip(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_u_ip_address {}'.format(error))
        return error


def filter_check_subnet(value):
    """
    Function to check for a subnet and mask combo in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a ipv4 subnet !!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_subnet {}'.format(error))
        return error

    elif ipv4.ip_mask(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_subnet {}'.format(error))
        return error


def filter_check_ip_mask_cidr(value):
    """
    Function to check to a CIDR mask number in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a ipv4 subnet mask in CIDR!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_ip_mask_cidr {}'.format(error))
        return error

    try:
        if ipv4.mask_conversion.get(int(value)):
            return value

        else:
            return error

    except ValueError as e:
        J2_FILTER_LOGGER.info('filter_check_ip_mask_cidr {} {}'.format(error, e))
        return error


def filter_check_ip_mask_standard(value):
    """
    Function to check for a standard mask in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a ipv4 standard subnet mask!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_ip_mask_standard {}'.format(error))
        return error

    else:
        not_found = False
        for key in ipv4.mask_conversion:
            if ipv4.mask_conversion.get(key).get('MASK') == value:
                return value

            else:
                not_found = True

        if not_found:
            J2_FILTER_LOGGER.info('filter_check_ip_mask_standard {}'.format(error))
            return error


def filter_check_vlan_number(value):
    """
    Function to check for a good VLAN number in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error the VLAN# should be between 1 and 4096!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_vlan_number {}'.format(error))
        return error

    else:
        try:
            if int(value) not in range(1, 4097):
                return error

            else:
                return value

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_check_vlan_number {}, caught {}'.format(error, e))
            return error


def filter_check_vni_number(value):
    """
    Function to check for a good VNI number in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error the VNI# should be between 1 and 16777214!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_vni_number {}'.format(error))
        return error

    else:
        try:
            if int(value) not in range(1, 16777215):
                return error

            else:
                return value

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_check_vni_number {}, caught {}'.format(error, e))
            return error


def filter_check_ip_inverse_mask_standard(value):
    """
    Function to check for a inverse mask in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a ipv4 inverse subnet mask!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_ip_inverse_mask_standard {}'.format(error))
        return error

    else:
        not_found = False
        for key in ipv4.mask_conversion:
            if ipv4.mask_conversion.get(key).get('INVMASK') == value:
                return value

            else:
                not_found = True

        if not_found:
            J2_FILTER_LOGGER.info('filter_check_ip_inverse_mask_standard {}'.format(error))
            return error


def filter_check_m_ip_address(value):
    """
    Function to check for a multicast ipv4 address in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this is required to be a multicast ipv4 address !!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_m_ip_address {}'.format(error))
        return error

    elif ipv4.mcast_ip(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_m_ip_address {}'.format(error))
        return error


def filter_check_as_number(value):
    """
    Function to check for a good BGP AS, EIGRP AS, OSPF Process in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error the AS# should be between 1 and 65535!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_as_number {}'.format(error))
        return error

    else:
        try:
            if int(value) not in range(1, 65536):
                J2_FILTER_LOGGER.info('filter_check_as_number {}'.format(error))
                return error

            else:
                return value

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_check_as_number {}, caught {}'.format(error, e))
            return error


def filter_check_required(value):
    """
    Function to check for a required value in a template
    :param value:
    :return:
    """
    error = '{value} !!!! This is a required value!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_required {}'.format(error))
        return error

    else:
        return value


def filter_check_community(value):
    """
    Function to check for a community in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error the community should be in this format XXX:XXX!!!!'.format(value=value)
    regex_community = re.compile(r'^[0-9]+:[0-9]+$')
    if not value:
        J2_FILTER_LOGGER.info('filter_check_community {}'.format(error))
        return error

    elif not regex_community.match(str(value)):
        J2_FILTER_LOGGER.info('filter_check_community {}'.format(error))
        return error

    else:
        return value


def filter_check_mac_address(value):
    """
    Function to check for a mac-address in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error the mac-address should be in this format ' \
            'xxxx.xxxx.xxxx, and only contain 0-9 or a-f!!!!'.format(value=value)
    regex_mac = re.compile(r'^([0-9]|[a-f]){4}\.([0-9]|[a-f]){4}\.([0-9]|[a-f]){4}$', re.IGNORECASE)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_mac_address {}'.format(error))
        return error

    elif not regex_mac.match(str(value)):
        J2_FILTER_LOGGER.info('filter_check_mac_address {}'.format(error))
        return error

    else:
        return value


def filter_check_permit_or_deny(value):
    """
    Function to check for permit, or deny in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error should be permit or deny!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_permit_or_deny {}'.format(error))
        return error

    elif value not in ('permit', 'deny'):
        J2_FILTER_LOGGER.info('filter_check_permit_or_deny {}'.format(error))
        return error

    else:
        return value


def filter_check_inside_or_outside(value):
    """
    Function to check for inside, or outside in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error should be inside or outside!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_inside_or_outside {}'.format(error))
        return error

    elif value not in ('inside', 'outside'):
        J2_FILTER_LOGGER.info('filter_check_inside_or_outside {}'.format(error))
        return error

    else:
        return value


def filter_check_number(value):
    """
    Function to check for any number in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error this should be any number!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_number {}'.format(error))
        return error

    try:
        if isinstance(int(value), int):
            return value

    except ValueError as e:
        J2_FILTER_LOGGER.info('filter_check_number {}, caught {}'.format(error, e))
        return error


def filter_check_route_map_match_items(value):
    """
    Function to check route-map match options in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error check template for possible match items!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_route_map_match_items {}'.format(error))
        return error

    elif value not in ('ip address prefix-list', 'as-path', 'ip address', 'community', 'extcommunity',
                       'ip multicast group'):
        J2_FILTER_LOGGER.info('filter_check_route_map_match_items {}'.format(error))
        return error

    else:
        return value


def filter_check_route_map_set_items(value):
    """
    Function to check route-map set options in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error check template for possible set items!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_route_map_set_items {}'.format(error))
        return error

    elif value not in ('local-preference', 'weight', 'community', 'as-path prepend', 'as-path prepend last-as'):
        J2_FILTER_LOGGER.info('filter_check_route_map_set_items {}'.format(error))
        return error

    else:
        return value


def filter_check_protocol_port_number(value):
    """
    Function to check for a good protocol port number in a template
    :param value:
    :return:
    """
    error = '{value} !!!! possible error should be between 0 and 65535!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_check_protocol_port_number {}'.format(error))
        return error

    else:
        try:
            if int(value) not in range(0, 65536):
                J2_FILTER_LOGGER.info('filter_check_protocol_port_number {}'.format(error))
                return error

            else:
                return value

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_check_protocol_port_number {}, caught {}'.format(error, e))
            return error


def filter_calculate_neighbor_ip_mask_30(value):
    """
    Function to calculate a neighbors IP using a 30 bit mask
    :param value:
    :return: An error, or a IP address
    """
    error = '{value} !!!! possible error should be a valid ipv4 address!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 {}'.format(error))
        return error

    else:
        try:
            if ipv4.ip(value, return_tuple=False):
                this_ip, nei_ip = ipv4.get_neighbor_ip(value, '30')
                return nei_ip

            else:
                J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 {}'.format(error))
                return error

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 {}, caught {}'.format(error, e))
            return error


def filter_calculate_neighbor_ip_mask_31(value):
    """
    Function to calculate a neighbors IP using a 31 bit mask
    :param value:
    :return: An error, or a IP address
    """
    error = '{value} !!!! possible error should be a valid ipv4 address!!!!'.format(value=value)
    if not value:
        J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 {}'.format(error))
        return error

    else:
        try:
            if ipv4.ip(value, return_tuple=False):
                this_ip, nei_ip = ipv4.get_neighbor_ip(value, '31')
                return nei_ip

            else:
                J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 {}'.format(error))
                return error

        except ValueError as e:
            J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 {}, caught {}'.format(error, e))
            return error


custom_filters = {
    'u_ip_address': filter_check_u_ip_address,
    'm_ip_address': filter_check_m_ip_address,
    'subnet': filter_check_subnet,
    'mask_cidr': filter_check_ip_mask_cidr,
    'mask_standard': filter_check_ip_mask_standard,
    'mask_inv': filter_check_ip_inverse_mask_standard,
    'as_number': filter_check_as_number,
    'vlan': filter_check_vlan_number,
    'vni': filter_check_vni_number,
    'required': filter_check_required,
    'community': filter_check_community,
    'mac': filter_check_mac_address,
    'p_or_d': filter_check_permit_or_deny,
    'number': filter_check_number,
    'rmap_match_items': filter_check_route_map_match_items,
    'rmap_set_items': filter_check_route_map_set_items,
    'protocol_port': filter_check_protocol_port_number,
    'i_or_o': filter_check_inside_or_outside,
    'nei_ip_30': filter_calculate_neighbor_ip_mask_30,
    'nei_ip_31': filter_calculate_neighbor_ip_mask_31,
}
