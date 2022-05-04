# -*- coding:utf-8 -*-
"""
模块描述:
 登陆的接口测试用例
作者：Sniper.ZH
"""
import json
import unittest
from ddt import ddt, file_data
import api.KeywordApi as kwa
from commons.Logger import logger
from commons.Decor import case_decor

"""
1.集成unittest完成测试用例和数据驱动的封装
"""


@ddt
class loginInterfaceTestCase(unittest.TestCase):

    @file_data('../testDatas/testdata_interface_login.yaml')
    @case_decor
    def test_login(self, **params):

        # 2：模拟请求
        res = kwa.do_post("/dologin/", data=params.get('data'))

        # 3：断言
        self.assertEqual(200, res.status_code, "登陆通讯失败{}".format(res.status_code))
        print(res.text)
        # print(type(res.text))
        logger.info(type(res.text))
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        self.assertEqual(kwa.get_value(params, 'code'), res.json()['code'], '测试失败')


if __name__ == '__main__':
    unittest.main()

