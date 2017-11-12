import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
import re
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.login import Login

class CouponTest(unittest.TestCase):
    common_method = Common_method()
    sheet4 = common_method.get_excle_sheet4()
    login = Login()
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def get_myconponList(self,uid,authkey):
        base_url = self.sheet4.cell_value(2,2)
        uid = uid
        authkey = authkey
        timestamp = self.common_method.timestamp
        key_list = [uid,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        postdata ={
            "uid" :uid,
            "timestamp" :timestamp,
            "key" :key,
            "status": self.sheet4.cell_value(2,6),
            "page": "1"
        }
        response_list = requests.post(base_url,data=postdata,verify=False)
        return  response_list


    def test_couponList(self):
        u"测试我的优惠券列表"
        phone = self.sheet4.cell_value (2, 4)
        if re.match (r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
            psw = self.sheet4.cell_value (2, 5)
            login_data = self.login.phone_login (phone, psw)
        else:
            login_data = self.login.wx_login(phone)
        # 从登录接口获取用户id,authkey,用户计算加密
        uid = str (login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        response = self.get_myconponList(uid,authkey)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual (len (result["data"]), 0)

    def test_couponDetail(self):
        u"测试优惠券详情"
        base_url = self.sheet4.cell_value(3,2)
        phone = self.sheet4.cell_value(3, 4)
        if re.match(r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
            psw = self.sheet4.cell_value(3, 5)
            login_data = self.login.phone_login(phone, psw)
        else:
            login_data = self.login.wx_login(phone)
        # 从登录接口获取用户id,authkey,用户计算加密
        uid = str(login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        response_couponlist = self.get_myconponList(uid, authkey)
        result_couponlist = json.loads(response_couponlist.content)
        if result_couponlist["data"]["items"]:
            couponnum = result_couponlist["data"]["items"][0]["couponnum"]
            timestamp = self.common_method.timestamp
            key_list = [uid,timestamp,authkey]
            key = self.common_method.get_key(key_list)
            uuid = result_couponlist["data"]["items"][0]["uuid"]
            params = {
                "couponnum" :couponnum,
                "key" :key,
                "uid" :uid,
                "timestamp" :timestamp,
                "uuid" : uuid
            }
            response = requests.post(base_url,params = params,verify = False)
            result = json.loads(response.content)
        else:
            self.assertEqual(uid,"该用户没有优惠券,无法查看优惠券详情")