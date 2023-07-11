"""
@FileName：test.py\n
@Description：\n
@Author：zhoujing\n
@contact：121531845@qq.com\n
@Time：2023/7/11 21:57\n
@Department：红石扩大小区\n
@Website：www.zhoujing.com\n
@Copyright：©2019-2023 xxx信息科技有限公司
"""

from tools.nginx_conf_parser import nginx

if __name__ == '__main__':
    test_path = r'F:\下载\dy-ng-conf\nginx.conf'
    conf = nginx.loadf(test_path)
    print(conf)
    path = nginx.dumpf(conf, 'nginx2.conf')
    print(path)
    conf2 = nginx.loadf(path)
    print(conf2)

