# -*- coding:utf-8 -*-
# Time   : 2024/9/13 10:17
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : onemore.py
# Software: PyCharm
# Description:
import os
import sys
from optparse import OptionParser

from loguru import logger

import parser_util
from common import *

# Please update version when something is changed!'
VERSION = '1.0'
# Requires Python 3.5 or newer.
PYTHON_VERSION_MAJOR = 3
PYTHON_VERSION_MINOR = 5

# quick check of system requirements:
major, minor = sys.version_info[:2]

if (major, minor) < (PYTHON_VERSION_MAJOR, PYTHON_VERSION_MINOR):
    logger.error("This script requires python >=3.5 to run!\n")
    logger.error("You seem to be running: " + sys.version)
    sys.exit(1)

# def help():
#     logger.info('onemore tool version: ' + VERSION)
#     logger.info('Usage: onemore.py [options]')
#     logger.info('Options:')
#     logger.info('  -h, --help       show this help message and exit')
#     logger.info('  -v, --version    onemore tool version')


# rewrite OptionParser
class MyOptionParser(OptionParser):
    def print_help(self, file=None):
        logger.info('onemore tool version: ' + VERSION)
        logger.info('Usage: onemore.py [options]')
        logger.info('Options:')
        logger.info('  -h, --help\tshow this help message and exit')
        logger.info('  -v, --version\tonemore tool version')
        for p in parser_util.get_parsers():
            logger.info('  {}, {}\t{}'.format(p.shortopt, p.longopt, p.desc))


def main():
    usage = 'usage: %prog [options to print]. Run with --help for more details'
    parser = MyOptionParser(usage=usage)

    parser.add_option('-v', '--version', dest='version', help='onemore tool version', default=VERSION)

    for p in parser_util.get_parsers():
        #logger.info('Adding parser name: ' + p.cls.__name__)
        # logger.info('Adding parser desc: ' + p.desc)
        # logger.info('Adding parser shortopt: ' + p.shortopt)
        # logger.info('Adding parser longopt: ' + p.longopt)
        parser.add_option(p.shortopt or '',
                          p.longopt,
                          dest=p.cls.__name__,
                          help=p.desc)

    (options, args) = parser.parse_args()

    # Set the options as global options
    for key, value in vars(options).items():
        GlobalOptions.set_options(key.lower(), value)

    GlobalOptions.root_path = os.path.dirname(os.path.abspath(__file__))

    # print help message if no options are provided
    if not any(vars(options).values()):
        parser.print_help()
        return 1

    if options.version:
        logger.info('onemore tool version: ' + VERSION)

    parsers_to_run = [p for p in parser_util.get_parsers()
                      if getattr(options, p.cls.__name__)]

    if not parsers_to_run:
        logger.error('No parsers selected. Run with --help for more details')
        return 1

    for i, p in enumerate(parsers_to_run):
        logger.success('Register parser: ' + p.cls.__name__)
        parser = p.cls()
        ret = parser.parse()
        if ret != EXIT_SUCCESS:
            logger.error('Parser {} failed with error code {}'.format(p.cls.__name__, ErrorCodeToString(ret)))
            return ret
        else:
            logger.success('Parser {} success'.format(p.cls.__name__))
    return 0


if __name__ == '__main__':
    result = main()
    sys.exit(result)
