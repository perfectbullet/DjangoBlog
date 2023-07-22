#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-26 20:48:26
LastEditTime: 2023-05-30 15:40:45
Description: 系统类
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''

import getpass
import json
import os
import shutil
import subprocess
from os.path import join
import webview
from loguru import logger
from pyapp.config.config import Config
from pyapp.update.update import AppUpdate

from api.utils.util import Util
from api.utils.python_run_jar import start_jar, kill_proc
from api.utils.nginx_conf import NginxConf
from common_utils.const import Const


class System:
    """
    系统类
    """

    window = None

    def save_file(self, file_path):
        res = {
            'result': True,
            'msg': 'ok'
        }
        if os.path.exists(file_path):
            save_filename = os.path.basename(file_path)
            result = self.window.create_file_dialog(webview.SAVE_DIALOG, save_filename=save_filename)
            shutil.copy(file_path, result)
        else:
            res['result'] = False
            res['msg'] = '文件不存在{}'.format(file_path)
        return res

    @staticmethod
    def system_py2js(func, info):
        '''调用js中挂载到window的函数'''
        infoJson = json.dumps(info)
        System.window.evaluate_js(f"{func}('{infoJson}')")

    @staticmethod
    def get_all_installed_software():
        '''获取按照软件列表'''
        rst_list = Util.get_software()
        return rst_list

    @staticmethod
    def init_start_nginx():
        ''' 开启默认nginx '''
        logger.info('开启默认nginx')
        ngconf = NginxConf(Const.NGINX_HOME)
        ret = ngconf.start_nginx()
        return ret

    @staticmethod
    def up_nginx(port, key, value):
        ''' 修改ng对应项'''
        logger.info('修改ng对应项')
        ngconf = NginxConf(Const.NGINX_HOME)
        ret = ngconf.up_server(port, key, value)
        return ret

    @staticmethod
    def rm_nginx( port):
        ''' 删除ng指定端口'''
        logger.info('删除ng指定端口')
        ngconf = NginxConf(Const.NGINX_HOME)
        ret = ngconf.rm_server(port)
        return ret

    @staticmethod
    def add_ng_config(customer_conf):
        ''' 业务新增nginx server 配置'''
        ngconf = NginxConf(Const.NGINX_HOME)
        ret = ngconf.add_server(customer_conf)
        return ret

    @staticmethod
    def uninstall_software(name):
        '''卸载软件 '''
        rst = Util.uninstall_software(name)
        return rst

    @staticmethod
    def start_jar(path):
        ''' 启动jar '''
        rst = start_jar(path)
        return rst

    @staticmethod
    def close_jar(pid):
        '''关闭jar'''
        rst = kill_proc(pid)
        return rst

    @staticmethod
    def system_getAppInfo():
        '''程序基础配置信息'''
        return {
            'appName': Config.appName,  # 应用名称
            'appVersion': Config.appVersion  # 应用版本号
        }

    def system_checkNewVersion(self):
        '''检查更新'''
        appUpdate = AppUpdate()  # 程序更新类
        res = appUpdate.check()
        return res

    def system_downloadNewVersion(self):
        '''下载新版本'''
        appUpdate = AppUpdate()  # 程序更新类
        res = appUpdate.run()
        return res

    def system_cancelDownloadNewVersion(self):
        '''取消下载新版本'''
        appUpdate = AppUpdate()  # 程序更新类
        res = appUpdate.cancel()
        return res

    def system_getOwner(self):
        # 获取本机用户名

        return getpass.getuser()

    def system_pyOpenFile(self, path):
        '''用电脑默认软件打开本地文件'''
        # 判断以下当前系统类型
        if Config.appIsMacOS:
            path = path.replace("\\", "/")
            subprocess.call(["open", path])
        else:
            path = path.replace("/", "\\")
            os.startfile(path)

    def system_pyCreateFileDialog(self, fileTypes=['全部文件 (*.*)'], directory=''):
        """
        打开文件对话框
        """
        # 可选文件类型
        # fileTypes = ['Excel表格 (*.xlsx;*.xls)']
        fileTypes = tuple(fileTypes)  # 要求必须是元组
        result = System.window.create_file_dialog(dialog_type=webview.OPEN_DIALOG, directory=directory,
                                                  allow_multiple=True, file_types=fileTypes)
        resList = list()
        if result is not None:
            for res in result:
                filePathList = os.path.split(res)
                dir = filePathList[0]
                filename = filePathList[1]
                ext = os.path.splitext(res)[-1]
                resList.append({
                    'filename': filename,
                    'ext': ext,
                    'dir': dir,
                    'path': res
                })
        return resList
