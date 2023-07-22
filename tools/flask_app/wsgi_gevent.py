#!/usr/bin/python
"""WSGI server example"""
import os
import time
from multiprocessing import Process

from gevent.pywsgi import WSGIServer
from loguru import logger
from common_utils import check_port_free, get_process_by_port
FLASK_PORT = 5000


def run_app():
    """
    只有在子进程运行时中导入 app
    """
    from flask_app.server import app
    logger.info('run_app pid is {}', os.getpid())
    wsgi_server = WSGIServer(('0.0.0.0', FLASK_PORT), app)
    wsgi_server.serve_forever()


def run_flask_process():
    """
    子进程中
    """
    other_proc = get_process_by_port(FLASK_PORT)
    if other_proc is not None:
        logger.info('FLASK_PORT({}) 被占用, pid is {}, port_free {}, try kill it', FLASK_PORT, other_proc.pid, other_proc.name())
        other_proc.kill()

    logger.info('在子进程中启动 WSGIServer, pid is {}, FLASK_PORT {}', os.getpid(), FLASK_PORT)
    proc = Process(target=run_app, daemon=False, name='flask_WSGIServer')
    proc.start()
    logger.info('flask_WSGIServer on {}, pid is {}, time is {}', FLASK_PORT, proc.pid, time.asctime())


if __name__ == '__main__':
    logger.info('__main__ pid is {}', os.getpid())
    run_flask_process()
    logger.info('__main__ ok, pid is {}', os.getpid())
