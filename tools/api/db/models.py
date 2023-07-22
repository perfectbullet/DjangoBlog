#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PPX/api/db/models.py
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:29:49
LastEditTime: 2023-04-24 13:52:25
Description: 创建数据表
usage: 更新数据表格式后，请按如下操作迁移数据库：
        m=备注更改内容 npm run alembic

        注意：上述命令仅能迁移打包程序自带数据库(Config.staticDir)。在程序运行初始化时，会自动检测并迁移本地电脑中保存的数据库(Config.storageDir)
'''

import json

from sqlalchemy import DateTime, Numeric, Column, Integer, String, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class BaseModel(Base):
    '''基类'''
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), doc='创建时间', comment='创建时间',
                        server_default=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"))
    updated_at = Column(DateTime(), doc='更新时间', comment='更新时间',
                        server_default=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"),
                        onupdate=text("(DATETIME(CURRENT_TIMESTAMP, 'localtime'))"))

    def _gen_tuple(self):
        # 处理 日期 等无法正常序列化的对象
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        for col in self.__table__.columns:
            try:
                if isinstance(col.type, DateTime):
                    value = convert_datetime(getattr(self, col.name))
                elif isinstance(col.type, Numeric):
                    value = float(getattr(self, col.name))
                else:
                    value = getattr(self, col.name)
                yield (col.name, value)
            except Exception as e:
                print(e)
                pass

    def toDict(self):
        # 转化为 字典
        return dict(self._gen_tuple())

    def toJson(self):
        # 序列化为 JSON
        return json.dumps(self.toDict())


class PPXStorageVar(BaseModel):
    '''储存变量'''
    __tablename__ = "ppx_storage_var"
    key = Column(String(), doc='键', nullable=False, index=True)
    val = Column(String(), doc='值', server_default='', nullable=False)
    remark = Column(String(), doc='备注', server_default='', nullable=False)

    def __str__(self):
        return self.key + ' => ' + self.val


class NginxProcInfo(BaseModel):
    """
    nginx 进程信息
    """
    __tablename__ = "ppx_nginx_proc_info"
    proc_name = Column(String(), doc='进程名称', server_default='', nullable=False)
    pid = Column(Integer, doc='进程号', nullable=False)

    def __str__(self):
        return 'NginxProcInfo:{}    {}'.format(self.pid, self.proc_name)


class JarProcInfo(BaseModel):
    """
    java 进程信息
    """
    __tablename__ = "ppx_jar_proc_info"
    proc_name = Column(String(), doc='jar 进程名称', server_default='', nullable=False)
    pid = Column(Integer, doc='进程号', nullable=False)
    jar_name = Column(String(), doc='jar 包名称', server_default='', nullable=False)
    port = Column(Integer, doc='jar 启动端口', nullable=False)

    def __str__(self):
        return 'NginxProcInfo:{}    {}'.format(self.pid, self.proc_name)


if __name__ == '__main__':
    from pyapp.db.db import DB
    db_path = DB.dbPath

    engine = create_engine("sqlite:///{}".format(db_path), echo=True)

    res = Base.metadata.create_all(engine, [Base.metadata.tables['ppx_jar_proc_info'], Base.metadata.tables['ppx_nginx_proc_info']])
    print(res)
