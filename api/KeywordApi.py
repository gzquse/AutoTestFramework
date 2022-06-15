import json
import json as json_lib
import socket

import requests
import commons.Config as config
from commons.Logger import logger
import jsonpath


def do_post(path, data=None, headers=None, json=None, create_session=False, session=None):
    print("post requests:")
    params = data if data is not None else json
    print("请求参数:", params)
    logger.info("请求参数")
    logger.info(params)

    if create_session and session:
        raise ValueError("create_session和session不能同时使用.")

    if create_session is True:
        req = requests.session()
    elif session is not None:
        req = session
    else:
        req = requests

    res = req.post(config.get_config('options.url') + path, data=data, json=json, headers=headers)
    print(res.status_code)
    logger.info("响应码: " + str(res.status_code))

    # 输出相应结果
    contentType = res.headers.get('Content-Type')
    if contentType == 'application/json':
        resContext = json_lib.dumps(res.json(), indent=2, ensure_ascii=False)
    elif contentType.startswith("text/html"):
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


def do_get(path, params=None, headers=None, create_session=False, session=None):
    print("get requests:")
    print("请求参数:", params)
    logger.info("请求参数")
    logger.info(params)

    if create_session and session:
        raise ValueError("create_session和session不能同时使用.")

    if create_session is True:
        req = requests.session()
    elif session is not None:
        req = session
    else:
        req = requests

    res = req.post(config.get_config('options.url') + path, params=params, headers=headers)
    print(res.status_code)
    logger.info("响应码: " + str(res.status_code))

    # 输出相应结果
    contentType = res.headers.get('Content-Type')
    logger.info(contentType)
    if contentType == 'application/json':
        resContext = json_lib.dumps(res.json(), indent=2, ensure_ascii=False)
    elif contentType.startswith("text/html"):
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


def get_value(content, key):
    return jsonpath.jsonpath(content, "$..{}".format(key))[0]


def socket_trasfer(params):
    logger.info("socket请求...begin...")
    serveraddr = (config.get_config('socket.host'), int(config.get_config('socket.port')))
    sk = socket.socket()
    sk.connect(serveraddr)

    # 组装请求报文
    # 按照文档中的接口协议约定
    json_str = json.dumps(params)
    send_str = "%010d%s" % (len(json_str.encode('utf-8')), json_str)
    logger.info(send_str)

    # str --> bytes
    # sendall 他是阻塞，tcp
    sk.sendall(send_str.encode('utf-8'))

    answer_len = int(sk.recv(10))
    logger.info("响应报文长度:" + str(answer_len))

    # recv方法是有长度限制，2048作为缓冲，循环接收
    content = sk.recv(answer_len).decode('utf-8')

    # 我们现在的场景只有json数据，如果有其他格式的内容，自己优化
    json_dict = json.loads(content)
    logger.info(str(json_dict))  # 解析后的字典

    # 不要忘了关闭socket
    sk.close()
    logger.info("socket请求...end...")

    return json_dict
