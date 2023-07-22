import os
import socket
import time
from os.path import exists
from os.path import join
from subprocess import PIPE

import psutil
from loguru import logger

from . import nginx

from common_utils.const import Const


def port_check(HOST):
    """
    检查系统占用端口
    :param HOST:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)  # Timeout in case of port not open
    try:
        s.connect((HOST, 22))  # Port ,Here 22 is port
        return True
    except:
        return False


class NginxConf:
    def __init__(self, nginx_home):
        self.nginx_home = os.path.abspath(nginx_home)
        # nginx 系统配置
        self.nginx_conf = os.path.abspath(join(nginx_home, 'conf', 'nginx.conf'))
        self.nginx = os.path.abspath(join(nginx_home, 'nginx.exe'))
        self.nginx_err_log = os.path.abspath(join(nginx_home, 'logs', 'error.log'))
        self.check_exists(self.nginx_home, self.nginx_conf, self.nginx)
        # 用户配置文件夹
        self.conf_d = join(nginx_home, 'conf.d')
        if not os.path.exists(self.conf_d):
            os.mkdir(self.conf_d)
        # -c 参数要用绝对路径
        self.reload_cmd = self.nginx + ' -s reload' + ' -c {}'.format(self.nginx_conf)
        self.start_cmd = self.nginx + ' -c {} -e {} -p {}'.format(self.nginx_conf, self.nginx_err_log, self.nginx_home)
        # self.start_cmd = 'start /b {} -c {} -e {} -p {}'.format(self.nginx, self.nginx_conf, self.nginx_err_log, self.nginx_home)

    def check_exists(self, *arg):
        # 检查路径都存在
        for fpath in arg:
            logger.info('检查路径是否存在 {}'.format(fpath))
            if not exists(fpath):
                msg = "路径不存在 {}, 当前路径 {}".format(fpath, os.getcwd())
                logger.exception(msg)
                raise FileNotFoundError(msg)

    def reload_nginx(self):
        """
        重启 nginx
        :return:
        """
        logger.info(f'nginx reload cmd {self.reload_cmd}')
        proc = psutil.Popen(self.reload_cmd, stdout=PIPE, cwd=self.nginx_home)
        time.sleep(Const.WAIT_NGINX_START)
        logger.info('重启nginx pid {}'.format(proc.pid))

    def start_nginx(self):
        """
        启动 nginx
        # 设置 stdout=PIPE 容易造成死锁
        # https://segmentfault.com/a/1190000020660715
        # https://stackoverflow.com/questions/10406532/python-subprocess-output-on-windows
        :return:
        """
        try:
            logger.info(f'启动 nginx cmd {self.start_cmd}')

            for pro in psutil.process_iter(['pid', 'name']):
                pname = pro.info['name']
                pid = pro.info['pid']
                if 'nginx' in pname:
                    logger.info(f'nginx 已经启动 {pname}, pid {pid}')
                    return {
                        'result': True,
                        'msg': 'nginx 已经启动',
                        'pid': pid
                    }
            logger.info('准备启动 nginx !')
            proc = psutil.Popen(self.start_cmd, shell=False, cwd=self.nginx_home)
            # proc = psutil.Popen(self.start_cmd, shell=False, cwd=self.nginx_home)
            time.sleep(Const.WAIT_NGINX_START)
            pid = proc.pid
            logger.info('启动 nginx pid {}', pid)
            if psutil.pid_exists(pid):
                return {'result': True, 'msg': 'start ok', 'pid': pid}
            else:
                return {'result': False, 'msg': 'start failed', 'pid': pid}
        except Exception as e:
            logger.info('启动 nginx {}', e)
            logger.exception(e)
            raise e

    def get_usage_port(self):
        """
        获取端口占用情况，包括系统端口
        :param conf_dir:
        :return:
        """
        ports = ['80', ]
        # 获取系统占用的端口
        ports.extend([str(i.laddr.port) for i in psutil.net_connections()])
        conf_ports = self.get_nginx_conf_port()
        ports.extend(list(conf_ports.keys()))
        return ports

    def get_nginx_conf_port(self):
        conf_ports = {}
        for fname in os.listdir(self.conf_d):
            if not fname.endswith('.conf'):
                continue
            fpath = join(self.conf_d, fname)
            conf = nginx.loadf(fpath)
            servers = conf.servers
            for serv in servers:
                listen_port = serv.filter('Key', 'listen')[0].value
                conf_ports[listen_port] = fpath
        return conf_ports

    def get_port(self, old_port, usage_ports, add_port):
        """
        在 old port基础上获取可用端口
        :param old_port:
        :return:
        """
        usage_ports.extend(add_port)
        new_port = old_port
        while new_port in usage_ports:
            msg = f'端口冲突, {new_port}'
            logger.info(msg)
            new_port = str(int(new_port) + 1)
        add_port.append(new_port)
        usage_ports.append(new_port)
        return new_port

    def add_server(self, customer_conf):
        """
        # 读取用户配置, 并写入 conf.d 文件夹下, 以端口命名的*.conf文件中
        :param customer_conf:
        :return:
        """
        logger.info('customer_conf is {}'.format(customer_conf))
        if not os.path.exists(self.nginx_conf) or not os.path.exists(customer_conf):
            logger.info('配置文件路径不存在')
            exit(0)

        # 读取用户配置, 并写入 conf.d 文件夹下, 以端口命名的*.conf文件中
        customer_conf = nginx.loadf(customer_conf)
        http = customer_conf.filter('Http')[0]
        servers = http.filter('Server')
        add_port = []
        #
        nginx_server_ports = self.get_usage_port()
        for serv in servers:
            lst = serv.filter('Key', 'listen')[0]
            listen_port = lst.value
            listen_port = self.get_port(listen_port, nginx_server_ports, add_port)
            lst.value = listen_port
            nginx.dumpf(serv, f'{self.conf_d}\\listen_{listen_port}.conf')
            logger.info(f'add listen_port {listen_port}')
        conf_ports = self.get_nginx_conf_port()
        self.reload_nginx()
        return {
            'result': True,
            'log': f'添加配置成功 {add_port}',
            'ports': add_port,
            'conf_ports': list(conf_ports.keys())
        }

    def rm_server(self, server_port):
        """
        按 conf.d 下端口查找 server_port 把不要的端口删除，然后重启
        :param server_port:
        :return:
        """
        conf_ports = self.get_nginx_conf_port()
        conf_path = conf_ports.get(server_port, None)
        logger.info('rm server conf_ports {}, conf_path {}'.format(conf_ports, conf_path))
        if conf_path and os.path.exists(conf_path):
            os.remove(conf_path)
            time.sleep(Const.WAIT_NGINX_START)
            self.reload_nginx()
            conf_ports.pop(server_port)
            logger.info('删除配置文件 {}, 并重启服务'.format(conf_path))
        else:
            logger.info('没有配置该端口 {}'.format(server_port))
        return conf_ports

    def up_server(self, server_port='', key='', value=''):
        """
        按 conf.d 下端口查找 server_port, 然后根据 key value 配置新的端口
        :param value:
        :param key:
        :param server_port:
        :return:
        """
        res = {
            'result': False,
            'msg': ''
        }
        for fname in os.listdir(self.conf_d):
            if not fname.endswith('.conf'):
                continue
            fpath = join(self.conf_d, fname)
            conf = nginx.loadf(fpath)
            serv = conf.servers[0]
            listen_port = serv.filter('Key', 'listen')[0].value
            if listen_port == server_port:
                logger.info('find server {}'.format(serv))
                root_obj = serv.filter('Key', key)[0]
                root_obj.value = value
                logger.info('got key obj {}'.format(root_obj))
                fpath_b = nginx.dumpf(serv, fpath)
                logger.info('fpath_b {}'.format(fpath_b))
                time.sleep(Const.WAIT_NGINX_START)
                self.reload_nginx()
                res['result'] = True
                res['msg'] = '更新端口 {} 的server, key={}, value={}'.format(server_port, key, value)
                break
        return res
