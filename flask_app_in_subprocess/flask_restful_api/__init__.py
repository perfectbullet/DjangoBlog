"""
@FileName：__init__.py.py
@Description：
@Author：zhoujing
@contact：121531845@qq.com
@Time：2023/8/9 22:33
@Department：红石扩大小区
@Website：www.zhoujing.com
@Copyright：©2019-2023 xxx信息科技有限公司
"""


import os
from datetime import timedelta

from flask import Flask
from loguru import logger

from flask_restful_api.api.conf.auth import jwt
from flask_restful_api.api.conf.routes import generate_routes
from flask_restful_api.api.database.database import db
from flask_restful_api.api.db_initializer.db_initializer import create_admin_user, create_super_admin, create_test_user
from flask_restful_api.api.models.models import User


def create_app():

    # Create a flask app.
    app = Flask(__name__)

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # 配置上传路径
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload_datas')
    # 配置最大上传文件
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db_path = os.path.join(os.getcwd(), "test.db")
    print(db_path)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    app.config["JWT_SECRET_KEY"] = "121531845"  # Change this!

    # ######################### 配置 jwt
    jwt.init_app(app)

    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        print('user_identity_lookup', user)
        return user

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        print('user_lookup_callback', _jwt_header, jwt_data)
        user = jwt_data["sub"]
        return User.query.filter_by(id=user['id']).one_or_none()

    # ######################### 配置 jwt


    # Generate routes.
    generate_routes(app)

    logger.info('UPLOAD_FOLDER is {}', app.config['UPLOAD_FOLDER'])

    # Database initialize with app.
    db.init_app(app)

    # Check if there is no database.
    if not os.path.exists(SQLALCHEMY_DATABASE_URI):
        with app.app_context():
            # New db app if no database.
            db.app = app

            # Create all database tables.
            db.create_all()

            # Create default super admin user in database.
            create_super_admin()

            # Create default admin user in database.
            create_admin_user()

            # Create default test user in database.
            create_test_user()

    # Return app.
    return app


if __name__ == '__main__':

    # Create app.
    app = create_app()

    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)
