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
        base_url = self.sheet5.cell_value(4,2)
        phone = self.sheet5.cell_value(4, 4)
        psw = self.sheet5.cell_value(4, 5)
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
            "scene" :"jmg",
            "timestamp" :timestamp,
            "key" :key
        }
        response = requests.post(base_url,params=params,verify=False)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"]["coupon_num"],"")


    def test_myconponList(self):
        u"测试我的优惠券列表"
        base_url = self.sheet5.cell_value(5,2)
        phone = self.sheet5.cell_value(5,4)
        psw = self.sheet5.cell_value(5,5)
        #从登录接口获取用户id,authkey,用户计算加密
        login_data = self.login.phone_login(phone,psw)
        uid = str(login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        timestamp = self.common_method.timestamp
        key_list = [uid,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        postdata ={
            "uid" :uid,
            "timestamp" :timestamp,
            "key" :key,
            "status": self.sheet5.cell_value(5,6),
            "page": "1"
        }
        response = requests.post(base_url,data=postdata,verify=False)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(len(result["data"]),0)

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


