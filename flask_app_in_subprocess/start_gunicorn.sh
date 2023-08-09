#!/bin/bash
gunicorn --config=gunicorn_config.py flask_restful_api:create_app