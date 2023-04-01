import os

f_dir = os.path.abspath(os.path.dirname(__file__))

ONE_GB = 1024 * 1024 * 1024


def get_dir_size(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size


def get_size(path, thred=ONE_GB):

    for dirname in os.listdir(path):
        count = 0
        directory = os.path.join(path, dirname)
        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        size = os.path.getsize(os.path.join(root, file))
                        count += size
        if os.path.isfile(directory):
            filesize = os.path.getsize(directory)
            count += filesize
        if count > thred:
            print('dirname is %s %.2f' % (directory, count / 1024.0 / 1024.0 / 1024.0, ), 'GB')


if __name__ == '__main__':
    # size = get_dir_size(r'C:\Users\Administrator\AppData\Local')
    # print('Total size is: %.3f Mb' % (size / 1024 / 1024))

    size = get_size(r'D:\\python_workspace')
