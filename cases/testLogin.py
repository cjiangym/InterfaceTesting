import unittest
import requests
import json
import xlrd
import hashlib
import math
from common.common_method import Common_method
from common.login import Login
from common.getKey import Key
from config import serverAddressConfig

#手机号登录、微信登录测试
class LoginTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    login = Login()
    svrAddr = serverAddressConfig.sv_29090

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def login_wx(self):
        pass

    def test_login_01(self):
        u"测试手机号码登录，正确的手机号、密码"
        phone = self.sheet1.cell_value (5, 5)
        psw = self.sheet1.cell_value (5, 6)
        try:
            self.result = self.login.phone_login (phone, psw)  # 手机号登录返回结果
        except:
            self.assertTrue(None,"登录失败")
        data = self.result["data"]
        response_mobile = data["user"]["mobile"]
        self.assertEqual(self.result["status"], 10001)


    def test_login_02(self):
        u"测试手机号码登录，错误密码登录"
        self.phone = self.sheet1.cell_value(6, 5)           # 手机号码
        self.psw = self.sheet1.cell_value(6,6)                      # 密码
        try:
            self.result = self.login.phone_login(self.phone,self.psw)
        except:
            self.assertTrue(None,"登录失败")
        self.assertEqual(self.result["status"],20003)
        self.assertEqual(self.result["msg"],"用户名或密码错误")


    def test_wxlogin_01(self):
        u"微信登录，需要绑定手机号码"
        thirdid = self.sheet1.cell_value(7,5)
        try:
            self.result = self.login.wx_login(thirdid)
        except:
            self.assertTrue(None,"微信登录失败")
        self.assertEqual(self.result["data"]["requirebindmobile"], 1)   # 是否需要绑定的判断条件，为0，不需要绑定,1为需要绑定
        self.assertIs(self.result["data"]["authkey"], "")

    def test_wxlogin_02(self):
        u"微信登录，不需要绑定手机号码"
        thirdid = self.sheet1.cell_value(8, 5)
        try:
            self.result = self.login.wx_login (thirdid)
        except:
            self.assertTrue(None,"微信登录失败")
        self.assertEqual (self.result["data"]["requirebindmobile"], 0)     # 是否需要绑定的判断条件，为0，不需要绑定
        self.assertIsNot (self.result["data"]["authkey"], "")
        self.assertNotEqual (len (self.result["data"]["user"]), 0)



    def test_getUserinfo(self):
        u"登录后获取用户信息userinfo"
        base_url = self.sheet1.cell_value(10,2)
        url = self.svrAddr + base_url
        phone = self.sheet1.cell_value(5,5)
        psw = self.sheet1.cell_value(5, 6)
        try:
            self.result = self.login.phone_login(phone,psw)
        except:
            self.assertTrue(None,"登录失败")
        uid = self.result["data"]["user"]["id"]
        params =  {
            "appversion":serverAddressConfig.version,
            "devcode":serverAddressConfig.devcode,
            "os":serverAddressConfig.os,
            "uid":uid
         }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        user_id = result["data"]["user"]["id"]
        self.assertEqual(user_id,uid)


    def test_getUserstatus(self):
        u"登录后获取用户状态userstatus"
        base_url = self.sheet1.cell_value(11,2)
        url = self.svrAddr + base_url
        phone = self.sheet1.cell_value(11,4)
        psw = self.sheet1.cell_value(11,5)
        try:
            self.result = self.login.phone_login(phone,psw)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        uid = str(self.result["data"]["user"]["id"])
        timestamp = serverAddressConfig.timestamp
        authkey = self.result["data"]["authkey"]
        list_key = [uid,timestamp,authkey]
        key = Key.get_key(self,list_key)
        params = {
            "uid":uid,
            "usertype":self.result["data"]["user"]["type"],    #用户类型（1为手机账号、4为微信账号）,
            "appversion":serverAddressConfig.version,
            "os":serverAddressConfig.os,
            "timestamp":timestamp,
            "key":key
        }
        response = requests.get(url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual (result["data"],None)
