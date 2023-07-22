import os

from flask import Flask
from flask import request, url_for, send_from_directory, jsonify
from flask_cors import CORS
from flask_loguru import Logger
from werkzeug.utils import secure_filename

from zip_utils.zip_utils import make_new_zip, get_node_attr
from common_utils import mkdir

ALLOWED_EXTENSIONS = {'zip', 'conf'}
HTTP200 = 200
HTTP400 = 400

app = Flask(__name__)
log = Logger()
file_fir = os.path.dirname(__file__)
log_dir = os.path.join(file_fir, 'logs')
mkdir(log_dir)

log.init_app(app, {
    'LOG_PATH': log_dir,
    'LOG_NAME': 'flask-run.log',
    'LOG_FORMAT': '{time} {level} {message}',
    'LOG_ROTATION': 3600,
    # 不输出json格式日志
    'LOG_SERIALIZE': False
})
from flask_loguru import logger

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# 上传压缩包的路径
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload_datas')
mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024

logger.info('UPLOAD_FOLDER is {}', UPLOAD_FOLDER)

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


@app.get('/')
def hello():
    return 'hello'


@app.route('/download/<dirname>/<filename>')
def download(dirname, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], dirname)
    return send_from_directory(directory, filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    logger.info('request method is {}', request.method)
    if request.method == 'POST':
        file = request.files['file']
        sofa_name = request.form.get('sofa_name')
        logger.info('sofa_name is {}', sofa_name)
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
            plugin_flag = ''
            if filename.endswith('zip'):
                plugin_flag = get_node_attr(filepath, 'pluginFlag')
            file_url = url_for('download', dirname=sofa_name, filename=filename)
            result = {
                'status': HTTP200,
                'filepath': filepath,
                'file_name': filename,
                'sofa_name': sofa_name,
                'plugin_flag': plugin_flag,
                'msg': 'file_url is {}'.format(file_url)
            }
            logger.info('result {}', result)
            return jsonify(result)
    return html


@app.post("/make_sofa_package")
def make_sofa_package():
    """
    # demo 方法
    # user = User.query.get_or_404(id)
    # user.update_from_json(request.json)
    # db.session.commit()
    # demo 方法
    """
    result = {
        'status': HTTP200,
        'sofa_package': '',
        'msg': 'ok'
    }
    data: dict = request.json
    plugin_infos = [(info.get('sofaPluginFilePath', ''), info.get('htmlFilePath', ''), info.get('router', ''),
                     info.get('module', '')) for info in data['pluginList']]
    try:
        new_zip_path = make_new_zip(data['sofaFilePath'], plugin_infos, data['nginxFilePath'])
        result['new_package_path'] = new_zip_path
    except ValueError as e:
        result['new_package_path'] = ''
        result['msg'] = '{}'.format(e)

    return jsonify(result)


if __name__ == '__main__':
    # 单机测试用
    app.run('0.0.0.0', 5000, False)
