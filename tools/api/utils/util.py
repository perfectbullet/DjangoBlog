__author__ = 'jmh081701'

from api.utils.get_reg_value import get_all_installed_software
import os
import subprocess


class Util:
    @staticmethod
    def get_software():
        rst_list = get_all_installed_software()
        rst = []
        for each in rst_list:
            rst.append(each[1])
        return rst

    @staticmethod
    def uninstall_software(software_name):
        rst_list = get_all_installed_software()
        uninstall_string = ""
        for each in rst_list:
            if each[0] == software_name:
                uninstall_string = each[1]
                break
        if uninstall_string == "":
            print("Not found installed program.")
            return '0'
        else:
            mypwd = "\\".join(uninstall_string.split('\\')[:-1])[1:]
            os.chdir(mypwd)
            split_path = uninstall_string.split('\\')
            cmd = split_path[-1].replace(r'"', '')
            cmd = cmd.replace(" /allusers", "")
            print("cmd is ", cmd)
            subprocess.Popen(mypwd, executable=cmd)
