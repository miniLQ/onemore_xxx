# -*- coding:utf-8 -*-
# Time   : 2024/9/13 10:50
# Author : liuqi
# Email  : liuqi@longcheer.com
# File   : download.py
# Software: PyCharm
# Description: For download code by project config file

from parser_util import register_parser, OnemoreParser
from loguru import logger
from common import *
import os
import xml.etree.ElementTree as ET


def download_code(project_name, repo_url, repo_sync):
    logger.info('Download code for project: ' + project_name)
    logger.success('Repo init: ' + repo_url)
    logger.success('Repo sync: ' + repo_sync)
    # download code
    # check download path

    # get the input path from user inputs
    logger.error('Please input the path to download the code: [default: {}]'.format(os.getcwd()))
    download_path = input()
    # current path if user input nothing
    if download_path == "":
        download_path = os.getcwd()
    logger.success('Download path: ' + download_path)
    if not os.path.exists(download_path):
        logger.error('Download path not exists: ' + download_path)
        logger.error('Please check the download path, create it if not exists!')
        return EXIT_NO_SUCH_DIRECTORY

    # download code
    ret = run_command(download_path, repo_url, True)
    if ret != EXIT_SUCCESS:
        return EXIT_CODE_DOWNLOAD_FAILED
    ret = run_command(download_path, repo_sync, True)
    if ret != EXIT_SUCCESS:
        return EXIT_CODE_DOWNLOAD_FAILED
    return ret


@register_parser(longopt='--download', desc='download code by project config file', shortopt='-d', optional=True)
class Download(OnemoreParser):
    def parse(self):
        logger.info('Download code by project config file')
        project_config = os.path.join(GlobalOptions.root_path, 'config', 'ProjectConfig.xml')
        logger.info('Project config file: ' + project_config)

        if not os.path.exists(project_config):
            logger.error('Project config file not exists: ' + project_config)
            logger.error('Please check the project config file, create it if not exists!')
            return EXIT_NO_SUCH_FILE

        # parse xml config file
        tree = ET.parse(project_config)
        root = tree.getroot()

        for child in root:
            ProjectInterName = ""
            ProjectRepoInit = ""
            ProjectRepoSync = ""
            for sub_child in child:
                if sub_child.tag == "ProjectInterName":
                    ProjectInterName = sub_child.text
                if sub_child.tag == "ProjectRepoInit":
                    ProjectRepoInit = sub_child.text
                if sub_child.tag == "ProjectRepoSync":
                    ProjectRepoSync = sub_child.text

            if ProjectInterName == GlobalOptions.download.upper():
                # download code
                # TODO
                ret = download_code(ProjectInterName, ProjectRepoInit, ProjectRepoSync)
                return ret

        # 模糊搜索
        logger.error("Can not find project: " + GlobalOptions.download)
        logger.error("Do you mean:")
        mean_list = []
        for child in root:
            ProjectInterName = ""
            ProjectRepoInit = ""
            ProjectRepoSync = ""
            for sub_child in child:
                if sub_child.tag == "ProjectInterName":
                    ProjectInterName = sub_child.text
                if sub_child.tag == "ProjectRepoInit":
                    ProjectRepoInit = sub_child.text
                if sub_child.tag == "ProjectRepoSync":
                    ProjectRepoSync = sub_child.text

            if GlobalOptions.download.upper() in ProjectInterName:
                mean_list.append([ProjectInterName, ProjectRepoInit, ProjectRepoSync])

        if len(mean_list) > 0:
            for i in range(len(mean_list)):
                if i == 0:
                    logger.error("  " + str(0) + ". " + "Exit")
                logger.error("  " + str(i + 1) + ". " + mean_list[i][0])
            logger.success("Please input the number of the project you want:")
            num = input()
            if num.isdigit() and 0 < int(num) <= len(mean_list):
                # logger.info('Download code for project: ' + mean_list[int(num)-1][0])
                # download code
                # TODO
                ret = download_code(mean_list[int(num) - 1][0], mean_list[int(num) - 1][1], mean_list[int(num) - 1][2])
                return ret
            elif num == "0":
                return EXIT_SUCCESS
            else:
                logger.error("Invalid input, please try again!")
                return EXIT_INVALID_ARG
        else:
            logger.error("No project found, please check the project config file!")
            return EXIT_NO_SUCH_PROJECT
