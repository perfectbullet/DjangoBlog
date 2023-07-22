import contextlib
import os
import shlex
import socket
import subprocess

from loguru import logger


def proc_by_pid_win(pid):
    """
    on windows
    :param pid:
    :return:
    """
    find_pid_cmd = 'tasklist /FI "PID eq {}"'
    find_pid_args = shlex.split(find_pid_cmd.format(pid))
    logger.info('find_args {}', find_pid_args)
    proc_find = subprocess.Popen(find_pid_args, stdout=subprocess.PIPE)
    find_result = proc_find.stdout.read()
    logger.info('proc_find stdout is {}', find_result)
    return find_result


def check_or_get(port):
    """
    检测端口是否可用, 并返回新的端口
    :param port:
    :return:
    """
    if not isinstance(port, int):
        port = int(port)
    new_port = get_free_port([port, ])
    if not new_port:
        start = int(port)
        end = start + 9999
        new_port = get_free_port(i for i in range(start, end))
    return new_port


def get_free_port(ports=None):
    """
    参考
    https://www.programcreek.com/python/?code=spotify%2Fdocker_interface%2Fdocker_interface-master%2Fdocker_interface%2Futil.py#
    https://www.programcreek.com/python/?code=flaggo%2Fpydu%2Fpydu-master%2Fpydu%2Fnetwork.py
    https://www.programcreek.com/python/?CodeExample=get+free+port
    Get a free port.
    Parameters
    ----------
    ports : iterable
        ports to check (obtain a random port by default)
    Returns
    -------
    port : int
        a free port
    """
    logger.info('ports is {}'.format(ports))
    if ports is None:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _socket:
            _socket.bind(('', 0))
            _, port = _socket.getsockname()
            return port
    # Get ports from the specified list
    for port in ports:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as _socket:
            try:
                _socket.bind(('', port))
                return port
            except socket.error as ex:
                if ex.errno not in (48, 98, 10013, 10048):
                    logger.exception(ex)
                    return None
                else:
                    logger.info(ex)
                    pass
    logger.exception("无法找到可用端口: {}".format(ports))
    return None


def abspath(path, ref=None):
    """
    Create an absolute path.
    Parameters
    ----------
    path : str
        absolute or relative path with respect to `ref`
    ref : str or None
        reference path if `path` is relative
    Returns
    -------
    path : str
        absolute path
    Raises
    ------
    ValueError
        if an absolute path cannot be constructed
    """
    if ref:
        path = os.path.join(ref, path)
    if not os.path.isabs(path):
        raise ValueError("expected an absolute path but got '%s'" % path)
    return path


def split_path(path, ref=None):
    """
    Split a path into its components.
    Parameters
    ----------
    path : str
        absolute or relative path with respect to `ref`
    ref : str or None
        reference path if `path` is relative
    Returns
    -------
    list : str
        components of the path
    """
    path = abspath(path, ref)
    return path.strip(os.path.sep).split(os.path.sep)


if __name__ == '__main__':
    new_port = get_free_port(range(8666, 8666+999))
    print(new_port)
