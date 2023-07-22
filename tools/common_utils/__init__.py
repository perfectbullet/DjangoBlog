import contextlib
import os
import socket
from typing import Optional

import psutil

from loguru import logger


def mkdir(local_dir):
    """
    递归创建, 本地路径
    """
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)


def check_port_free(port):
    """

    """
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _socket:
        try:
            _socket.bind(('', port))
            return True
        except socket.error as ex:
            if ex.errno not in (48, 98, 10013, 10048):
                logger.exception(ex)
                return False
            else:
                logger.info(ex)
                return False


def get_process_by_port(port) -> Optional[psutil.Process]:
    """
    按端口获取第一个匹配到的进程
    """
    for p in psutil.process_iter():
        for c in p.connections():
            if c.status == 'LISTEN' and c.laddr.port == port:
                return p


def get_process_by_name(process_name) -> Optional[psutil.Process]:
    """
    按名稱获取第一个匹配到的进程
    """
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc


def get_process_by_name_port(process_name, port):
    processes = [proc for proc in psutil.process_iter() if proc.name()
                 == process_name]
    for p in processes:
        for c in p.connections():
            if c.status == 'LISTEN' and c.laddr.port == port:
                return p
    return None
