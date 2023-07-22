from os.path import join

class Const:
    NGINX_HOME = join('static', 'utils', 'nginx-1.24.0')
    # 等待nginx 启动时间
    WAIT_NGINX_START = 5