
import unittest
from ddt import ddt, file_data
from commons.Decor import case_decor
import api.KeywordApi as kwa
from api.DataBaseApi import DataBaseApi


@ddt
class OrderQueryTestCast(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dba = DataBaseApi()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.dba.conn.close()

    @file_data('../testDatas/testdata_interface_order_query_normal.yaml')
    @case_decor
    def test_normal(self, **params):
        req_params = params.get('data')

        data_total = self.dba.queryOrderCount(req_params)
        per_page = req_params.get('limit')

        # 总页数
        pages = data_total // per_page + 1
        print("总记录数: {}, 总页数{}".format(data_total, pages))
        for page in range(1, pages+1):
            print("当前测试第{}页".format(page))
            req_params['page'] = page
            # 模拟请求
            res = kwa.do_post('/orderQueryApi/', json=req_params)
            # 断言
            self.assertEqual(200, res.status_code)
            self.assertEqual(0, kwa.get_value(res.json(), 'code'))

            # 断言总记录数
            self.assertEqual(data_total, kwa.get_value(res.json(), 'count'), '总记录数不符')

            # 断言查询结果的数据条数，必须不超过limit
            data_count = len(kwa.get_value(res.json(), 'data'))
            # 如果不是最后一页，data中数据的数量必须等于limit
            self.assertTrue(per_page >= data_count)
            if page < pages:
                self.assertEqual(per_page, data_count)

            for order in kwa.get_value(res.json(), 'data'):
                if 'order_dep' in req_params:
                    self.assertEqual(req_params.get('order_dep'), order.get('dep'))
                if 'order_type' in req_params:
                    self.assertEqual(req_params.get('order_type'), order.get('type'))
                if 'order_date' in req_params:
                    self.assertEqual(req_params.get('order_date'), order.get('date'))

    @file_data('../testDatas/testdata_interface_order_query_error.yaml')
    @case_decor
    def test_error(self, **params):
        req_params = params.get('data')
        # 模拟请求
        res = kwa.do_post('/orderQueryApi/', json=req_params)
        # 断言
        self.assertEqual(200, res.status_code)
        self.assertEqual(kwa.get_value(params, 'code'), kwa.get_value(res.json(), 'code'))


if __name__ == '__main__':
    unittest.main()
