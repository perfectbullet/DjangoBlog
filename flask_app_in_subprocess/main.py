#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import timedelta
from flask import Flask

from api.conf.routes import generate_routes
from api.database.database import db
from api.db_initializer.db_initializer import (create_admin_user,
                                               create_super_admin,
                                               create_test_user)
from api.conf.auth import jwt
from api.models.models import User


def create_app():
    # Create a flask app.
    app = Flask(__name__)

    # Set debug true for catching the errors.
    app.config['DEBUG'] = True

    # Set database url.

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db_path = os.path.join(os.getcwd(), "test2.db")
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

    # Database initialize with app.
    db.init_app(app)

    # Check if there is no database.
    if not os.path.exists(db_path):
        # New db app if no database.
        db.app = app

        # Create all database tables.
        print('create all')
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
    app.run(port=5000, debug=True, host='0.0.0.0', use_reloader=True)
