
import json
import unittest
from ddt import ddt, file_data
import api.KeywordApi as kwa
from commons.\
    Logger import logger


@ddt
class loginInterfaceTestCase(unittest.TestCase):

    @file_data('../testDatas/testdata_interface_login.yaml')
    def test_login(self, **params):
        print("{:*^50s}".format("the first correct answer"))
        path = "/dologin/"
        data = {
            "username": params['username'],
            "pwd": params['password'],
            "randomCode": "1234"
        }

        # 2：send request
        res = kwa.do_post(path, data)

        # 3：assert
        self.assertEqual(200, res.status_code, "fail:{}".format(res.status_code))
        print('text', res.text)
        # print(type(res.text))
        logger.info(type(res.text))
        # logger.info(res.text)
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        self.assertEqual(params['code'], res.json()['code'], 'failed')


if __name__ == '__main__':
    unittest.main()

