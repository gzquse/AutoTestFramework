# -*- coding:utf-8 -*-
"""
模块描述:
  关键字驱动方法的类
作者：Sniper.ZH
"""
import json

import requests
import commons.Config as config
from commons.Logger import logger
import jsonpath


def do_post(path, data, create_session=False, session=None):
    print("post requests:")
    print("请求参数:", data)
    logger.info("请求参数")
    logger.info(data)

    if create_session and session:
        raise ValueError("create_session和session不能同时使用.")

    if create_session is True:
        req = requests.session()
    elif session is not None:
        req = session
    else:
        req = requests

    res = req.post(config.get_config('options.url') + path, data=data)
    print(res.status_code)
    logger.info("响应码: " + str(res.status_code))

    # 输出相应结果
    contentType = res.headers.get('Content-Type')
    if contentType == 'application/json':
        resContext = json.dumps(res.json(), indent=2, ensure_ascii=False)
    elif contentType == "text/html":
        resContext = res.text[:1000]
    else:
        resContext = "未定义"

    print("响应报文:")
    print(resContext)
    logger.info(resContext)
    if create_session is True or session is not None:
        return res, req
    else:
        return res


def do_get():
    pass


def get_value(content, key):
    return jsonpath.jsonpath(content, "$..{}".format(key))[0]
