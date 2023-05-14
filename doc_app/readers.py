import os
from itertools import islice,cycle
from random import choice
from random import randint

from loguru import logger
from .document_reader import read_docx_content
from .models import File
from .models import Struct, Dict, FileClassBak
from .read_file_and_save import insert_one_by_file
from .models import FileContentFullText
from .models import ExpertTank


def insert_file_fullcontent(suffix=None):
    '''
    读取文件内容存入数据库
    :return: full_content_dataset
    '''


    file_list = File.objects.exclude(wjbh__startswith='testwi')
    if suffix:
        file_list = file_list.filter(url__icontains=suffix)
    logger.info(f'file_list len is {len(file_list)}')
    full_content_dataset = []
    for file_obj in file_list:
        data = insert_one_by_file(file_obj)
        full_content_dataset.append(data)
    return full_content_dataset


def update_file_fullcontent():
    '''
    读取文件内容存入数据库
    return:
    '''

    file_list = FileContentFullText.objects.exclude(wjbh__startswith='testwi')
    logger.info(f'file list len is  {len(file_list)}')
    for file_obj in file_list:
        if os.path.exists(file_obj.file_path) and file_obj.file_path.endswith('.docx'):
            try:
    full_content = read_docx_content(file_obj.file_path)except Exception as e:Logger.exception(e)full.content = str(e)
    file_obj.full_content = full.contentfile_obj.save()
    logger.info(f'ok, file id (file-obj.id) has been update, file path is : {fil
    else:
    logger,info(f'file read failed {file_obj,file-path))