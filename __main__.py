"""
Main entry point
"""
import logging
import os
import sys
import platform
from argparse import ArgumentParser
import qct
from qct.version import __version__
COMPILE = False
LOGGER = logging.getLogger('qct_main')


def set_directory_structure():
    """Function that sets directory structure"""
    if COMPILE:
        if platform.system().lower() == 'linux':
            if os.path.islink('/bin/quick'):  # pylint: disable=no-else-return
                return qct.Directories(base_dir=os.path.dirname(os.readlink('/bin/quick')))
            else:
                return qct.Directories(base_dir=os.path.dirname(os.path.realpath(sys.argv[0])))
        else:
            return qct.Directories(base_dir=os.path.dirname(os.path.realpath(sys.argv[0])))

    else:
        return qct.Directories(base_dir=os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
    directories = set_directory_structure()
    YML_FILE = None

    logging.basicConfig(format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
                        filename=os.path.join(directories.logging_dir, 'logs.txt'))
    logging.getLogger().setLevel(directories.get_logging_level())
    LOGGER.warning('Logging started!!')

    arg_parser = ArgumentParser(description='Quick Config Templates')
    arg_parser.add_argument('-d', '--debug', help='The debug level default is level 3, highest is 1 and lowest is 5, '
                                                  'it will also show you your yml data in a JSON format')
    arg_parser.add_argument('-f', '--folder', help='Put output file in a folder, name of the folder')
    arg_parser.add_argument('-o', '--outputfile', help='The filename to output config to')
    arg_parser.add_argument('-v', '--version', action='version', version=__version__)

    subparsers = arg_parser.add_subparsers(title='commands', description='Valid commands: a single command is required',
                                           help='CLI Help', dest='a sinlge command please see the -h option')
    subparsers.required = True

    # This is the sub parser to run a configuration build
    arg_parser_run_build = subparsers.add_parser('run_build', help='Run a config build.')
    arg_parser_run_build.set_defaults(which_sub='run_build')
    arg_parser_run_build.add_argument('yml_file', nargs='*', help='The name of the yml file of your config, not '
                                                                  'required if you are using the -a option')
    arg_parser_run_build.add_argument('-a', '--auto_build', action='store_true',
                                      help='This option uses a csv only to build a config.  If you use this option '
                                           'you are also required to use the -t option.')
    arg_parser_run_build.add_argument('-b', '--begin', nargs='+', help='Begin config from your selection, like Cisco')
    arg_parser_run_build.add_argument('-c', '--config_only', action='store_true', help='Display the config, do not '
                                                                                       'output to file')
    arg_parser_run_build.add_argument('-i', '--include', nargs='+', help='Include config from your selection, like '
                                                                         'Cisco')
    arg_parser_run_build.add_argument('-j', '--json', action='store_true', help='Display the config, in JSON format')
    arg_parser_run_build.add_argument('-p', '--package', help='The zip filename to output the package to')
    arg_parser_run_build.add_argument('-r', '--remote', action='store_true', help='Remote builder')
    arg_parser_run_build.add_argument('-t', '--typefile', help='The filename of the csv for variable replacement')
    arg_parser_run_build.add_argument('-y', '--yml', action='store_true', help='Display the config, in YML format')

    # This is the sub parser to run a dev server to receive config builds
    arg_parser_run_server = subparsers.add_parser('run_server', help='Run a server to build configs, this is a dev '
                                                                     'server only!')
    arg_parser_run_server.set_defaults(which_sub='run_server')
    arg_parser_run_server.add_argument('-i', '--ip', help='The IP to listen on.')
    arg_parser_run_server.add_argument('-d', '--debug', action='store_true', help='Debug')
    arg_parser_run_server.add_argument('-p', '--port', help='The port to listen on.')
    arg_parser_run_server.add_argument('-u', '--uri', help='The base api uri, default is /qct/api/v1')

    # This is the sub parser to run a conversion to Prefix-List to YML
    arg_parser_create_yml_from_prefix_list = subparsers.add_parser('pl_create', help='Create Prefix-List YML '
                                                                                     'from a Prefix-List')
    arg_parser_create_yml_from_prefix_list.set_defaults(which_sub='pl_create')
    arg_parser_create_yml_from_prefix_list.add_argument('file_name', help='The name of the text file the '
                                                                          'Prefix-List is in.')
    arg_parser_create_yml_from_prefix_list.add_argument('-c', '--config_only', action='store_true',
                                                        help='Display the output, do not output to file')
    arg_parser_create_yml_from_prefix_list.add_argument('-r', '--reset_sequences', action='store_true',
                                                        help='Reset sequence numbers')

    # This is the sub parser to run a conversion to Route-Map to YML
    arg_parser_create_yml_from_route_map = subparsers.add_parser('rm_create', help='Create Route-Map YML '
                                                                                   'from a Route-Map ')
    arg_parser_create_yml_from_route_map.set_defaults(which_sub='rm_create')
    arg_parser_create_yml_from_route_map.add_argument('file_name', help='The name of the text file the '
                                                                        'Route-Map is in.')
    arg_parser_create_yml_from_route_map.add_argument('-c', '--config_only', action='store_true',
                                                      help='Display the output, do not output to file')
    arg_parser_create_yml_from_route_map.add_argument('-r', '--reset_sequences', action='store_true',
                                                      help='Reset sequence numbers')

    # This is the sub parser to run a conversion to ACL to YML
    arg_parser_create_yml_from_acl = subparsers.add_parser('acl_create', help='Create ACL YML from a ACL ')
    arg_parser_create_yml_from_acl.set_defaults(which_sub='acl_create')
    arg_parser_create_yml_from_acl.add_argument('file_name', help='The name of the text file the ACL is in.')
    arg_parser_create_yml_from_acl.add_argument('-c', '--config_only', action='store_true',
                                                help='Display the output, do not output to file')
    arg_parser_create_yml_from_acl.add_argument('-r', '--reset_sequences', action='store_true',
                                                help='Reset sequence numbers')

    args = arg_parser.parse_args()

    try:
        if args.debug:
            directories.set_logging_level(args.debug)
            logging.getLogger().setLevel(directories.get_logging_level())

        if args.folder:
            directories.set_output_dir_folder(args.folder)

        if args.which_sub == 'pl_create':
            if args.outputfile:
                OUTPUT_FILE_NAME = args.outputfile

            else:
                OUTPUT_FILE_NAME = 'pl_convert.yml'

            qct.convert_pl(directories, args.file_name, OUTPUT_FILE_NAME, args.config_only, args.reset_sequences)

        elif args.which_sub == 'rm_create':
            if args.outputfile:
                OUTPUT_FILE_NAME = args.outputfile

            else:
                OUTPUT_FILE_NAME = 'rm_convert.yml'

            qct.convert_rm(directories, args.file_name, OUTPUT_FILE_NAME, args.config_only, args.reset_sequences)

        elif args.which_sub == 'acl_create':
            if args.outputfile:
                OUTPUT_FILE_NAME = args.outputfile

            else:
                OUTPUT_FILE_NAME = 'acl_convert.yml'

            qct.convert_acl(directories, args.file_name, OUTPUT_FILE_NAME, args.config_only, args.reset_sequences)

        elif args.which_sub == 'run_build':
            if args.outputfile:
                OUTPUT_FILE_NAME = args.outputfile

            else:
                OUTPUT_FILE_NAME = 'config.txt'

            if args.auto_build:
                if args.typefile:
                    pass

                else:
                    arg_parser.print_help()
                    sys.exit('\n!!! You are not using the -a option correctly please see the help. !!!')

            else:
                if len(args.yml_file) == 1:
                    YML_FILE = args.yml_file[0]

                else:
                    arg_parser.print_help()
                    sys.exit('\n!!! You are required to have only one yml_file argument. !!!')

            qct.TemplateEngine(directories, YML_FILE, OUTPUT_FILE_NAME, args.config_only, args.json, args.yml,
                               args.package, args.typefile, args.auto_build, args.remote, args.begin, args.include)

        elif args.which_sub == 'run_server':
            if args.ip:
                IP = args.ip

            else:
                IP = '127.0.0.1'

            if args.port:
                PORT = args.port

            else:
                PORT = 5000

            if args.uri:
                BASE_API_URI = args.uri

            else:
                BASE_API_URI = '/qct/api/v1'

            qct.run_local_server(IP, PORT, BASE_API_URI, args.debug, directories)

    except AttributeError as e:  # pylint: disable=invalid-name
        LOGGER.critical(e)
        arg_parser.print_help()

    except FileNotFoundError as e:  # pylint: disable=invalid-name
        LOGGER.critical(e)
        print('\n !!! {} !!! \n'.format(e))
        arg_parser.print_help()

    except Exception as e:  # pylint: disable=broad-except,invalid-name
        LOGGER.critical(e)
        arg_parser.print_help()
