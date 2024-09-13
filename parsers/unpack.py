# -*- coding:utf-8 -*-
# Time   : 2024/9/13 16:20
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : unpack.py
# Software: PyCharm
# Description: For unpack android images

from parser_util import register_parser, OnemoreParser
from loguru import logger
from common import *
import os


@register_parser(longopt='--unpack', desc='unpack android images', shortopt='-u', optional=True)
class Unpack(OnemoreParser):
    def parse(self):
        logger.info('Unpack android images')
        logger.info(GlobalOptions.unpack)

        # get the input path from user inputs
        logger.success('Please input the path to unpack the images: [default: {}]'.format(os.getcwd()))
        unpack_path = input()
        if not os.path.exists(unpack_path):
            logger.error('Unpack path not exists: ' + unpack_path)
            logger.error('Please check the unpack path, create it if not exists!')
            return EXIT_NO_SUCH_DIRECTORY

        # unpack images
        ret = run_command(unpack_path, GlobalOptions.unpack, True)
        if ret != EXIT_SUCCESS:
            return EXIT_CODE_UNPACK_FAILED
        return ret
