import logging
import os
from logging.handlers import RotatingFileHandler

logs_path = '../logs/etl_logs.log'

os.makedirs(os.path.dirname(logs_path), exist_ok=True)

logger = logging.getLogger('etl_application')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler(logs_path, maxBytes=20000000, backupCount=5, mode='a')
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)
