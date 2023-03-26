import os
from io import BytesIO
from os.path import join, getsize
from pathlib import PurePosixPath

import cv2
import numpy as np
from PIL import Image, ExifTags


def reduce_pil_image(img):
    """
    压缩 PIL image对象, 返回一个PIL image对象
    :param max_size:
    :param img: PIL image对象
    :return: PIL image对象
    """
    try:
        # 获取图片拍摄角度,再处理是保持角度
        orientation = 0
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img.getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except KeyError as e:
        print('KeyError, the key is {}'.format(e))
    except Exception as e:
        print('unkonwn Exception is {}'.format(e))
    # xsize, ysize = img.size
    # if xsize > max_size:
    #     ysize = int(max_size / xsize * ysize)
    #     xsize = max_size
    # elif ysize > max_size:
    #     xsize = int(max_size / ysize * xsize)
    #     ysize = max_size
    # img = img.resize((xsize, ysize))
    return img


def reduce_by_opencv(impath, newpath):
    '''
    opencv 通过改变尺寸压缩图片， 然后保存为jpg格式
    :param impath:
    :param suffix:
    :return:
    '''
    # img = cv2.imread(impath, flags=cv2.IMREAD_COLOR)
    img = cv2.imdecode(np.fromfile(impath, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        # cv2.imwrite(newpath, img, (80,))
        cv2.imencode(ext='.jpg', img=img)[1].tofile(newpath)
    else:
        print('######################### img read failed {} #########################'.format(impath))


def reduce_by_pil(impath, newpath):
    '''
    pil 通过改变尺寸压缩图片， 然后保存为jpg格式
    :param impath:
    :param suffix:
    :return:
    '''
    with open(impath, mode='rb') as fobj:
        stream = BytesIO(fobj.read())
        img = Image.open(stream).convert("RGB")
        img = reduce_pil_image(img)
        img.save(newpath)


if __name__ == '__main__':
    img_dir = r'D:\xiaomi10_photoes'
    reduce_dir = r'D:\xiaomi10_photoes_reduce'

    for root, dirs, files in os.walk(img_dir):
        # print(root, "consumes", end="")
        # print(sum([getsize(join(root, n)) for n in files]), end="")
        # print("bytes in", len(files), "non-directory files")
        new_root = root.replace(img_dir, reduce_dir)
        if not os.path.exists(new_root):
            os.mkdir(new_root)
        for fname in files:
            suffix = PurePosixPath(fname).suffix
            if suffix in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']:
                impath = join(root, fname)
                new_path = join(new_root, fname)
                new_path = new_path.replace(suffix, '.jpg')
                print('impath {}, newpath {}'.format(impath, new_path))
                try:
                    reduce_by_opencv(impath, new_path)
                except Exception as e:
                    print('######################### Exception {} #########################'.format(e))
