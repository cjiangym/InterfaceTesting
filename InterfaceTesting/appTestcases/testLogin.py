import unittest
import requests
import json
import xlrd
import hashlib
import math

from InterfaceTesting.run_all_cases import Common_method


#手机号登录、微信登录测试
class LoginTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()
    dict = common_method.get_common_params()
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def phone_login(self):
        base_url = self.sheet1.cell_value(5, 2)  #接口地址
        phone = str(math.floor(self.sheet1.cell_value(5, 5)))   # 手机号码
        password = self.sheet1.cell_value(5, 6)      # 密码
        userId = str(math.floor(self.sheet1.cell_value(5, 4)))   # 游客id
        appversion = self.dict["version"]  # 版本号
        devcode = self.dict["devcode"]     # 设备号
        os = self.dict["os"]      # 操作系统
        type = "2"       # 类型
        params = {
            "appversion":appversion,
            "devcode":devcode,
            "phone":phone,
            "password":password,
            "os":os,
            "type":type,
            "uid":userId
        }
        response = requests.get(base_url, params=params)
        return  response

    def login_wx(self):
        pass

    def test_login_01(self):
        u"测试手机号码登录，正确的手机号、密码"
        response = self.phone_login()
        result = json.loads(response.content)
        print(response.url)
        data = result["data"]
        status = result["status"]
        response_mobile = data["user"]["mobile"]
        self.assertEqual(status, 10001)
        print(result)

    def test_login_02(self):
        u"测试手机号码登录，错误密码登录"
        base_url = self.sheet1.cell_value(6, 2)  # 接口地址
        phone = str(math.floor(self.sheet1.cell_value(6, 5)))  # 手机号码
        password = self.sheet1.cell_value(6, 6)  # 密码
        userId = str(math.floor(self.sheet1.cell_value(6, 4)))  # 游客id
        appversion = self.dict["version"]  # 版本号
        devcode = self.dict["devcode"]  # 设备号
        os = self.dict["os"]  # 操作系统
        type = "2"  # 类型
        params = {
            "appversion": appversion,
            "devcode": devcode,
            "phone": phone,
            "password": password,
            "os": os,
            "type": type,
            "uid": userId
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(response.url)
        msg = result["msg"]
        self.assertEqual(msg,"用户名或密码错误")
        print (result)

    def test_wxlogin_01(self):
        u"微信登录，需要绑定手机号码"
        base_url = self.sheet1.cell_value(7,2)
        thirdid = self.sheet1.cell_value(7,5)
        uid = str(math.floor(self.sheet1.cell_value(7,4)))  #游客id
        appversion = Common_method.__dict__["version"]  # 版本号
        devcode = Common_method.__dict__["devcode"]  # 设备号
        os = Common_method.__dict__["os"]  # 操作系统
        timestamp = Common_method.__dict__["timestamp"]  # 时间戳
        list_key = [thirdid, devcode, timestamp]         # 字符串加密
        key = self.common_method.get_key(list_key)
        params ={
            "thirdid":thirdid,
            "uid":uid,
            "appversion":appversion,
            "devcode":devcode,
            "os":os,
            "timestamp":timestamp,
            "key":key
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(response.url)
        data = result["data"]
        #是否需要绑定的判断条件，为0，不需要绑定
        is_bind = data["requirebindmobile"]
        autherkey = data["authkey"]
        self.assertEqual(is_bind,1)
        self.assertIs(autherkey,"")

    def test_wxlogin_02(self):
        u"微信登录，不需要绑定手机号码"
        base_url = self.sheet1.cell_value(8, 2)
        thirdid = self.sheet1.cell_value(8, 5)
        uid = str(math.floor(self.sheet1.cell_value(8, 4)))  # 游客id
        appversion = Common_method.__dict__["version"]  # 版本号
        devcode = Common_method.__dict__["devcode"]  # 设备号
        os = Common_method.__dict__["os"]  # 操作系统
        timestamp = Common_method.__dict__["timestamp"]  # 时间戳
        list_key = [thirdid, devcode, timestamp]  # 字符串加密
        key = self.common_method.get_key(list_key)
        params = {
            "thirdid": thirdid,
            "uid": uid,
            "appversion": appversion,
            "devcode": devcode,
            "os": os,
            "timestamp": timestamp,
            "key": key
        }
        response = requests.get(base_url,params=params)
        result = json.loads (response.content)
        autherkey = result["data"]["authkey"]
        is_bind = result["data"]["requirebindmobile"]     # 是否需要绑定的判断条件，为0，不需要绑定
        self.assertEqual (is_bind, 0)
        self.assertIsNot(autherkey,"")

    def test_getUserinfo(self):
        u"登录后获取用户信息userinfo"
        base_url = self.sheet1.cell_value(10,2)
        appversion = Common_method.__dict__["version"]
        devcode = Common_method.__dict__["devcode"]
        os = Common_method.__dict__["os"]
        login_response = self.phone_login()
        login_result = json.loads(login_response.content)
        uid = login_result["data"]["user"]["id"]
        params =  {
            "appversion":appversion,
            "devcode":devcode,
            "os":os,
            "uid":uid}
        response = requests.get(base_url,params=params)
        print(response.url)
        result = json.loads(response.content)
        user_id  = result["data"]["user"]["id"]
        self.assertEqual(user_id,int(uid))

    def test_getUserstatus(self):
        u"登录后获取用户状态userstatus"
        base_url = self.sheet1.cell_value(11,2)
        login_response = self.phone_login()
        login_result = json.loads(login_response.content)
        uid = login_result["data"]["user"]["id"]
        usertype = login_result["data"]["user"]["type"]    #用户类型（1为手机账号、4为微信账号）
        appversion = self.dict["version"]
        devcode = self.dict["devcode"]
        os = self.dict["os"]
        timestamp = self.dict["timestamp"]
        key_list = []




