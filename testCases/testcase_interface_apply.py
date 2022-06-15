
import json
import unittest
from ddt import ddt, file_data
import api.KeywordApi as kwa
import commons.Config as config
from commons.Decor import case_decor
from api.DataBaseApi import DataBaseApi

# 1: 还原测试现场、避免产生测试过程垃圾数据
# 2: 数据级断言


@ddt
class applyInterfaceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 查询现在数据库中的最大id
        cls.dba = DataBaseApi()
        cls.max_id = cls.dba.queryMaxId()

        # 先登陆
        login_data = {
            "username": config.get_config('loginuser.name'),
            "pwd": config.get_config('loginuser.pass'),
            "randomCode": "1234"
        }
        res, session = kwa.do_post("/dologin/", data=login_data, create_session=True)
        if res.status_code == 200 and res.json()['code'] == 0:
            cls.session = session

    @classmethod
    def tearDownClass(cls) -> None:
        # 清除测试数据
        cls.dba.clearTestData(cls.max_id)
        # 关闭数据库连接
        cls.dba.conn.close()

    @file_data("../testDatas/testdata_interface_apply_normal.yaml")
    @case_decor
    def test_apply_normal(self, **params):
        # 提交需求申请
        res, session = kwa.do_post('/commit_order/', data=params.get('data'), session=self.session)
        # 用例断言
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()['code'])

        # 数据级断言
        new_id = res.json()['order_id']
        orderInfo = self.dba.queryOrderById(new_id)
        print("order:", orderInfo)
        self.assertEqual(orderInfo[1], kwa.get_value(params, 'order_name'))
        self.assertEqual(orderInfo[2], kwa.get_value(params, 'order_type'))
        self.assertEqual(orderInfo[3], kwa.get_value(params, 'order_dep'))
        self.assertEqual(orderInfo[4].strftime("%Y-%m-%d"), kwa.get_value(params, 'order_date'))
        self.assertEqual(orderInfo[5], kwa.get_value(params, 'order_sys'))
        self.assertEqual(orderInfo[6], kwa.get_value(params, 'order_desc'))
        self.assertEqual(orderInfo[7], '0')

    @file_data("../testDatas/testdata_interface_apply_error.yaml")
    @case_decor
    def test_apply_error(self, **params):
        # 查询数据库最大id
        max_id = self.dba.queryMaxId()
        # 提交需求申请
        res, session = kwa.do_post('/commit_order/', data=params.get('data'), session=self.session)
        # 用例断言
        self.assertEqual(200, res.status_code)
        self.assertEqual(kwa.get_value(params, 'code'), res.json()['code'])

        # 断言一下，最大id没有变化
        self.assertEqual(max_id, self.dba.queryMaxId())


if __name__ == '__main__':
    unittest.main()
