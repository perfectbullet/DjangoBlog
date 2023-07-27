#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2023-05-30 16:12:53
Description: 生成客户端主程序
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import argparse
import os
import sys

import webview
from loguru import logger
from api.api import API
from pyapp.config.config import Config
from pyapp.db.db import DB
from flask_app_in_subprocess.wsgi_gevent import run_flask_process

cfg = Config()  # 配置
db = DB()  # 数据库类
api = API()  # 本地接口

cfg.init()


def on_shown():
    # 展示窗口时启动
    logger.info('先启动flask应用, current pid is {}', os.getpid())
    run_flask_process()
    logger.info('启动flask应用完成')
    logger.info('程序启动')
    # 初始化数据库
    db.init()


def on_loaded():
    logger.info('on_loaded 加载完毕')


def on_closing():
    logger.info('on_closing 程序关闭')


def WebViewApp(ifCef=False):
    # 是否为开发环境
    Config.devEnv = sys.flags.dev_mode
    logger.info('Config.devEnv is {}, current pid is {}'.format(Config.devEnv, os.getpid()))

    # 视图层页面URL
    if Config.devEnv:
        # 开发环境
        MAIN_DIR = f'http://localhost:{Config.devPort}/'
        template = os.path.join(MAIN_DIR, "")  # 设置页面，指向远程
    else:
        # 生产环境
        MAIN_DIR = os.path.join(".", "web")
        template = os.path.join(MAIN_DIR, "index.html")  # 设置页面，指向本地

    logger.info('MAIN_DIR is {}, template is {}'.format(MAIN_DIR, template))

    # 系统分辨率
    screens = webview.screens
    screens = screens[0]
    width = screens.width
    height = screens.height
    # 程序窗口大小
    initWidth = int(width * 3 / 3)
    initHeight = int(height * 4 / 5)
    minWidth = int(initWidth / 2)
    minHeight = int(initHeight / 2)

    # 创建窗口
    window = webview.create_window(title=Config.appName, url=template, js_api=api, width=initWidth, height=initHeight,
                                   min_size=(minWidth, minHeight))

    api.init_nginx()
    # 获取窗口实例
    api.setWindow(window)

    # 绑定事件
    window.events.shown += on_shown
    window.events.loaded += on_loaded
    window.events.closing += on_closing

    # CEF模式
    guiCEF = 'cef' if ifCef else None

    # 启动窗口
    webview.start(debug=Config.devEnv, http_server=True, gui=guiCEF)
    logger.info('webview.start 完成！！！')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cef", action="store_true", dest="if_cef", help="if_cef")
    args = parser.parse_args()

    ifCef = args.if_cef  # 是否开启cef模式

    WebViewApp(ifCef)
