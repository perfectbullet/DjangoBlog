#!/usr/bin/python
"""WSGI server example"""
from multiprocessing import Process

from gevent.pywsgi import WSGIServer


def run_app():
    """
    只有在子进程运行时中导入 app
    """
    from server import app
    from gevent.server import _tcp_listener

    listener = _tcp_listener(('0.0.0.0', 5004))
    wsgi_server = WSGIServer(listener, app)
    wsgi_server.serve_forever()


if __name__ == '__main__':
    import time

    print('在子进程中运行 Flask或其他应用的方法')
    proc = Process(target=run_app, daemon=False)
    proc.start()
    print('Serving on 5004... ok, ', time.asctime())
    proc.join(20)
    print('end ', time.asctime())
