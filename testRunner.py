# -*- coding:utf-8 -*-
"""
模块描述:
  测试执行器
作者：Sniper.ZH
"""
import datetime
import os
import unittest
from api.MyHTMLTestRunner import HTMLTestRunner
import commons.Config as config

ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
reports_path = config.get_config('reports.path')
report_file = os.path.join(reports_path, "test_report_{}.html".format(ts))

# 如果目录不存在，创建
if not os.path.exists(reports_path):
    os.mkdir(reports_path)

with open(report_file, "wb") as reportFile:
    discorver = unittest.defaultTestLoader.discover(
        start_dir=config.get_config('reports.casespath'),
        pattern="{}*.py".format(config.get_config('reports.casespartten'))
    )
    runner = HTMLTestRunner(
        title=config.get_config('reports.title'),
        description=config.get_config('reports.desc'),
        stream=reportFile
    )
    runner.run(discorver)


# 自动发邮件 、自动发短信
