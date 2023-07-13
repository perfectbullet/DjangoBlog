import time
from os.path import join
from nginx.nginx_conf import NginxConf
from loguru import logger

import requests

if __name__ == '__main__':
    nginx_home = r'D:\zjpython_work\nginx-1.24.0'
    conf_d = join(nginx_home, '../conf.d')
    nginx_conf = join(nginx_home, 'conf', '../nginx.conf')  # r'D:\zjpython_work\nginx-1.24.0\conf\nginx.conf'
    nginx_exe = join(nginx_home, 'nginx.exe')  # r'D:\zjpython_work\nginx-1.24.0\nginx.exe'

    nginxconf = NginxConf(nginx_home)
    nginxconf.start_nginx()

    # 客户配置文件
    my_nginx_conf = 'c2.conf'
    res = nginxconf.add_server(my_nginx_conf)
    logger.info(f'add conf result is {res}')
    conf_ports = res['conf_ports']
    for port in conf_ports:
        url = 'http://localhost:{}'.format(port)
        try:
            r = requests.get(url)
            msg = 'url {}  请求状态 {}'.format(url, r.status_code)
            logger.info(msg)
        except:
            msg = 'url {} 请求失败'.format(url)
            logger.error(msg)

    nginxconf.up_server(server_port='99', key='root', value='dist333')

    # 比如返回
    # {'result': True, 'log': "添加配置成功 ['84', '85']", 'ports': ['84', '85']}
    # 可以通过  http://localhost:84/ 测试
    time.sleep(5)
    nginxconf.rm_server('85')
