# -*- coding:utf-8 -*-
# Time   : 2024/9/13 11:57
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : common.py
# Software: PyCharm
# Description: Common defines

import os
from loguru import logger
import subprocess


# Global options
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_NO_SUCH_FILE = 2
EXIT_INVALID_ARG = 3
EXIT_INVALID_OPTION = 4
EXIT_NO_SUCH_PROJECT = 5
EXIT_NO_SUCH_DIRECTORY = 6
EXIT_RUN_COMMAND_FAILED = 7
EXIT_CODE_DOWNLOAD_FAILED = 8
EXIT_CODE_COMPILE_FAILED = 9
EXIT_CODE_UNPACK_FAILED = 10


class Options():
    def __init__(self):
        self.version = ""
        self.download = ""
        # get the root path of the project
        self.root_path = ""
        self.compile = ""
        self.unpack = ""

    def set_options(self, key, value):
        if key == "version":
            self.version = value
        elif key == "download":
            self.download = value
        elif key == "root_path":
            self.root_path = value
        elif key == "compile":
            self.compile = value
        elif key == "unpack":
            self.unpack = value
        else:
            pass


def run_command(path=None, command=None, debug=False):
    """
    Run a command in a given path
    :param debug:
    :param path: The path to run the command in
    :param command: The command to run
    :return: The return code of the command
    """
    if path is not None:
        if not os.path.exists(path):
            logger.error("Path not exists: " + path)
            return EXIT_NO_SUCH_DIRECTORY
        os.chdir(path)

    #logger.info(command)
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    if debug:
        for line in iter(res.stdout.readline, b''):
            print(line.decode('utf-8').strip())
    out, err = res.communicate()

    if res.returncode != 0:
        logger.error('command "{}" returned {}'.format(command, ErrorCodeToString(EXIT_RUN_COMMAND_FAILED)))
        return EXIT_RUN_COMMAND_FAILED
    return EXIT_SUCCESS


def ErrorCodeToString(error_code):
    """
    Convert error code to string
    :param error_code: The error code
    :return: The string of the error code
    """
    if error_code == EXIT_SUCCESS:
        return "EXIT_SUCCESS"
    elif error_code == EXIT_FAILURE:
        return "EXIT_FAILURE"
    elif error_code == EXIT_NO_SUCH_FILE:
        return "EXIT_NO_SUCH_FILE"
    elif error_code == EXIT_INVALID_ARG:
        return "EXIT_INVALID_ARG"
    elif error_code == EXIT_INVALID_OPTION:
        return "EXIT_INVALID_OPTION"
    elif error_code == EXIT_NO_SUCH_PROJECT:
        return "EXIT_NO_SUCH_PROJECT"
    elif error_code == EXIT_NO_SUCH_DIRECTORY:
        return "EXIT_NO_SUCH_DIRECTORY"
    elif error_code == EXIT_RUN_COMMAND_FAILED:
        return "EXIT_RUN_COMMAND_FAILED"
    elif error_code == EXIT_CODE_DOWNLOAD_FAILED:
        return "EXIT_CODE_DOWNLOAD_FAILED"
    elif error_code == EXIT_CODE_COMPILE_FAILED:
        return "EXIT_CODE_COMPILE_FAILED"
    elif error_code == EXIT_CODE_UNPACK_FAILED:
        return "EXIT_CODE_UNPACK_FAILED"

    else:
        return "Unknown error code"


GlobalOptions = Options()
