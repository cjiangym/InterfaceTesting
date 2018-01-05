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
from config import  serverAddressConfig

class CouponTest(unittest.TestCase):
    common_method = Common_method()
    sheet4 = common_method.get_excle_sheet(3)
    sheet5 = common_method.get_excle_sheet(4)
    login = Login()
    svrAddr = serverAddressConfig.coupon_29083
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def get_myconponList(self,uid,authkey):
        base_url = self.sheet4.cell_value(2,2)
        timestamp = serverAddressConfig.timestamp
        key_list = [uid,timestamp,authkey]
        key = Key.get_key(self,key_list)
        status = self.sheet4.cell_value (2, 6)
        params_name = ["uid","timestamp","key","status","page","appversion","os","devcode"]
        params_value = [uid,timestamp,key,status,"1",serverAddressConfig.version,serverAddressConfig.os,serverAddressConfig.devcode]
        response_list = self.common_method.post_response(self.svrAddr,base_url,params_name,params_value)
        return  response_list


    def test_couponList(self):
        u"测试我的优惠券列表"
        phone = self.sheet4.cell_value (2, 4)
        try:
            if re.match (r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
                psw = self.sheet4.cell_value (2, 5)
                self.login_data = self.login.phone_login (phone, psw)
            else:
                self.login_data = self.login.wx_login(phone)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        '''从登录接口获取用户id,authkey,用户计算加密'''
        #uid = str(self.login_data["data"]["user"]["id"])
        #authkey = self.login_data["data"]["authkey"]
        uid = "1603491"
        authkey = "nwkXC3dQjUrhYNYi"
        try:
            self.response = self.get_myconponList(uid,authkey)
        except:
            self.assertTrue(None,"获取优惠券列表失败")
        self.assertEqual(self.response.status_code,200)
        result = json.loads (self.response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual(result["data"],None)

    def test_mygiftcoupons(self):
        u"测试我的兑换代金券列表"
        base_url = self.sheet4.cell_value(4,2)
        phone = self.sheet4.cell_value(4,4)
        psw = self.sheet4.cell_value(4,5)
        try:
            if re.match (r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
                self.login_data = self.login.phone_login (phone, psw)
            else:
                self.login_data = self.login.wx_login(phone)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        uid = str(self.login_data["data"]["user"]["id"])
        authkey = self.login_data["data"]["authkey"]
        timestamp = serverAddressConfig.timestamp
        key_list = [uid,timestamp,authkey]
        key = Key.get_key(self,key_list)
        retailid = self.sheet4.cell_value (4, 6),
        status = self.sheet4.cell_value (4, 7),
        type = self.sheet4.cell_value (4, 8),
        params_name = ["uid","retailid","status","type","page","timestamp","key","appversion"]
        params_value = [uid,retailid,status,type,"1",serverAddressConfig.timestamp,key,serverAddressConfig.version]
        response = self.common_method.post_response(self.svrAddr,base_url,params_name,params_value)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual(result["data"],None)


    def test_couponDetail(self):
        u"测试优惠券详情"
        base_url = self.sheet4.cell_value(3,2)
        phone = self.sheet4.cell_value(3, 4)
        psw = self.sheet4.cell_value (3, 5)
        try:
            if re.match(r"\d", phone):  # 是手机号则使用手机好登录，否则使用微信登录
                self.login_data = self.login.phone_login(phone, psw)
            else:
                self.login_data = self.login.wx_login(phone)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        # 从登录接口获取用户id,authkey,用户计算加密
        uid = str(self.login_data["data"]["user"]["id"])
        authkey = self.login_data["data"]["authkey"]
        try:
            self.response_couponlist = self.get_myconponList(uid, authkey)
        except:
            self.assertTrue(None,"获取优惠券列表失败...")
        result_couponlist = json.loads(self.response_couponlist.content)
        '''查看列表的第1张优惠券详情'''
        if result_couponlist["data"]["items"]:
            couponnum = result_couponlist["data"]["items"][0]["couponnum"]
            timestamp = serverAddressConfig.timestamp
            key_list = [uid,couponnum,timestamp,authkey]
            key = Key.get_key(self,key_list)
            uuid = result_couponlist["data"]["items"][0]["uuid"]
            params_name = ["couponnum","key","uid","timestamp","uuid","appversion"]
            params_value = [couponnum,key,uid,timestamp,uuid,serverAddressConfig.version]
            response = self.common_method.post_response(self.svrAddr,base_url,params_name,params_value)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertNotEqual(result["data"],{})
            self.assertNotEqual(result["data"],None)
        else:
            self.assertTrue(None,"该用户没有优惠券,无法查看优惠券详情")