import logging
import os
import sys
from argparse import ArgumentParser
import module as mod
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'dev'
__version_info__ = (1, 0, 5, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'
COMPILE = False


LOGGER = logging.getLogger(__name__)


def set_directory_structure():
    if COMPILE:
        return mod.Directories(base_dir=os.path.dirname(os.path.realpath(sys.argv[0])))

    else:
        return mod.Directories(base_dir=os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
    directories = set_directory_structure()
    yml_file = None

    logging.basicConfig(format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
                        filename=os.path.join(directories.logging_dir, 'logs.txt'))
    logging.getLogger().setLevel(directories.get_logging_level())
    LOGGER.warning('Logging started!!')

    arg_parser = ArgumentParser(description='Quick Config Templates')
    arg_parser.add_argument('yml_file', nargs='*', help='The name of the yml file of your config, '
                                                        'not required if you are using the -a option')
    arg_parser.add_argument('-a', '--auto_build', action='store_true',
                            help='This option uses a csv only to build a config.  If you use this option you '
                                 'are also required to use the -t option.')
    arg_parser.add_argument('-c', '--config_only', action='store_true', help='Display the config, do not output '
                                                                             'to file')
    arg_parser.add_argument('-d', '--debug', help='The debug level default is level 3, highest is 1 and lowest is 5, '
                                                  'it will also show you your yml data in a JSON format')
    arg_parser.add_argument('-f', '--folder', help='Put output file in a folder, name of the folder')
    arg_parser.add_argument('-j', '--json', action='store_true', help='Display the config, in JSON format')
    arg_parser.add_argument('-o', '--outputfile', help='The filename to output config to')
    arg_parser.add_argument('-t', '--typefile', help='The filename of the csv for variable replacement')
    arg_parser.add_argument('-v', '--version', action='version', version=__version__)
    arg_parser.add_argument('-y', '--yml', action='store_true', help='Display the config, in YML format')

    args = arg_parser.parse_args()

    try:
        if args.debug:
            directories.set_logging_level(args.debug)
            logging.getLogger().setLevel(directories.get_logging_level())

        if args.folder:
            directories.set_output_dir_folder(args.folder)

        if args.outputfile:
            output_file_name = args.outputfile

        else:
            output_file_name = 'config.txt'

        if args.auto_build:
            if args.typefile:
                yml_file = mod.auto_build_check(directories, args.typefile)

            else:
                arg_parser.print_help()
                exit('\n!!! You are not using the -a option correctly please see the help. !!!')

        else:
            if len(args.yml_file) == 1:
                yml_file = args.yml_file[0]

            else:
                arg_parser.print_help()
                exit('\n!!! You are required to have only one yml_file argument. !!!')

        mod.scripts.te(directories, mod.scripts.pre_run_yml(directories.get_yml_dir(), yml_file, args.typefile),
                       output_file_name, args.config_only, args.json, args.yml)

    except AttributeError as e:
        LOGGER.critical(e)
        arg_parser.print_help()
