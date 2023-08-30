import os
from datetime import datetime
from loguru import logger
today = datetime.now()


file_dir = os.path.dirname(__file__)
log_dir = os.path.join(file_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)

logger.add(os.path.join(log_dir, "log-upload.log"), rotation="1 MB")


def log(msg):
    logger.info(msg)
