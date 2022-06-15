
import datetime
import unittest
from ddt import ddt, file_data
from bs4 import BeautifulSoup
import api.KeywordApi as kwa
import commons.Config as config
from commons.Decor import case_decor
from api.DataBaseApi import DataBaseApi


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

    @file_data("../testDatas/testdata_interface_orderQuery_normal.yaml")
    @case_decor
    def test_apply_normal(self, **params):
        # 提交需求申请
        res, session = kwa.do_post('/commit_order/', data=params.get('data'), session=self.session)
        # 用例断言
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, res.json()['code'])

        # 调用需求详情页面
        response, s = kwa.do_get('/info_order/', params={'oid': res.json()['order_id']}, session=self.session)
        print(response)

        # 断言
        self.assertEqual(200, response.status_code)

        # 解析网页
        soup = BeautifulSoup(response.content, features='lxml')

        elements = soup.select('.layui-form-mid')
        for element in elements:
            print(element.text)

        # 断言网页内容是否符合需求
        self.assertEqual(res.json()['order_id'], int(elements[0].text))  # id
        self.assertEqual(kwa.get_value(params, 'order_name'), elements[1].text)  # 名称
        self.assertEqual(kwa.get_value(params, 'assert_dep'), elements[2].text)  # 部门
        self.assertEqual(kwa.get_value(params, 'order_desc'), elements[7].text)  # 描述
        expact_date = datetime.datetime.strptime(kwa.get_value(params, 'order_date'), "%Y-%m-%d").strftime("%Y年%m月%d日")
        # 2021年09月03日 2021-09-03
        self.assertEqual(expact_date, elements[5].text)


if __name__ == '__main__':
    unittest.main()