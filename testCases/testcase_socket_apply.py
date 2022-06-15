
import unittest
from ddt import ddt, file_data
import api.KeywordApi as kwa
import commons.Config as config
from commons.Decor import case_decor
from api.DataBaseApi import DataBaseApi


@ddt
class applySocketTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 查询现在数据库中的最大id
        cls.dba = DataBaseApi()
        cls.max_id = cls.dba.queryMaxId()

    @classmethod
    def tearDownClass(cls) -> None:
        # 清除测试数据
        cls.dba.clearTestData(cls.max_id)
        # 关闭数据库连接
        cls.dba.conn.close()

    @file_data("../testDatas/testdata_socket_apply_normal.yaml")
    @case_decor
    def test_apply_normal(self, **params):
        # 提交需求申请
        req_params = params.get('data')
        req_params['service'] = 'createOrder'
        res_json = kwa.socket_trasfer(req_params)
        # 用例断言
        self.assertEqual('000000', res_json['code'])

        # 数据级断言
        new_id = res_json['order_id']
        orderInfo = self.dba.queryOrderById(new_id)
        print("order:", orderInfo)
        self.assertEqual(orderInfo[1], kwa.get_value(params, 'order_name'))
        self.assertEqual(orderInfo[2], kwa.get_value(params, 'order_type'))
        self.assertEqual(orderInfo[3], kwa.get_value(params, 'order_dep'))
        self.assertEqual(orderInfo[4].strftime("%Y-%m-%d"), kwa.get_value(params, 'order_date'))
        self.assertEqual(orderInfo[5], kwa.get_value(params, 'order_sys'))
        self.assertEqual(orderInfo[6], kwa.get_value(params, 'order_desc'))
        self.assertEqual(orderInfo[7], '0')

    @file_data("../testDatas/testdata_socket_apply_error.yaml")
    @case_decor
    def test_apply_error(self, **params):
        # 查询数据库最大id
        max_id = self.dba.queryMaxId()
        # 提交需求申请
        req_params = params.get('data')
        if 'service' not in req_params:
            req_params['service'] = 'createOrder'
        res_json = kwa.socket_trasfer(req_params)
        # 用例断言
        self.assertEqual(kwa.get_value(params, 'code'), res_json['code'])

        # 断言一下，最大id没有变化
        self.assertEqual(max_id, self.dba.queryMaxId())


if __name__ == '__main__':
    unittest.main()
