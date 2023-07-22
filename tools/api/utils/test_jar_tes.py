import unittest

from .jar_tools import read_jar_xml, read_jar_properties, find_jar_conf


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pass
        # self.assertEqual(True, False)  # add assertion here

    def test_read_jar_xml(self):
        testjar_path = 'nginxWebUI-3.6.1.jar'
        yml_path = 'app.yml'
        yml_info = read_jar_xml(testjar_path, yml_path)
        self.assertIn('server', yml_info)

    def test_read_jar_properties(self):
        testjar_path = 'base-plugin-app-0.0.1-SNAPSHOT3.jar'
        file_path_in_jar = r'BOOT-INF/classes/application.properties'
        proper = read_jar_properties(testjar_path, file_path_in_jar)

        server_ort = proper.get('server.port').data
        self.assertEqual(server_ort, '8666')

    def test_find_jar_conf(self):
        testjar_path = 'base-plugin-app-0.0.1-SNAPSHOT3.jar'
        file_name_in_jar = 'application.properties'
        find_conf = find_jar_conf(testjar_path, file_name_in_jar)
        print('\n{} \n{}'.format('*' * 100, find_conf))
        self.assertIsNotNone(find_conf, '没有配置文件 {}'.format(file_name_in_jar))


if __name__ == '__main__':
    unittest.main()
