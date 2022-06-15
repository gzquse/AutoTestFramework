
import datetime
import socket
import json

# socket客户端连接服务器
serveraddr = ("127.0.0.1", 8888)
sk = socket.socket()
sk.connect(serveraddr)

params = {
    'service': 'createOrder',
    'order_dep': '001',
    'order_date': datetime.date.today().strftime("%Y-%m-%d"),
    'order_name': '需求名称',
    'order_sys': 'sys',
    'order_type': 'change',
    'order_desc': '描述信息',
}

# 组装请求报文
# 按照文档中的接口协议约定
json_str = json.dumps(params)
send_str = "%010d%s" % (len(json_str.encode('utf-8')), json_str)
print(send_str)

# str --> bytes
# sendall 他是阻塞，tcp
sk.sendall(send_str.encode('utf-8'))

answer_len = int(sk.recv(10))
print("响应报文长度:", answer_len)

# recv方法是有长度限制，2048作为缓冲，循环接收
content = sk.recv(answer_len).decode('utf-8')
print(content)  # json的字符串 str
print(type(content))  # str

json_dict = json.loads(content)
print(json_dict)  # 解析后的字典
print(type(json_dict))  # 字典

print("响应码:", json_dict['code'])
print("响应信息:", json_dict['msg'])
print("需求单编号:", json_dict['order_id'])

# 不要忘了关闭socket
sk.close()

# 断言
assert json_dict['code'] == '000000', "测试失败"
