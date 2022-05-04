# -*- coding:utf-8 -*-
"""
模块描述:
  日志收集模块
作者：Sniper.ZH
"""
import logging.config
import os

fmt = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

# 找到logs目录的绝对路径
base_path = os.path.dirname(os.path.dirname(__file__))
log_path = os.path.join(base_path, 'logs')

# 判断一下logs目录不存在，创建出来
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_file = os.path.join(log_path, "debug.log")

file_handler = logging.handlers.RotatingFileHandler(
    # 'debug.log',
    log_file,
    backupCount=10,
    encoding='utf-8'
)

logging.basicConfig(
    format=fmt,
    datefmt=datefmt,
    handlers=[file_handler],
    level=logging.INFO
)

# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL

logger = logging.getLogger()
