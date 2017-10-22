import unittest
import requests
import json
import xlrd
import hashlib
import math

from InterfaceTesting.run_all_cases import Common_method


#手机号登录、微信登录测试
class LoginTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    #手机号登录接口地址
    def get_url(self,base_url,phone,password,uid):
        #版本号
        appversion = Common_method.__dict__["version"]
        #设备号
        devcode = Common_method.__dict__["devcode"]
        #操作系统
        os = Common_method.__dict__["os"]
        #类型
        type = "2"
        # list拼接接口地址
        list_url1 = ["appversion", "devcode", "phone", "password", "os", "os", "type","uid"]
        list_url2 = [appversion, devcode, phone, password, os, type, uid]
        list_url3 = Common_method.get_url (self,list_url1, list_url2)  #生成例如：appversion=401000&devcode=aa783ojkljf&phone=13450244170格式
        url = base_url + list_url3                                #加上接口地址前缀
        print(url)
        return url

    #微信登录接口地址
    def get_url_wx(self,base_url,thirdid,uid):
        # 版本号
        appversion = Common_method.__dict__["version"]
        # 设备号
        devcode = Common_method.__dict__["devcode"]
        # 操作系统
        os = Common_method.__dict__["os"]
        timestamp = Common_method.__dict__["timestamp"]
        #字符串加密
        list_key = [thirdid,devcode,timestamp]
        key = Common_method.get_key(self,list_key)
        #list拼接地址
        list_url1 = ["thirdid","key","uid","appversion","devcode","os","timestamp"]
        list_url2 = [thirdid,key,uid,appversion,devcode,os,timestamp]
        list_url3 = Common_method.get_url(self,list_url1,list_url2)  #生成例如：thirdid=aaa&key=joekehfkrjfkdl&appversion=401000格式
        url= base_url+list_url3
        print(url)
        return url

    def test_login_01(self):
        u"测试手机号码登录，正确的手机号、密码"
        sheet1 = Common_method().get_excle_sheet1()
        base_url = sheet1.cell_value(5,2)
        # 手机号码
        phone = str (math.floor (sheet1.cell_value (5, 7)))
        # 密码
        password = sheet1.cell_value (5, 8)
        # 游客id
        userId = str (math.floor (sheet1.cell_value (5, 6)))
        #获取接口地址
        self.url = self.get_url(base_url,phone,password,userId)
        response = requests.get(self.url)
        result = json.loads (response.content)
        data = result["data"]
        status = result["status"]
        response_mobile = data["user"]["mobile"]
        self.assertEqual(status,10001)
        self.assertEqual(response_mobile,phone)
        print (result)

    def test_login_02(self):
        u"测试手机号码登录，错误密码登录"
        sheet1 = Common_method().get_excle_sheet1()
        base_url = sheet1.cell_value(6,2)
        # 手机号码
        phone = str (math.floor (sheet1.cell_value (6, 7)))
        # 密码
        password = sheet1.cell_value (6, 8)
        # 游客id
        userId = str (math.floor (sheet1.cell_value (6, 6)))
        #获取接口地址
        self.url = self.get_url(base_url,phone,password,userId)
        response = requests.get(self.url)
        result = json.loads (response.content)
        msg = result["msg"]
        self.assertEqual(msg,"用户名或密码错误")
        print (result)

    def test_wxlogin_01(self):
        u"微信登录，需要绑定手机号码"
        sheet1 = Common_method.get_excle_sheet1(self)
        base_url = sheet1.cell_value(7,2)
        third_id = sheet1.cell_value(7,9)
        uid = str(math.floor(sheet1.cell_value(7,6)))
        #获取接口地址
        self.url = self.get_url_wx(base_url,third_id,uid)
        response = requests.get(self.url)
        result = json.loads(response.content)
        data = result["data"]
        #是否需要绑定的判断条件，为0，不需要绑定
        is_bind = data["requirebindmobile"]
        autherkey = data["authkey"]
        self.assertEqual(is_bind,1)
        self.assertIs(autherkey,"")


    def test_wxlogin_02(self):
        u"微信登录，不需要绑定手机号码"
        sheet1 = Common_method.get_excle_sheet1 (self)
        base_url = sheet1.cell_value (8, 2)
        third_id = sheet1.cell_value (8, 9)
        uid = str (math.floor (sheet1.cell_value (8, 6)))
        # 获取接口地址
        self.url = self.get_url_wx (base_url, third_id, uid)
        response = requests.get (self.url)
        result = json.loads (response.content)
        data = result["data"]
        autherkey = data["authkey"]
        # 是否需要绑定的判断条件，为0，不需要绑定
        is_bind = data["requirebindmobile"]
        self.assertEqual (is_bind, 0)
        self.assertIsNot(autherkey,"")

    def test_wxlogin_03_getUserinfo(self):
        u"登录后获取用户信息userinfo"
        appversion = Common_method.__dict__["version"]
        devcode = Common_method.__dict__["devcode"]
        os = Common_method.__dict__["os"]
        sheet1 = Common_method.get_excle_sheet1(self)
        uid = str(math.floor(sheet1.cell_value(10,6)))
        base_url = sheet1.cell_value(10,2)
        # list拼接地址
        list_url1 = ["appversion", "devcode", "os", "uid"]
        list_url2 = [appversion, devcode, os, uid]
        list_url3 = Common_method.get_url (self,list_url1,list_url2)  # 生成例如：thirdid=aaa&key=joekehfkrjfkdl&appversion=401000格式
        self.url = base_url + list_url3
        response = requests.get(self.url)
        result = json.loads(response.content)
        user_id  = result["data"]["user"]["id"]
        self.assertEqual(user_id,int(uid))
        print(self.url)

    def test_wxlogin_04_getUserstatus(self):
        u"登录后获取用户状态userstatus"
        #获取接口地址前缀
        sheet1 = Common_method.get_excle_sheet1(self)
        base_url = sheet1.cell_value(11,2)
        #用户id
        uid = sheet1.cell_value(11,6)
        #用户类型（1为手机账号、4为微信账号）
        usertype = sheet1.cell_value(11,7)
        #获取appversion,os等
        dict = Common_method.get_common_params(self)
        appversion = dict["version"]
        devcode = dict["devcode"]
        os = dict["os"]
        timestamp = dict["timestamp"]
        print(timestamp)
        #获取key
       # key_list =
        #key = Common_method.get_key()





