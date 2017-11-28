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
from common.getKey import Key

class CouponTest(unittest.TestCase):
    common_method = Common_method()
    sheet4 = common_method.get_excle_sheet4()
    sheet5 = common_method.get_excle_sheet5()
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
        key = Key.get_key(self,key_list)
        postdata ={
            "uid" :uid,
            "timestamp" :timestamp,
            "key" :key,
            "status": self.sheet4.cell_value(2,6),
            "page": "1",
            "appversion": self.common_method.version,
            "os" :self.common_method.os,
            "devcode" :self.common_method.devcode
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
        uid = str(login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        response = self.get_myconponList(uid,authkey)
        self.assertEqual(response.status_code,200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual(len (result["data"]),0)

    def test_mygiftcoupons(self):
        u"测试我的兑换代金券列表"
        base_url = self.sheet4.cell_value(4,2)
        phone = self.sheet4.cell_value(4,4)
        psw = self.sheet4.cell_value(4,5)
        if re.match (r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
            psw = self.sheet4.cell_value (2, 5)
            login_data = self.login.phone_login (phone, psw)
        else:
            login_data = self.login.wx_login(phone)
        uid = str(login_data["data"]["user"]["id"])
        authkey = login_data["data"]["authkey"]
        timestamp = self.common_method.timestamp
        key_list = [uid,timestamp,authkey]
        key = Key.get_key(self,key_list)
        params = {
            "uid" :uid,
            "retailid": self.sheet4.cell_value (4, 6),
            "status": self.sheet4.cell_value (4, 7),
            "type" :self.sheet4.cell_value(4,8),
            "page" :self.sheet4.cell_value(4,9),
            "timestamp": timestamp,
            "key" :key
        }
        response = requests.post(base_url,params=params,verify=False)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(len(result["data"]["items"]),0)

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
            key_list = [uid,couponnum,timestamp,authkey]
            key = Key.get_key(self,key_list)
            uuid = result_couponlist["data"]["items"][0]["uuid"]
            params = {
                "couponnum" :couponnum,
                "key" :key,
                "uid" :uid,
                "timestamp" :timestamp,
                "uuid" : uuid,
                "appversion":self.common_method.version
            }
            response = requests.post(base_url,params = params,verify = False)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertNotEqual(result["data"],{})
            self.assertNotEqual(result["data"],"null")
        else:
            self.assertEqual(uid,"该用户没有优惠券,无法查看优惠券详情")