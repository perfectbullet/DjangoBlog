import os


class Config(object):
    """项目的配置文件"""
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:liaoqianhurryup@49.232.208.236:3303/liaoqian_mysql_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = 'abc'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
