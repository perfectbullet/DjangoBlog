import zipfile
import yaml

from loguru import logger
from jproperties import Properties
from .port_utils import check_or_get

# jar 配置文件路径
PROPER_SUFFIX = '.properties'
YAM_SUFFIX = '.yml'
JAR_CONF_SUFFIX = {PROPER_SUFFIX, YAM_SUFFIX}


def find_jar_conf(jar_path: str, conf_name: str) -> str:
    """
    在jar中查找文件
    :param jar_path:
    :param conf_name: 配置文件名称
    :return:
    """
    with zipfile.ZipFile(jar_path) as zf:
        # Create a Path object.
        for finfo in zf.filelist:
            filename = finfo.filename
            if filename.endswith(conf_name):
                return filename


def read_jar_xml(jar_path: str, yml_path: str) -> dict:
    """
    读取jar包中的yml
    :param yml_path:
    :param jar_path:
    :return: dict
    """
    contents_bytes = read_zip_file_content(jar_path, yml_path)
    yml_info = yaml.safe_load(contents_bytes)
    return yml_info


def read_jar_properties(jar_path: str, properties_path: str) -> Properties:
    """
    读取 jar 包 propertie

    获取数据示例  configs.get('server.port').data
    :param properties_path:
    :param jar_path:
    :return:
    """
    contents = read_zip_file_content(jar_path, properties_path)
    properties = Properties()
    properties.load(contents)
    return properties


def read_zip_file_content(zip_path: str, file_path: str) -> bytes:
    """
    读取 压缩包指定文件内容
    :param file_path:
    :return:
    """
    with zipfile.ZipFile(zip_path) as zf:
        # Create a Path object.
        path = zipfile.Path(zf, at=file_path)
        contents = path.read_bytes()
        return contents


def save_jar_properties(proper: Properties):
    """

    :param proper:
    :return:
    """
    pass


def get_jar_port(jar_path: str, conf_name: str):
    """
    获取 jar 包 的端口
    :param jar_path:
    :param conf_name:
    :return:
    """
    # 先查找文件在jar中的路径
    conf_path = find_jar_conf(jar_path, conf_name)
    if conf_path is None:
        logger.info('jar 包中没有找到文件名 {} 的文件'.format(conf_name))
        return None
    if conf_name.endswith(PROPER_SUFFIX):
        proper = read_jar_properties(jar_path, conf_path)
        server_ort = proper.get('server.port').data
    elif conf_name.endswith(YAM_SUFFIX):
        yml_info = read_jar_xml(jar_path, conf_name)
        server_ort = yml_info['server']['port']
    else:
        logger.info('jar 配置文件名称格式不正确 {}'.format(JAR_CONF_SUFFIX))
        return None
    return server_ort, conf_path


if __name__ == '__main__':
    testjar_path = 'base-plugin-app-0.0.1-SNAPSHOT3.jar'
    file_path_in_jar = r'BOOT-INF/classes/application.properties'
    conf_name = 'application.properties'
    # proper = read_jar_properties(testjar_path, file_path_in_jar)
    server_port = get_jar_port(testjar_path, conf_name)
    new = check_or_get(server_port)
    print(server_port)
