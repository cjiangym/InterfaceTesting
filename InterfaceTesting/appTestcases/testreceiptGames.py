import unittest
import requests
import json
import xlrd
import hashlib
import math
from InterfaceTesting.run_all_cases import Common_method

class ReceiptGamesTests(unittest.TestCase):
    common_method = Common_method()
    sheet3 = common_method.get_excle_sheet3()
    dict = common_method.get_common_params()
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_receipt(self):
        u"测试拍立赚上传小票"
        base_url = self.sheet3.cell_value(2,2)
        appversion = self.dict["version"]
        timestamp = self.dict["timestamp"]
        os = self.dict["os"]
        devcode = self.dict["devcode"]
        pages = "1"    #页码
        cityid = self.sheet3.cell_value(2,4)
        cityname = self.sheet3.cell_value(2,5)
        lon = self.sheet3.cell_value(2,6)
        lat = self.sheet3.cell_value(2,7)
        uid = self.sheet3.cell_value(2,8)
        key_list = []
        key = self.common_method.get_key(key_list)
        session = requests.session()           #多个接口，使用session关联


