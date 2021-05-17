"""
Some utilities
"""
import logging

LOGGER = logging.getLogger(__name__)


def clean_list(pre_list):
    """
    Function delete blank lines from a list
    :param pre_list: A list made from a file
    :return:
        A Cleaned List

    """
    post_list = list()
    for line in pre_list:
        if len(line) > 0:
            post_list.append(line)

    return post_list
