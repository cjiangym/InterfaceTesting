import unittest
import requests
import json
import xlrd
import hashlib
import math
from common.common_method import Common_method
from common.login import Login


#手机号登录、微信登录测试
class LoginTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()
    login = Login()
    phone = sheet1.cell_value (5, 5)
    psw = sheet1.cell_value (5, 6)
    response = login.phone_login (phone, psw)          #手机号登录返回结果

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def login_wx(self):
        pass

    def test_login_01(self):
        u"测试手机号码登录，正确的手机号、密码"
        if self.response ==200:
            result = json.loads (self.response.content)
            if result["data"]:
                print(self.response.url)
                data = result["data"]
                status = result["status"]
                response_mobile = data["user"]["mobile"]
                self.assertEqual(status, 10001)
                print(result)
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(self.response.status_code,200)

    def test_login_02(self):
        u"测试手机号码登录，错误密码登录"
        self.phone = str(math.floor(self.sheet1.cell_value(6, 5)))  # 手机号码
        self.psw = self.sheet1.cell_value(6, 6)                     # 密码
        password_md5 = hashlib.md5 (self.psw.encode ("utf-8")).hexdigest ()  # 密码通过md5加密
        login_response = self.login.phone_login(self.phone,self.psw)
        if login_response ==200:
            result = json.loads (login_response.content)
            if result["data"]:
                print (self.response.url)
                self.assertEqual(result["status"],20003)
                self.assertEqual(result["msg"],"用户名或密码错误")
                print (result)
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(login_response.status_code,200)

    def test_wxlogin_01(self):
        u"微信登录，需要绑定手机号码"
        thirdid = self.sheet1.cell_value(7,5)
        response = self.login.wx_login(thirdid)
        if response.status_code ==200:
            result = json.loads (response.content)
            if result["data"]:
                print (response.url)
                print (result)
                self.assertEqual (result["data"]["requirebindmobile"], 1)  # 是否需要绑定的判断条件，为0，不需要绑定,1为需要绑定
                self.assertIs (result["data"]["authkey"], "")
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(response.status_code,200)


    def test_wxlogin_02(self):
        u"微信登录，不需要绑定手机号码"
        thirdid = self.sheet1.cell_value (8, 5)
        response = self.login.wx_login (thirdid)
        if response.status_code ==200:
            result = json.loads (response.content)
            if result["data"]:
                autherkey = result["data"]["authkey"]
                is_bind = result["data"]["requirebindmobile"]  # 是否需要绑定的判断条件，为0，不需要绑定
                self.assertEqual (is_bind, 0)
                self.assertIsNot (autherkey, "")
                self.assertNotEqual (len (result["data"]["user"]), 0)
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(response.status_code,200)



    def test_getUserinfo(self):
        u"登录后获取用户信息userinfo"
        base_url = self.sheet1.cell_value(10,2)
        appversion = self.common_method.version
        devcode = self.common_method.devcode
        os = self.common_method.os
        self.phone = self.sheet1.cell_value (5, 5)
        self.psw = self.sheet1.cell_value (5, 6)
        if self.response.status_code ==200:
            login_result = json.loads(self.response.content)
            if login_result["data"]:
                uid = login_result["data"]["user"]["id"]
                params =  {
                    "appversion":appversion,
                    "devcode":devcode,
                    "os":os,
                    "uid":uid
                }
                response = requests.get (base_url, params=params)
                print (response.url)
                result = json.loads (response.content)
                user_id = result["data"]["user"]["id"]
                self.assertEqual (user_id, int (uid))
            else:self.assertEqual(login_result["msg"],0)
        else:
            self.assertEqual(self.login_response.status_code,200)


    def test_getUserstatus(self):
        u"登录后获取用户状态userstatus"
        base_url = self.sheet1.cell_value(11,2)
        if self.response.status_code ==200:
            login_result = json.loads(self.response.content)
            if login_result["data"]:
                uid = str(login_result["data"]["user"]["id"])
                usertype = login_result["data"]["user"]["type"]    #用户类型（1为手机账号、4为微信账号）
                appversion = self.common_method.version
                devcode = self.common_method.devcode
                os = self.common_method.os
                timestamp = self.common_method.timestamp
                authkey = login_result["data"]["authkey"]
                key_list = [uid,timestamp,authkey]
                key = self.common_method.get_key(key_list)
                params = {
                    "uid":uid,
                    "usertype":usertype,
                    "appversion":appversion,
                    "os":os,
                    "timestamp":timestamp,
                    "key":key
                }
                response = requests.get(base_url,params=params)
                print(response.url)
                self.assertEqual(response.status_code,200)
                result = json.loads(response.content)
                self.assertEqual(result["status"],10001)
                self.assertNotEqual(len(result["data"]),0)
            else:
                self.assertEqual(login_result["msg"],0)
        else:
            self.assertEqual(self.response.status_code,200)
