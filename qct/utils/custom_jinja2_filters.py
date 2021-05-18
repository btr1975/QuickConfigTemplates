"""
Custom Jinja2 template filters
"""
import re
import logging
import ipaddresstools as ipv4

J2_FILTER_LOGGER = logging.getLogger('qct_template_filter')


def filter_check_u_ip_address(value):
    """Function to check for a unicast ipv4 address in a template

    :type value: String
    :param value: Value to check if it is a IPv4 Unicast address

    :rtype: String
    :returns: value, or an error
    """
    error = f'{value} !!!! possible error this is required to be a unicast ipv4 address !!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_u_ip_address %s', error)
        return error

    elif ipv4.ucast_ip(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_u_ip_address %s', error)
        return error


def filter_check_subnet(value):
    """Function to check for a subnet and mask combo in a template

    :type value: String
    :param value: Value to check if it is a IPv4 Subnet in CIDR format

    :rtype: String
    :returns: The value or an error
    """
    error = f'{value} !!!! possible error this is required to be a ipv4 subnet !!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_subnet %s', error)
        return error

    elif ipv4.ip_mask(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_subnet %s', error)
        return error


def filter_check_ip_mask_cidr(value):
    """Function to check to a CIDR mask number in a template

    :type value: String
    :param value: The value to check if it is a CIDR value

    :rtype: String
    :return: The value or an error
    """
    error = f'{value} !!!! possible error this is required to be a ipv4 subnet mask in CIDR!!!!'
    if not value:
        J2_FILTER_LOGGER.info('filter_check_ip_mask_cidr %s', error)
        return error

    try:
        if ipv4.mask_conversion.get(int(value)):  # pylint: disable=no-else-return
            return value

        else:
            return error

    except ValueError as e:  # pylint: disable=invalid-name  # pylint: disable=invalid-name
        J2_FILTER_LOGGER.info('filter_check_ip_mask_cidr %s %s', error, e)
        return error


def filter_check_ip_mask_standard(value):  # pylint: disable=inconsistent-return-statements
    """
    Function to check for a standard mask in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error this is required to be a ipv4 standard subnet mask!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_ip_mask_standard %s', error)
        return error

    else:
        not_found = False
        for key in ipv4.mask_conversion:
            if ipv4.mask_conversion.get(key).get('MASK') == value:  # pylint: disable=no-else-return
                return value

            else:
                not_found = True

        if not_found:
            J2_FILTER_LOGGER.info('filter_check_ip_mask_standard %s', error)
            return error


def filter_check_vlan_number(value):
    """
    Function to check for a good VLAN number in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error the VLAN# should be between 1 and 4096!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_vlan_number %s', error)
        return error

    else:
        try:
            if int(value) not in range(1, 4097):  # pylint: disable=no-else-return
                return error

            else:
                return value

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_check_vlan_number %s, caught %s', error, e)
            return error


def filter_check_vni_number(value):
    """
    Function to check for a good VNI number in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error the VNI# should be between 1 and 16777214!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_vni_number %s', error)
        return error

    else:
        try:
            if int(value) not in range(1, 16777215):  # pylint: disable=no-else-return
                return error

            else:
                return value

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_check_vni_number %s, caught %s', error, e)
            return error


def filter_check_ip_inverse_mask_standard(value):  # pylint: disable=inconsistent-return-statements
    """
    Function to check for a inverse mask in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error this is required to be a ipv4 inverse subnet mask!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_ip_inverse_mask_standard %s', error)
        return error

    else:
        not_found = False
        for key in ipv4.mask_conversion:
            if ipv4.mask_conversion.get(key).get('INVMASK') == value:  # pylint: disable=no-else-return
                return value

            else:
                not_found = True

        if not_found:
            J2_FILTER_LOGGER.info('filter_check_ip_inverse_mask_standard %s', error)
            return error


def filter_check_m_ip_address(value):
    """
    Function to check for a multicast ipv4 address in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error this is required to be a multicast ipv4 address !!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_m_ip_address %s', error)
        return error

    elif ipv4.mcast_ip(value, return_tuple=False):
        return value

    else:
        J2_FILTER_LOGGER.info('filter_check_m_ip_address %s', error)
        return error


def filter_check_as_number(value):
    """
    Function to check for a good BGP AS, EIGRP AS, OSPF Process in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error the AS# should be between 1 and 65535!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_as_number %s', error)
        return error

    else:
        try:
            if int(value) not in range(1, 65536):  # pylint: disable=no-else-return
                J2_FILTER_LOGGER.info('filter_check_as_number %s', error)
                return error

            else:
                return value

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_check_as_number %s, caught %s', error, e)
            return error


def filter_check_required(value):
    """
    Function to check for a required value in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! This is a required value!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_required %s', error)
        return error

    else:
        return value


def filter_check_community(value):
    """
    Function to check for a community in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error the community should be in this format XXX:XXX!!!!'
    regex_community = re.compile(r'^[0-9]+:[0-9]+$')
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_community %s', error)
        return error

    elif not regex_community.match(str(value)):
        J2_FILTER_LOGGER.info('filter_check_community %s', error)
        return error

    else:
        return value


def filter_check_mac_address(value):
    """
    Function to check for a mac-address in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error the mac-address should be in this format ' \
            f'xxxx.xxxx.xxxx, and only contain 0-9 or a-f!!!!'
    regex_mac = re.compile(r'^([0-9]|[a-f]){4}\.([0-9]|[a-f]){4}\.([0-9]|[a-f]){4}$', re.IGNORECASE)
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_mac_address %s', error)
        return error

    elif not regex_mac.match(str(value)):
        J2_FILTER_LOGGER.info('filter_check_mac_address %s', error)
        return error

    else:
        return value


def filter_check_permit_or_deny(value):
    """
    Function to check for permit, or deny in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error should be permit or deny!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_permit_or_deny %s', error)
        return error

    elif value not in ('permit', 'deny'):
        J2_FILTER_LOGGER.info('filter_check_permit_or_deny %s', error)
        return error

    else:
        return value


def filter_check_inside_or_outside(value):
    """
    Function to check for inside, or outside in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error should be inside or outside!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_inside_or_outside %s', error)
        return error

    elif value not in ('inside', 'outside'):
        J2_FILTER_LOGGER.info('filter_check_inside_or_outside %s', error)
        return error

    else:
        return value


def filter_check_number(value):  # pylint: disable=inconsistent-return-statements
    """
    Function to check for any number in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error this should be any number!!!!'
    if not value:
        J2_FILTER_LOGGER.info('filter_check_number %s', error)
        return error

    try:
        if isinstance(int(value), int):
            return value

    except ValueError as e:  # pylint: disable=invalid-name
        J2_FILTER_LOGGER.info('filter_check_number %s, caught %s', error, e)
        return error


def filter_check_route_map_match_items(value):
    """
    Function to check route-map match options in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error check template for possible match items!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_route_map_match_items %s', error)
        return error

    elif value not in ('ip address prefix-list', 'as-path', 'ip address', 'community', 'extcommunity',
                       'ip multicast group'):
        J2_FILTER_LOGGER.info('filter_check_route_map_match_items %s', error)
        return error

    else:
        return value


def filter_check_route_map_set_items(value):
    """
    Function to check route-map set options in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error check template for possible set items!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_route_map_set_items %s', error)
        return error

    elif value not in ('local-preference', 'weight', 'community', 'as-path prepend', 'as-path prepend last-as'):
        J2_FILTER_LOGGER.info('filter_check_route_map_set_items %s', error)
        return error

    else:
        return value


def filter_check_protocol_port_number(value):
    """
    Function to check for a good protocol port number in a template
    :param value:
    :return:
    """
    error = f'{value} !!!! possible error should be between 0 and 65535!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_check_protocol_port_number %s', error)
        return error

    else:
        try:
            if int(value) not in range(0, 65536):  # pylint: disable=no-else-return
                J2_FILTER_LOGGER.info('filter_check_protocol_port_number %s', error)
                return error

            else:
                return value

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_check_protocol_port_number %s, caught %s', error, e)
            return error


def filter_calculate_neighbor_ip_mask_30(value):
    """
    Function to calculate a neighbors IP using a 30 bit mask
    :param value:
    :return: An error, or a IP address
    """
    error = f'{value} !!!! possible error should be a valid ipv4 address!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 %s', error)
        return error

    else:
        try:
            if ipv4.ip(value, return_tuple=False):  # pylint: disable=no-else-return
                this_ip, nei_ip = ipv4.get_neighbor_ip(value, '30')  # pylint: disable=unused-variable
                return nei_ip

            else:
                J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 %s', error)
                return error

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_30 %s, caught %s', error, e)
            return error


def filter_calculate_neighbor_ip_mask_31(value):
    """
    Function to calculate a neighbors IP using a 31 bit mask
    :param value:
    :return: An error, or a IP address
    """
    error = f'{value} !!!! possible error should be a valid ipv4 address!!!!'
    if not value:  # pylint: disable=no-else-return
        J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 %s', error)
        return error

    else:
        try:
            if ipv4.ip(value, return_tuple=False):  # pylint: disable=no-else-return
                this_ip, nei_ip = ipv4.get_neighbor_ip(value, '31')  # pylint: disable=unused-variable
                return nei_ip

            else:
                J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 %s', error)
                return error

        except ValueError as e:  # pylint: disable=invalid-name
            J2_FILTER_LOGGER.info('filter_calculate_neighbor_ip_mask_31 %s, caught %s', error, e)
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
