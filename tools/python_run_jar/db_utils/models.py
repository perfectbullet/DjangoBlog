from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import os
from os.path import join
from sqlalchemy import create_engine



class Base(DeclarativeBase):
    pass


class JarConf(Base):
    __tablename__ = "jar_conf"
    id: Mapped[int] = mapped_column(primary_key=True)
    jar_name: Mapped[str] = mapped_column(String(512))
    conf_name: Mapped[str] = mapped_column(String(512))
    fullname: Mapped[str] = mapped_column(String(512))
    ser_port: Mapped[int] = mapped_column(Integer())

    def __repr__(self) -> str:
        return f"JarConf(id={self.id!r}, jar_name={self.jar_name!r}, fullname={self.conf_name!r})"


class NginxConf(Base):
    __tablename__ = "nginx_conf"

    id: Mapped[int] = mapped_column(primary_key=True)
    conf_name: Mapped[str] = mapped_column(String(512))
    fullname: Mapped[str] = mapped_column(String(512))
    server_port: Mapped[int] = mapped_column(Integer())
    proxy_pass = mapped_column(String(512))

    def __repr__(self) -> str:
        return f"conf_name(id={self.id!r}, server_port={self.server_port!r})"


DB_PATH = join(os.getcwd(), 'db1.db')
engine = create_engine("sqlite:///{}".format(DB_PATH), echo=True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
