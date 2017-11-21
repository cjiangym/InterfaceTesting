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
    sheet5 = common_method.get_excle_sheet5()

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_sendcoupons(self):
        u"测试发送代金券"
        base_url = "https://sv.ismartgo.cn/couponsv/appcoupon/sendActivityCoupon.do"
        phone = "13450244170"
        psw = "123456"
        login_data = self.login.phone_login(phone, psw)
        uid = str(login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        #uid = "1799100"                                 #uid = "15500221"
        #authkey = "xpeRm32QW17pu3FZ"                     #authkey = "GWtk7sLgTvFHjkyB"
        timestamp = self.common_method.timestamp
        key_list = [uid,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        params = {
            "uid" : uid,
            "couponType" :1,
            "discountVal" :"9.99",
            "scene" :"test_jmg",
            "timestamp" :timestamp,
            "key" :key
        }
        response = requests.post(base_url,params=params,verify=False)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"]["coupon_num"],"")


