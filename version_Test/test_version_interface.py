import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.login import Login

class CouponTest(unittest.TestCase):
    login = Login()
    common_method = Common_method()
    sheet4 = common_method.get_excle_sheet4()

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_mygiftcoupons(self):
        u"测试我的优惠券列表"
        base_url = ""
        phone = self.sheet4.cell_value(2,4)
        psw = self.sheet4.cell_value(2,5)
        response_dict = self.login.phone_login(phone,psw)
        uid = str(response_dict["user_id"])
        authkey = response_dict["authkey"]
        timestamp = self.common_method.timestamp
        key_list = [uid,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        params = {
            "uid" :uid,
            "retailid": self.sheet4.cell_value (2, 6),
            "status": self.sheet4.cell_value (2, 7),
            "type" :self.sheet4.cell_value(2,8),
            "page" :self.sheet4.cell_value(2,9),
            "timestamp": timestamp,
            "key" :key
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(response)
        print(result)
        #self.assertEqual(result["data"]["items"])

    def test_mygift_list(self):
        u"测试我的兑换列表"
        base_url = ""
        params = {
            "uid" : self.sheet4.cell_value (3, 2),
            "giftType" : self.sheet4.cell_value (3, 4),
            "pages" : self.sheet4.cell_value (3, 5),
            "pageSiz" : self.sheet4.cell_value (3, 6),
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(result)
        self.assertNotEqual(result["data"]["userGiftList"][0]["trade_money"],"")
        self.assertNotEqual (result["data"]["userGiftList"][0]["discount_value"], "")


