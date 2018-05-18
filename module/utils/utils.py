import logging
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2018 Ben Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = 'MIT'
__status__ = 'prod'
__version_info__ = (1, 0, 0, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

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
