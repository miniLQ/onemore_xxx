# -*- coding:utf-8 -*-
# Time   : 2024/9/13 16:20
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : unpack.py
# Software: PyCharm
# Description: For unpack android images

from parser_util import register_parser, OnemoreParser, get_system_type
from loguru import logger
from common import *
import os


@register_parser(longopt='--unpack', desc='unpack android images', shortopt='-u', optional=True)
class Unpack(OnemoreParser):
    def parse(self):
        logger.info('Unpack android images')
        logger.info(GlobalOptions.unpack)

        if not os.path.exists(GlobalOptions.unpack):
            logger.error('{} is not exist!' + GlobalOptions.unpack)
            logger.error('Please check it and try again!')
            return EXIT_NO_SUCH_FILE

        # get the input path from user inputs
        logger.success('Please input the output path to unpack the images: [default: {}]'.format(os.getcwd()))
        outputpath = input()
        if outputpath == '':
            outputpath = os.getcwd()
        outputpathAbs = os.path.abspath(outputpath)
        if not os.path.exists(outputpathAbs):
            logger.error('Unpack path not exists: ' + outputpathAbs)
            logger.error('Please check the unpack path, create it if not exists!')
            return EXIT_NO_SUCH_DIRECTORY

        # get the unpack tools path
        unpackToolsPath = os.path.join(GlobalOptions.root_path, 'tools', 'Android_boot_image_editor')

        # unpack images
        cmd = 'rm -rf {}/build'.format(unpackToolsPath)
        ret = run_command(None, cmd, True)
        if ret != EXIT_SUCCESS:
            return EXIT_RUN_COMMAND_FAILED

        cmd = 'cp -r {} {}'.format(GlobalOptions.unpack, unpackToolsPath)
        ret = run_command(None, cmd, True)
        if ret != EXIT_SUCCESS:
            return EXIT_RUN_COMMAND_FAILED

        os.chdir(unpackToolsPath)

        system_type = get_system_type()
        if system_type == 'Windows':
            cmd = 'gradlew.bat unpack'.format(unpackToolsPath)
        else:
            cmd = 'gradlew unpack'.format(unpackToolsPath)
        ret = run_command(unpackToolsPath, cmd, True)
        if ret != EXIT_SUCCESS:
            return EXIT_RUN_COMMAND_FAILED

        cmd = 'cp -rf {}/build {}'.format(unpackToolsPath, os.path.join(outputpathAbs, 'unpack_output'))
        ret = run_command(None, cmd, True)
        if ret != EXIT_SUCCESS:
            return EXIT_RUN_COMMAND_FAILED

        logger.info("Output path: " + os.path.join(outputpathAbs, 'unpack_output'))

        return ret
