#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

# from api.conf.auth import auth
from flask_restful_api.api.database.database import db
from flask_restful_api.api.models.models import JsonData

CODE200 = 200
CODE404 = 404


class JsonAip2(Resource):
    @jwt_required()
    def post(self):
        content, json_id = request.json.get("content"), request.json.get("id")

        if json_id is not None:
            json_data = JsonData.query.filter_by(id=json_id).first()
        else:
            # 新增一个
            json_data = JsonData()

        # Update content.
        json_data.content = content

        # Commit session.
        db.session.add(json_data)
        db.session.commit()
        # db.session.flush()
        msg = 'update or insert JsonData({})'.format(json_data)
        data = {'id': json_data.id, 'content': json_data.content}
        # Return success status.
        return {"code": CODE200, "msg": msg, 'data': data}

    @jwt_required()
    def get(self):
        # Get usernames.
        json_id = request.args.get("id")
        if json_id:
            json_datas: JsonData = JsonData.query.filter_by(id=json_id)
        else:
            json_datas: JsonData = JsonData.query.all()

        if not json_datas:
            return {"code": CODE404, "msg": "未找到数据"}

        data = [{
            "id": jdata.id,
            "content": jdata.content,
        } for jdata in json_datas]
        return {"code": CODE200, "msg": "ok", "data": data}
