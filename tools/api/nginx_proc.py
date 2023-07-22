import psutil
from loguru import logger
import time
from api.utils.nginx_conf import NginxConf
from common_utils.const import Const
from common_utils import get_process_by_name_port, get_process_by_name


class NginxProc:
    """
    nginx 进程管理类
    """

    def __init__(self):
        self.NGINX_HOME = Const.NGINX_HOME
        self.nginx_conf = NginxConf(self.NGINX_HOME)
        self.proc = None
        self.pid = None
        self.init_nginx()

    def init_nginx(self):
        """
        默认开启nginx
        """
        try:
            logger.info(f'NginxProc 启动 cmd {self.nginx_conf.start_cmd}')
            for proc in psutil.process_iter(['pid', 'name']):
                pname = proc.info['name']
                pid = proc.info['pid']
                if 'nginx' in pname:
                    logger.info(f'nginx 已经启动 {pname}, pid {pid} {proc.status()}, 准备终结该进程!')
                    proc.kill()
            logger.info('初始化 nginx 完成')
            self.proc = psutil.Popen(self.nginx_conf.start_cmd, shell=False, cwd=self.NGINX_HOME)
            time.sleep(Const.WAIT_NGINX_START)
            logger.info('初始化 nginx pid {}', self.proc.pid)
        except Exception as e:
            logger.info('初始化 nginx 失败{}', e)
            logger.exception(e)
            raise e
