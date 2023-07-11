import os
from os.path import join
from subprocess import PIPE
from os.path import exists

import psutil
from loguru import logger

from tools.nginx_conf_parser import nginx


class NginxConf:
    def __init__(self, nginx_home):

        self.nginx_home = nginx_home
        # nginx 系统配置
        self.nginx_conf = os.path.abspath(join(nginx_home, 'conf', 'nginx.conf'))
        
        self.nginx = join(nginx_home, 'nginx.exe')
        self.check_exists(self.nginx_home, self.nginx_conf, self.nginx)
        # 用户配置文件夹
        self.conf_d = join(nginx_home, 'conf.d')
        if not os.path.exists(self.conf_d):
            os.mkdir(self.conf_d)
        self.reload_cmd = self.nginx + ' -s reload' + ' -c {}'.format(self.nginx_conf)

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
        stdout = proc.stdout.read(1024)
        logger.info('stdout {}', stdout)

    def get_usage_port(self):
        """
        :param conf_dir:
        :return:
        """
        ports = ['80', ]
        for fname in os.listdir(self.conf_d):
            if not fname.endswith('.conf'):
                continue
            fpath = join(self.conf_d, fname)
            conf = nginx.loadf(fpath)
            servers = conf.servers
            for serv in servers:
                listen_port = serv.filter('Key', 'listen')[0].value
                ports.append(listen_port)
        return ports

    def get_port(self, old_port, add_port):
        """
        在 old port基础上获取可用端口
        :param old_port:
        :return:
        """
        usage_ports = self.get_usage_port()
        usage_ports.extend(add_port)
        new_port = old_port
        while new_port in usage_ports:
            msg = f'端口冲突, {new_port}'
            logger.info(msg)
            new_port = str(int(new_port) + 1)
        add_port.append(new_port)
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
        c = nginx.loadf(self.nginx_conf)

        # 读取用户配置, 并写入 conf.d 文件夹下, 以端口命名的*.conf文件中
        customer_conf = nginx.loadf(customer_conf)
        http = customer_conf.filter('Http')[0]
        servers = http.filter('Server')
        add_port = []
        for serv in servers:
            lst = serv.filter('Key', 'listen')[0]
            listen_port = lst.value
            listen_port = self.get_port(listen_port, add_port)
            lst.value = listen_port
            nginx.dumpf(serv, f'{self.conf_d}\\listen_{listen_port}.conf')
            logger.info(f'add listen_port {listen_port}')
        self.reload_nginx()
        return {
            'result': True,
            'log': f'添加配置成功 {add_port}',
            'ports': add_port
        }


if __name__ == '__main__':
    nginx_home = r'D:\zjpython_work\nginx-1.24.0'
    conf_d = join(nginx_home, 'conf.d')
    nginx_conf = join(nginx_home, 'conf', 'nginx.conf')  # r'D:\zjpython_work\nginx-1.24.0\conf\nginx.conf'
    nginx_exe = join(nginx_home, 'nginx.exe')  # r'D:\zjpython_work\nginx-1.24.0\nginx.exe'

    nginxconf = NginxConf(nginx_home)
    # 客户配置文件
    my_nginx_conf = 'c2.conf'
    res = nginxconf.add_server(my_nginx_conf)
    logger.info(f'add conf result is {res}')
    # 比如返回
    # {'result': True, 'log': "添加配置成功 ['84', '85']", 'ports': ['84', '85']}
    # 可以通过  http://localhost:84/ 测试
