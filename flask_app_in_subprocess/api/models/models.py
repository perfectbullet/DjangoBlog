#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import g
from flask_jwt_extended import create_access_token

from api.conf.auth import jwt
from api.database.database import db


class JsonData(db.Model):
    """
    json数据表
    """
    # data id
    id = db.Column(db.Integer, primary_key=True)
    # data content
    content = db.Column(db.String, default='')
    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # data content
    content2 = db.Column(db.String, default='')

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<JsonData(id='%s', content='%s')>" % (
            self.id,
            self.content,
        )


class User(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # User name.
    username = db.Column(db.String(length=80))

    # User password.
    password = db.Column(db.String(length=80))

    # User email address.
    email = db.Column(db.String(length=80))

    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Unless otherwise stated default role is user.
    user_role = db.Column(db.String, default="user")

    # Generates auth token.
    def generate_auth_token(self, permission_level):

        # Check if admin.
        if permission_level == 1:

            # Generate admin token with flag 1.
            token = create_access_token({"id": self.id, "email": self.email, "admin": 1})
            # Return admin flag.
            return token

            # Check if admin.
        elif permission_level == 2:

            # Generate admin token with flag 1.
            token = create_access_token({"id": self.id, "email": self.email, "admin": 2})
            # Return admin flag.
            return token

        # Return normal user flag.
        return create_access_token({"id": self.id, "email": self.email, "admin": 0})

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.email,
            self.created,
        )


class Blacklist(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Blacklist id.
    id = db.Column(db.Integer, primary_key=True)

    # Blacklist invalidated refresh tokens.
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):

        # This is only for representation how you want to see refresh tokens after query.
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
            self.id,
            self.refresh_token,
        )
