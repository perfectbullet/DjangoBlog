import zipfile

from jproperties import Properties
from jar_utils.port_utils import check_or_get


def read_jar_properties(jar_path: str, properties_path: str) -> Properties:
    """
    读取 jar 包 propertie

    获取数据示例  configs.get('server.port').data
    :param properties_path:
    :param jar_path:
    :param file_path:
    :return:
    """
    contents = read_zip_file_content(jar_path, properties_path)
    properties = Properties()
    properties.load(contents)
    return properties


def read_zip_file_content(zip_path: str, file_path: str) -> str:
    """
    读取 压缩包指定文件内容
    :param file_path:
    :return:
    """
    with zipfile.ZipFile(zip_path) as zf:
        # Create a Path object.
        path = zipfile.Path(zf, at=file_path)
        contents = path.read_text(encoding='UTF-8')
        return contents


def get_jar_port(jar_path, pro_path='BOOT-INF/classes/application.properties'):
    """
    获取 jar 包 的端口
    :param jar_path:
    :param pro_path:
    :return:
    """
    proper = read_jar_properties(jar_path, pro_path)
    server_ort = proper.get('server.port').data
    return server_ort


if __name__ == '__main__':
    testjar_path = 'base-plugin-app-0.0.1-SNAPSHOT3.jar'
    # file_path_in_jar = r'BOOT-INF/classes/application.properties'
    # proper = read_jar_properties(testjar_path, file_path_in_jar)
    server_port = get_jar_port(testjar_path)
    new = check_or_get(server_port)
    print(server_port)
