# -*- coding:utf-8 -*-
"""
模块描述:
  用户登陆接口测试
  # 1.f12开发者工具
  # 2.fiddler抓包工具
  # 3.接口文档
作者：Sniper.ZH
"""
import requests

# 线性代码
# 接口自动化测试领域的Hello World
# 1：确认请求地址、参数、请求方法等
print("{:*^50s}".format("第1个测试用例: 正例"))
url = "http://127.0.0.1:8001/dologin/"
data = {
    "username": "admin",
    "pwd": "123456",
    "randomCode": "1234"
}

# 2：模拟请求
res = requests.post(url, data=data)
print(res.status_code)

# 3：断言
assert res.status_code == 200, "登陆通讯失败{}".format(res.status_code)
print(res.text)
assert res.json()['code'] == 0, "测试失败"

print("{:*^50s}".format("第2个测试用例: 反例"))
data = {
    "username": "admin",
    "pwd": "1234561",
    "randomCode": "1234"
}

# 模拟请求
res = requests.post(url, data=data)
print(res.status_code)

# 断言
assert res.status_code == 200, "登陆通讯失败{}".format(res.status_code)
print(res.text)
assert res.json()['code'] == 11, "测试失败"
