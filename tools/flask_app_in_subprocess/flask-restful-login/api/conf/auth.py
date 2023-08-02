#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth

# 过期的版本
# from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# from authlib.jose import jwt, JoseError
from authlib.jose import JsonWebToken
# JWT creation.
# jwt = JsonWebToken("top secret!", expires_in=3600)


jwt = JsonWebToken(['RS256'])

# Refresh token creation.
refresh_jwt = JsonWebToken(['RS256'])

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
