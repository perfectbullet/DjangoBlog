"""
@FileName：upload_app.py
@Description：
@Author：zhoujing
@contact：121531845@qq.com
@Time：2023/8/8 23:35
@Department：红石扩大小区
@Website：www.zhoujing.com
@Copyright：©2019-2023 xxx信息科技有限公司
"""
import os

from flask import request, url_for, send_from_directory, jsonify
from loguru import logger
from werkzeug.utils import secure_filename

HTTP200 = 200
HTTP400 = 400

ALLOWED_EXTENSIONS = {'zip', 'conf'}
html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_app_init(app):
    """
    初始化上传app
    @param app:
    @return:
    """
    @app.get('/')
    def hello():
        return '在子进程中利用 gevent WSGIServer 运行 Flask 他应用的方法'

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        logger.info('request method is {}', request.method)
        if request.method == 'POST':
            file = request.files['file']
            sofa_name = request.form.get('sofa_name')
            logger.info('form data is {}', request.form)
            if sofa_name:
                sofa_dir = os.path.join(app.config['UPLOAD_FOLDER'], sofa_name)
            else:
                sofa_name = file.filename.rsplit('.', 1)[0]
                sofa_dir = os.path.join(app.config['UPLOAD_FOLDER'], sofa_name)
            if not os.path.exists(sofa_dir):
                os.mkdir(sofa_dir)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(sofa_dir, filename)
                file.save(filepath)
                file_url = url_for('uploaded_file', filename=filename)
                result = jsonify({
                    'status': HTTP200,
                    'filepath': filepath,
                    'file_name': filename,
                    'sofa_name': sofa_name,
                    'msg': 'file_url is {}'.format(file_url)
                })
                logger.info('result {}', result)
                return result
        return html
