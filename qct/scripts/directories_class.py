"""
Code to deal with directories
"""
import logging
import os
import sys
import zipfile
import persistentdatatools as pdt
from yaml import safe_load


LOGGER = logging.getLogger(__name__)


class Directories:  # pylint: disable=too-many-instance-attributes
    """Class to hold directory structure

    :type base_dir: String
    :param base_dir: The base level directory
    """
    def __init__(self, base_dir):  # pylint: disable=too-many-branches,too-many-statements
        self.base_dir = base_dir
        self.data_dir = os.path.join(self.base_dir, 'Data')
        pdt.verify_directory('Data', self.base_dir, directory_create=True)
        with open(os.path.join(self.data_dir, 'config.yml'), 'r') as file:
            self.yml_config_data = file.read()

        self.dir_config = safe_load(self.yml_config_data).get('config')
        self.templates_dir = list()
        self.yml_dir = list()

        # This sets the location of the yml input directory
        self.yml_dir.append(os.path.join(self.base_dir, 'yaml'))
        if self.dir_config.get('yml_directory'):
            if isinstance(self.dir_config.get('yml_directory'), list):
                self.yml_dir += self.dir_config.get('yml_directory')

            else:
                self.yml_dir.append(self.dir_config.get('yml_directory'))

            for directory in self.yml_dir:
                if not os.path.isdir(directory):
                    LOGGER.critical('Could not find yml directory stated in config file %s', directory)
                    sys.exit('Bad yml directory {}'.format(directory))

        else:
            pdt.verify_directory('yaml', self.base_dir, directory_create=True)

        # This sets the default directory for templates, and adds extra directories for templates
        self.templates_dir.append(os.path.join(self.base_dir, 'templates'))
        if self.dir_config.get('templates_directory'):
            if isinstance(self.dir_config.get('templates_directory'), list):
                self.templates_dir += self.dir_config.get('templates_directory')

            else:
                self.templates_dir.append(self.dir_config.get('templates_directory'))

            for directory in self.templates_dir:
                if not os.path.isdir(directory):
                    LOGGER.critical('Could not find templates in directory stated in config file %s', directory)
                    sys.exit('Bad templates directory {}'.format(directory))

        else:
            pdt.verify_directory('templates', self.base_dir, directory_create=True)

        # This sets the location of the output directory
        if self.dir_config.get('output_directory'):
            self.output_dir = self.dir_config.get('output_directory')
            if not os.path.isdir(self.output_dir):
                LOGGER.critical('Could not find output directory stated in config file %s', self.output_dir)
                sys.exit('Bad output directory {}'.format(self.output_dir))

        else:
            self.output_dir = os.path.join(self.base_dir, 'Output')
            pdt.verify_directory('Output', self.base_dir, directory_create=True)

        # This sets the logging directory
        if self.dir_config.get('logging_directory'):
            self.logging_dir = self.dir_config.get('logging_directory')
            if not os.path.isdir(self.logging_dir):
                LOGGER.critical('Could not find logging directory stated in config file %s', self.logging_dir)
                sys.exit('Bad logging directory {}'.format(self.logging_dir))

        else:
            self.logging_dir = os.path.join(self.base_dir, 'Logs')
            pdt.verify_directory('Logs', self.base_dir, directory_create=True)

        # This sets the logging level
        if self.dir_config.get('logging_level'):
            self.set_logging_level(self.dir_config.get('logging_level'))

        else:
            self.logging_level = logging.WARNING

    def set_logging_level(self, level):
        """Method to set the logging level

        :type level: Integer
        :param level: The logging level

        :rtype: None
        :returns: Nonr
        """
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
        """Method to get current logging level

        :rtype: Integer
        :returns: The logging level
        """
        return self.logging_level

    def set_output_dir_folder(self, output_folder):
        """Method to set the output directory

        :type output_folder: String
        :param output_folder: The folder to output to

        :rtype: None
        :returns: None
        """
        pdt.verify_directory(output_folder, self.output_dir, directory_create=True)
        self.output_dir = os.path.join(self.output_dir, output_folder)

    def get_output_dir(self):
        """Method to get the output directory

        :rtype: String
        :returns: The output directory
        """
        return self.output_dir

    def get_yml_dir(self, file_name):
        """Method to get file path

        :type file_name: String
        :param file_name: The filename to look for

        :rtype: String
        :returns: The directory where the file is located
        """
        for yml_dir in self.yml_dir:
            if os.path.isfile(os.path.join(yml_dir, file_name)):
                return yml_dir

        error = 'File name {} not found in any directory in {}'.format(file_name, self.yml_dir)
        raise FileNotFoundError(error)

    def get_templates_dir(self):
        """Method to get the templates directory

        :rtype: String
        :returns: The templates directory
        """
        return self.templates_dir

    def get_data_dir(self):
        """Method to get the data directory

        :rtype: String
        :returns: The data directory
        """
        return self.data_dir

    def get_logging_dir(self):
        """Method to get the logging directory

        :rtype: String
        :returns: The logging directory
        """
        return self.logging_dir

    def collect_and_zip_files(self, dir_list, zip_file_name, file_extension_list=None,  # pylint: disable=too-many-locals,too-many-branches
                              file_name_list=None):
        """
        Method to collect files and make a zip file
        :param dir_list: A list of directories
        :param zip_file_name: Zip file name
        :param file_extension_list: A list of extensions of files to find
        :param file_name_list: A list of file names to find
        :return:
            Outputs a zip file

        """
        temp_list = list()

        if isinstance(dir_list, list):
            for dir_name in dir_list:
                if not os.path.isdir(dir_name):
                    raise Exception('NOT DIR')

        else:
            error = 'Method collect_and_zip_files from class {} expected dir_list to be a ' \
                    'list but received a {}'.format(type(self), type(dir_list))
            LOGGER.critical(error)
            raise TypeError(error)

        if not file_extension_list and not file_name_list:
            for dir_name in dir_list:
                temp_files_list = pdt.list_files_in_directory(dir_name)
                for file_name in temp_files_list:
                    temp_list.append(os.path.join(dir_name, file_name))

        if file_extension_list:
            if isinstance(file_extension_list, list):
                for dir_name in dir_list:
                    temp_files_list = pdt.list_files_in_directory(dir_name)
                    for file_name in temp_files_list:
                        garbage, extension = file_name.split('.')  # pylint: disable=unused-variable
                        if extension in file_extension_list:
                            temp_list.append(os.path.join(dir_name, file_name))

            else:
                error = 'Method collect_and_zip_files from class {} expected file_extension_list to be a ' \
                        'list but received a {}'.format(type(self), type(file_extension_list))
                LOGGER.critical(error)
                raise TypeError(error)

        if file_name_list:
            if isinstance(file_name_list, list):
                for dir_name in dir_list:
                    temp_files_list = pdt.list_files_in_directory(dir_name)
                    for file_name in temp_files_list:
                        if file_name in file_name_list:
                            temp_list.append(os.path.join(dir_name, file_name))

            else:
                error = 'Method collect_and_zip_files from class {} expected file_name_list to be a ' \
                        'list but received a {}'.format(type(self), type(file_name_list))
                LOGGER.critical(error)
                raise TypeError(error)

        if len(zip_file_name.split('.')) == 2:
            name, ext = zip_file_name.split('.')
            if ext != 'zip':
                LOGGER.warning('Changed the extension of zip_file_name=%s to be zip', zip_file_name)
                zip_file_name = '{}.{}'.format(name, 'zip')

        else:
            error = 'Method collect_and_zip_files from class {} expected zip_file_name to only contain one . ' \
                    'but received {}'.format(type(self), zip_file_name)
            LOGGER.critical(error)
            raise NameError(error)

        with zipfile.ZipFile(os.path.join(self.get_output_dir(), zip_file_name), 'a') as the_zip_file:
            for file in temp_list:
                the_zip_file.write(file)

        the_zip_file.close()
