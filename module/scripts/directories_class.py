import logging
import os
from yaml import safe_load
import module as mod
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 0, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class Directories(object):
    """
    Class to hold directory structure
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_dir = os.path.join(self.base_dir, 'Data')
        mod.pdt.verify_directory('Data', self.base_dir, directory_create=True)
        self.yml_config_data = open(os.path.join(self.data_dir, 'config.yml'))
        self.dir_config = safe_load(self.yml_config_data).get('config')
        self.templates_dir = list()

        # This sets the location of the yml input directory
        if self.dir_config.get('yml_directory'):
            self.yml_dir = self.dir_config.get('yml_directory')
            if not os.path.isdir(self.yml_dir):
                LOGGER.critical('Could not find yml directory stated in config file {}'.format(self.yml_dir))
                exit('Bad yml directory {}'.format(self.yml_dir))

        else:
            self.yml_dir = os.path.join(self.base_dir, 'yaml')
            mod.pdt.verify_directory('yaml', self.base_dir, directory_create=True)

        # This sets the default directory for templates, and adds extra directories for templates
        self.templates_dir.append(os.path.join(self.base_dir, 'templates'))
        if self.dir_config.get('templates_directory'):
            if isinstance(self.dir_config.get('templates_directory'), list):
                self.templates_dir += self.dir_config.get('templates_directory')

            else:
                self.templates_dir.append(self.dir_config.get('templates_directory'))

            for directory in self.templates_dir:
                if not os.path.isdir(directory):
                    LOGGER.critical('Could not find templates in directory stated in config file {}'.format(directory))
                    exit('Bad templates directory {}'.format(directory))

        else:
            mod.pdt.verify_directory('templates', self.base_dir, directory_create=True)

        # This sets the location of the output directory
        if self.dir_config.get('output_directory'):
            self.output_dir = self.dir_config.get('output_directory')
            if not os.path.isdir(self.output_dir):
                LOGGER.critical('Could not find output directory stated in config file {}'.format(self.output_dir))
                exit('Bad output directory {}'.format(self.output_dir))

        else:
            self.output_dir = os.path.join(self.base_dir, 'Output')
            mod.pdt.verify_directory('Output', self.base_dir, directory_create=True)

        # This sets the logging directory
        if self.dir_config.get('logging_directory'):
            self.logging_dir = self.dir_config.get('logging_directory')
            if not os.path.isdir(self.logging_dir):
                LOGGER.critical('Could not find logging directory stated in config file {}'.format(self.logging_dir))
                exit('Bad logging directory {}'.format(self.logging_dir))

        else:
            self.logging_dir = os.path.join(self.base_dir, 'Logs')
            mod.pdt.verify_directory('Logs', self.base_dir, directory_create=True)

        # This sets the logging level
        if self.dir_config.get('logging_level'):
            self.set_logging_level(self.dir_config.get('logging_level'))

        else:
            self.logging_level = logging.WARNING

    def set_logging_level(self, level):
        if str(level) == '1':
            self.logging_level = logging.DEBUG
        elif str(level) == '2':
            self.logging_level = logging.INFO
        elif str(level) == '3':
            self.logging_level = logging.WARNING
        elif str(level) == '4':
            self.logging_level = logging.ERROR
        elif str(level) == '5':
            self.logging_level = logging.CRITICAL

    def get_logging_level(self):
        return self.logging_level

    def set_output_dir_folder(self, output_folder):
        mod.pdt.verify_directory(output_folder, self.output_dir, directory_create=True)
        self.output_dir = os.path.join(self.output_dir, output_folder)

    def get_output_dir(self):
        return self.output_dir

    def get_yml_dir(self):
        return self.yml_dir

    def get_templates_dir(self):
        return self.templates_dir
