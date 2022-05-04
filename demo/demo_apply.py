# -*- coding:utf-8 -*-
"""
模块描述:
  需求申请的测试代码
作者：Sniper.ZH
"""
import requests

# 先登陆
# 必须使用session，关联登陆和需求申请2个接口
session = requests.session()
login_url = "http://127.0.0.1:8001/dologin/"
data = {
    "username": "admin",
    "pwd": "123456",
    "randomCode": "1234"
}

# 2：模拟请求
res = session.post(login_url, data=data)
print(res.status_code)

if res.status_code == 200 and res.json().get('code') == 0:
    # 需求申请
    print("{:*^50s}".format("第1个测试用例: 正例"))
    apply_url = "http://127.0.0.1:8001/commit_order/"
    apply_data = {
        'order_dep': '001',
        'order_date': '2021-08-29',
        'order_name': '需求名称',
        'order_sys': '关联系统',
        'order_type': 'new',
        'order_desc': '描述信息',
    }
    res = session.post(apply_url, data=apply_data)

    print(res.status_code)
    print(res.text)
    assert res.status_code == 200, "通讯失败"
    assert res.json()['code'] == 0, "测试失败"

    print("{:*^50s}".format("第2个测试用例: 反例 部门未输入"))
    apply_url = "http://127.0.0.1:8001/commit_order/"  # 192.168.3.1
    apply_data = {
        # 'order_dep': '001',
        'order_date': '2021-08-29',
        'order_name': '需求名称',
        'order_sys': '关联系统',
        'order_type': 'new',
        'order_desc': '描述信息',
    }
    res = session.post(apply_url, data=apply_data)

    print(res.status_code)
    print(res.text)
    assert res.status_code == 200, "通讯失败"
    assert res.json()['code'] == -1, "测试失败"

    print("{:*^50s}".format("第3个测试用例: 反例 日期格式非法"))
    apply_url = "http://127.0.0.1:8001/commit_order/"
    apply_data = {
        'order_dep': '001',
        'order_date': '123123',
        'order_name': '需求名称',
        'order_sys': '关联系统',
        'order_type': 'new',
        'order_desc': '描述信息',
    }
    res = session.post(apply_url, data=apply_data)

    print(res.status_code)
    print(res.text)
    assert res.status_code == 200, "通讯失败"
    assert res.json()['code'] == 500001, "测试失败"
