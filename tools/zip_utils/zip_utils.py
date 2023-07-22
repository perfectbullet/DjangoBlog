import os
import zipfile
from typing import List
from xml.etree import ElementTree as et
from loguru import logger


def check_utf8(file):
    """
    查看文件编码格式
    """
    valid_utf8 = True
    try:
        et.parse(file)
    except ValueError as e:
        valid_utf8 = False
        logger.exception(e)
    return valid_utf8


def get_node_attr(zip_path, attr_name: str) -> str:
    """

    """
    with zipfile.ZipFile(zip_path) as zf:
        # Create a Path object.
        for name in zf.namelist():
            if name.endswith('xml'):
                valid_utf8 = check_utf8(zf.open(name))
                if not valid_utf8:
                    raise ValueError('文件编码错误')
                master_dom = et.parse(zf.open(name))
                root_node = master_dom.getroot()
                attrib = root_node.attrib
                return attrib.get(attr_name)
    return ''


def make_new_zip(master_zip: str, subzips: List[tuple], nginx_conf: str) -> str:
    """
    重新打包zip
    :param master_zip:
    :param subzips: 插件包的参数list[zip_path, front_zip, router, module]
    :param nginx_conf
    :return: new_zip_path
    """
    master_name, suffix = master_zip.rsplit('.', 1)
    # master 包写入
    new_zip_path = '{}-new.{}'.format(master_name, suffix)

    with zipfile.ZipFile(new_zip_path, mode='w') as new_zip:
        # 写入 ningx
        new_zip.write(nginx_conf, os.path.basename(nginx_conf))
        # 先寫入主包 jar
        xml_name = 'xml_name.xml'
        root_node = None
        # root_node  中键入节点
        root_plugin = et.Element("pluginList")
        pluginProxyNginxBean = et.Element("pluginProxyNginxBean", attrib={'nginxName': os.path.basename(nginx_conf)})

        with zipfile.ZipFile(master_zip) as master_zf:
            # Create a Path object.
            for name in master_zf.namelist():
                if name.endswith('jar'):
                    new_zip.writestr(name, master_zf.open(name).read())
                elif name.endswith('xml'):
                    valid_utf8 = check_utf8(master_zf.open(name))
                    if not valid_utf8:
                        raise ValueError('文件编码错误')
                    xml_name = os.path.basename(name)
                    master_dom = et.parse(master_zf.open(name))
                    root_node = master_dom.getroot()
        # 其他包
        for zip_path, front_zip, router, module in subzips:
            if zip_path:
                with zipfile.ZipFile(zip_path) as other_zipfile:
                    # Create a Path object.
                    for name in other_zipfile.namelist():
                        if name.endswith('jar'):
                            new_zip.writestr(name, other_zipfile.open(name).read())
                        elif name.endswith('xml'):
                            valid_utf8 = check_utf8(other_zipfile.open(name))
                            if not valid_utf8:
                                raise ValueError('文件编码错误')
                            sub_dom = et.parse(other_zipfile.open(name))
                            pluginList = sub_dom.find('pluginList')
                            for pluginItemBean in pluginList:
                                # <pluginHtmlBean name="对应前端压缩文件名称" router="对应前端router" module="前端对应module"/>
                                pluginHtmlBean = et.Element("pluginHtmlBean",
                                                            attrib={
                                                                'name': os.path.basename(front_zip),
                                                                'router': router,
                                                                'module': module,
                                                            })
                                pluginItemBean.append(pluginHtmlBean)
                                root_plugin.append(pluginItemBean)
            if front_zip:
                new_zip.write(front_zip, os.path.basename(front_zip))
        root_node.append(root_plugin)
        root_node.append(pluginProxyNginxBean)
        xml_str = et.tostring(root_node, encoding='UTF-8')
        ver = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""".encode(encoding='UTF-8')
        xml_ver = ver + xml_str
        new_zip.writestr(xml_name, xml_ver)

        return new_zip_path


def test_check_utf8(testzip_path):
    with zipfile.ZipFile(testzip_path) as master_zf:
        # Create a Path object.
        for name in master_zf.namelist():
            if name.endswith('xml'):
                valid_utf8 = check_utf8(master_zf.open(name))
                print('valid_utf8: ', valid_utf8)


def test_get_node_attr(testzip_path):
    res = get_node_attr(testzip_path, 'pluginFlag')
    print('get_node_attr ', res)


if __name__ == '__main__':
    testzip_path = 'before_zip/sofa-master1.zip'
    subzips2 = [('before_zip/sofa-node-plugin2.zip',
                 'before_zip/sofa-node-plugin2对应的前端.zip', 'sofa-master1/sofa-node-plugin2/', 'sofa-node-plugin2'),
                ('before_zip/sofa-node-plugin3.zip',
                 'before_zip/sofa-node-plugin3对应的前端.zip', 'sofa-master1/sofa-node-plugin2/', 'sofa-node-plugin2')]
    nginx_conf2 = 'before_zip/nginx_dysy.conf'
    # proper = read_zip_properties(testzip_path, file_path_in_zip)
    # conf_path = get_zip_info(testzip_path)
    # new_zip_path = make_new_zip(testzip_path, subzips2, nginx_conf2)
    # print(new_zip_path)

    testzip_path1 = 'before_zip/1.zip'
    test_get_node_attr(testzip_path1)
    testzip_path2 = 'before_zip/2.zip'
    test_get_node_attr(testzip_path2)
    testzip_path3 = 'before_zip/3.zip'
    test_get_node_attr(testzip_path3)
