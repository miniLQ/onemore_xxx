# -*- coding:utf-8 -*-
# Time   : 2024/9/13 14:23
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : compile.py
# Software: PyCharm
# Description: For compile code by project config file

from parser_util import register_parser, OnemoreParser
from loguru import logger
from common import *
import os
import xml.etree.ElementTree as ET


@register_parser(longopt='--compile', desc='compile code by project config file', shortopt='-c', optional=True)
class Compile(OnemoreParser):
    def parse(self):
        logger.info('Compile code by project config file')
        project_config = os.path.join(GlobalOptions.root_path, 'config', 'ProjectConfig.xml')
        logger.info('Project config file: ' + project_config)

        if not os.path.exists(project_config):
            logger.error('Project config file not exists: ' + project_config)
            logger.error('Please check the project config file, create it if not exists!')
            return EXIT_NO_SUCH_FILE

        logger.info(GlobalOptions.compile)

        project_name = GlobalOptions.compile.split(' ')[0]
        build_component = GlobalOptions.compile.split(' ')[1]
        build_profile = GlobalOptions.compile.split(' ')[2]

        # parse xml config file
        tree = ET.parse(project_config)
        root = tree.getroot()

        for child in root:
            ProjectInterName = ""
            ProjectRepoInit = ""
            ProjectRepoSync = ""
            for sub_child in child:
                if sub_child.tag == 'ProjectBuildScript':
                    ProjectBuildScript = sub_child.text
                if sub_child.tag == 'ProjectInterName':
                    ProjectInterName = sub_child.text

            if ProjectInterName == project_name.upper():
                logger.info('Compile code for project: ' + ProjectInterName)
                logger.success('Project build script: ' + ProjectBuildScript)
                # check build script
                buildScriptAbsPath = os.path.join(GlobalOptions.root_path, 'config', 'build_scripts', ProjectBuildScript)
                if not os.path.exists(buildScriptAbsPath):
                    logger.error('Project build script not exists: ' + buildScriptAbsPath)
                    logger.error('Please check the project build script, create it if not exists!')
                    return EXIT_NO_SUCH_FILE

                # get the input path from user inputs
                logger.success('Please input the path to compile the code:')
                code_path = input()
                # 如果用户直接输入回车，则默认下载到当前路径
                if code_path == "":
                    code_path = os.getcwd()
                logger.success('Code path: ' + code_path)
                # compile code
                #cmd = 'chmod +x ' + buildScriptAbsPath
                #ret = run_command(cmd)
                #if ret != EXIT_SUCCESS:
                #    return EXIT_RUN_COMMAND_FAILED
                cmd = 'bash {} {} {} {}'.format(buildScriptAbsPath, code_path, build_component, build_profile)
                ret = run_command(code_path, cmd, True)
                if ret != EXIT_SUCCESS:
                    return EXIT_CODE_COMPILE_FAILED

        # 模糊搜索
        mean_list = []
        for child in root:
            ProjectInterName = ""
            ProjectBuildScript = ""
            for sub_child in child:
                if sub_child.tag == 'ProjectBuildScript':
                    ProjectBuildScript = sub_child.text
                if sub_child.tag == 'ProjectInterName':
                    ProjectInterName = sub_child.text

            if project_name.upper() in ProjectInterName:
                mean_list.append([ProjectInterName, ProjectBuildScript])

        if len(mean_list) > 0:
            logger.error("Can not find project: " + project_name)
            logger.error("Do you mean:")
            for i in range(len(mean_list)):
                if i == 0:
                    logger.error("  " + str(0) + ". " + "Exit")
                logger.error("  " + str(i + 1) + ". " + mean_list[i][0])

            logger.success("Please input the number of the project you want:")
            num = input()
            if num.isdigit() and 0 < int(num) <= len(mean_list):
                # logger.info('Download code for project: ' + mean_list[int(num)-1][0])
                # compile code
                # TODO
                # check build script
                buildScriptAbsPath = os.path.join(GlobalOptions.root_path, 'config', 'build_scripts', mean_list[int(num) - 1][1])
                if not os.path.exists(buildScriptAbsPath):
                    logger.error('Project build script not exists: ' + buildScriptAbsPath)
                    logger.error('Please check the project build script, create it if not exists!')
                    return EXIT_NO_SUCH_FILE

                # get the input path from user inputs
                logger.success('Please input the path to compile the code: [default: {}]'.format(os.getcwd()))
                code_path = input()
                # current path if user input nothing
                if code_path == "":
                    code_path = os.getcwd()
                logger.success('Code path: ' + code_path)

                cmd = 'bash {} {} {} {}'.format(buildScriptAbsPath, code_path, build_component, build_profile)
                ret = run_command(code_path, cmd, True)
                if ret != EXIT_SUCCESS:
                    return EXIT_CODE_COMPILE_FAILED
                return ret
            elif num == "0":
                return EXIT_SUCCESS
            else:
                logger.error("Invalid input, please try again!")
                return EXIT_INVALID_ARG
        else:
            logger.error("No project found, please check the project config file!")
            return EXIT_NO_SUCH_PROJECT

