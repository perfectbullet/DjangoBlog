import os
import re
import shutil
from os.path import join, getsize


if __name__ == '__main__':
    # 删除文件的正则表达式
    rm_re = re.compile(r'使用说明(.*).txt')
    re_name_a = re.compile(r'(\d+-\d+ .*)_一手免费IT资源加一手QQ3303538452,加我送课\[\d\](.mp4)')
    re_name_2 = re.compile(r'(\d+-\d+.*)_(.*)QQ3303538452(.*)(\.mp4|\.png)$')

    JYMM = '解压密码'
    KQBD = '看前必读'
    MFLQ = '免费领取课程'
    # file_dir = r'G:\mksz494 - 首门程序员理财课 Python量化交易系统实战[完结]'
    # file_dir = r'G:\Python全能工程师（2022版本）'
    file_dir = 'G:\幕课网算法与数据结构体系课-bobo全部算法'
    for root, dirs, files in os.walk(file_dir):
        if JYMM in dirs:
            dir_path = join(root, JYMM)
            # shutil.rmtree(dir_path)
        for name in files:
            fpath = join(root, name)
            if '(一手资源微信Darren69669)' in name:
                new_name = name.replace('(一手资源微信Darren69669)', '')
                new_path = join(root, new_name)
                os.rename(fpath, new_path)
                print(name)
                print(new_name)
                print()
                continue

            mt_res = rm_re.match(name)
            re_mt = re_name_a.match(name)
            re2_mt = re_name_2.match(name)
            print(name)

            if KQBD in name or MFLQ in name:
                print(fpath)
                # os.remove(fpath)

            if mt_res:
                print(mt_res.group())
                # os.remove(fpath)
                continue
            if re_mt:
                new_name = re_mt.group(1) + re_mt.group(2)
                new_path = join(root, new_name)
                # os.rename(fpath, new_path)
                print(name)
                print(new_name)
                print()
                continue

            if re2_mt:
                new_name = re2_mt.group(1) + re2_mt.group(4)
                new_path = join(root, new_name)
                # os.rename(fpath, new_path)
                print(name)
                print(new_name)
                print()
                continue

