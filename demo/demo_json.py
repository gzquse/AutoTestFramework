# -*- coding:utf-8 -*-
"""
模块描述:
  需求申请查询api接口
作者：Sniper.ZH
"""
import json

import requests

# 请求地址和参数
url = 'http://127.0.0.1:8001/orderQueryApi/'
data = {
  "page": 1,
  "limit": 30,
  "order_dep": "001",
  "order_type": "new",
  # "order_date": "2020-10-17"
}

# 模拟请求
res = requests.post(url, json=data)

print(res.status_code)
# print(res.text)
# print(json.dumps(res.json(), indent=2, ensure_ascii=False))

# 断言
assert res.status_code == 200
for order in res.json()['data']:
    print(order)
    assert order['dep'] == data['order_dep']
    assert order['type'] == data['order_type']
