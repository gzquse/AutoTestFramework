# -*- coding:utf-8 -*-
"""
模块描述:
  装饰器定义模块
作者：Sniper.ZH
"""
import functools
import json
import datetime
import random

from commons.Logger import logger


def case_decor(_func):
    @functools.wraps(_func)
    def inner(*args, **kwargs):
        """
        测试用例装饰器
        :return:
        """
        logger.info("-"*50)
        caseName = type(args[0]).__name__
        caseDesc = kwargs.get('description')
        logger.info("{}{}...begin...".format(caseName, caseDesc))

        print("用例描述:", caseDesc)
        print("入口参数:")
        logger.info("入口参数:")
        datas = kwargs['data']
        for key in datas.keys():

            # 数据计算和加工
            # 第一种方式 字符串判断表达式

            if datas[key].startswith('<') and datas[key].endswith('>'):
                datas[key] = eval(datas[key][1:-1])

            print(key, ":", datas[key])
            logger.info(key + " : " + str(datas[key]))

        res = _func(*args, **kwargs)

        logger.info("{}{}...end...".format(caseName, caseDesc))
        return res
    return inner

