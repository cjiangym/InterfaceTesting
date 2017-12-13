import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.getKey import Key


class UpdateUserTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def updateUser(self,base_url,uid,update_name,update_value):
        #修改个人资料
        devcode = self.common_method.devcode
        key_list =[uid,devcode]
        key = Key.get_key(self,key_list)
        params = {
            "appversion":self.common_method.version,
            "id":uid,
            "devcode":devcode,
            update_name:update_value,
            "key":key
        }
        response = requests.get(base_url,params=params)
        return response

    def test_update_01_Logo(self):
        u"测试修改头像"
        base_url = self.sheet1.cell_value(48,2)
        uid = self.sheet1.cell_value(48,4)
        logopath = self.sheet1.cell_value(48,5)
        response = self.updateUser(base_url,uid,"logopath",logopath)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        assert_result = int(self.sheet1.cell_value(48,6))
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual (result["data"],"null")
        self.assertNotEqual(result["data"]["user"],{})
        self.assertEqual(result["data"]["user"]["id"],assert_result)


