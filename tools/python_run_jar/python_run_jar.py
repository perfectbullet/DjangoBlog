import os
import shlex
import subprocess
import time

import psutil
from loguru import logger

from jar_utils.jar_tools import get_jar_port
from jar_utils.port_utils import check_or_get

# 等待进程退出最长时间
WATI_TERMINAL_TIME = 2
# SIGTERM exit code, 退出状态码
SIGTERM_EXIT_CODE = 15
# 等待程序启动时间
WATI_JAR_START = 5

PWD = os.getcwd()
# JAVA_BIN = os.path.join(PWD, 'static', 'units', 'jre1.8.0_202', 'bin', 'java.exe')
JAVA_BIN = 'java'


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


def start_jar(jar_path):
    """
    通过命令启动jar包
    :param command:
    :return:
    {
        'pid': proc.pid,
        'start_ok': start_ok,
        'start_log': stdout.decode('utf8', 'ignore'),
    }
    """
    jar_ser_port = get_jar_port(jar_path)
    new_ser_port = check_or_get(jar_ser_port)
    jar_path_abs = os.path.abspath(jar_path)
    start_command = '{} -jar {} --server.port={}'.format(JAVA_BIN, jar_path_abs, new_ser_port)
    logger.info('start jar call subprocess run, start_command {}, pwd is {}'.format(start_command, PWD))
    proc = psutil.Popen(start_command, cwd=PWD)
    time.sleep(WATI_JAR_START)
    pid = proc.pid
    logger.info('start jar call subprocess run, pid {}'.format(pid))

    pid_exists = psutil.pid_exists(proc.pid)
    return {
        'pid': proc.pid,
        'reslut': pid_exists,
        'log': 'pid_exists {}'.format(pid_exists),
    }


def kill_proc(pid):
    """
    kill a process by pid
    通用的 终结进程
    参考文档为
    https://psutil.readthedocs.io/en/latest/#quick-links
    :param force:
    :param pid: int
    :return:
    """

    if pid is None:
        return {
            'result': False,
            'log': f'pid 为 None'
        }
    pid = int(pid)
    if not psutil.pid_exists(pid):
        return {
            'result': False,
            'log': f'pid {pid} 的进程不存在'
        }

    proc = psutil.Process(pid)
    proc.terminate()  # 更好的方式结束
    proc.kill()
    exit_code = proc.wait(WATI_TERMINAL_TIME)
    logger.info(f'exit_code is {exit_code}')
    return {
        'result': True if exit_code == SIGTERM_EXIT_CODE else False,
        'log': f'关闭状态 {exit_code}'
    }


def get_usage_pid(pid):
    """
    获取进程资源占用情况
    :param pid:
    :return:{
    pid
    cpu_percent
    status
    name
    memory_percent
    }
    """
    proc = psutil.Process(pid)
    with proc.oneshot():
        usage_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'status', 'memory_percent'])
        usage_info['rss'] = proc.memory_info().rss
        return usage_info


if __name__ == '__main__':
    jar_path = './base-plugin-app-0.0.1-SNAPSHOT3.jar'

    # 启动 jar包
    start_result = start_jar(jar_path)
    logger.info('start_result {}'.format(start_result))

    for i in range(10):
        use_info = get_usage_pid(start_result['pid'])
        logger.info('use_info: {}', use_info)
        time.sleep(3)

    # kill jar 包
    # kill_result = kill_proc(start_result['pid'])
    # print(kill_result)


