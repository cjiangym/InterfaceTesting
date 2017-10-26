import unittest
import requests
import json
import xlrd
import hashlib
import math
import time
from xlrd import xldate_as_tuple
from InterfaceTesting.run_all_cases import Common_method

class wxCreateTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass


    def get_validCode(self,mobile):
        base_url = "http://192.168.1.243:29090/appsv2/app/getValidCode.do"
        phone =mobile
        type = "1"        #注册时获取验证码，类型为1
        key_list = [phone]
        key = Common_method.get_key(self,key_list)
        params = {
            "phone":phone,
            "key":key,
            "type":type
        }
        response = requests.get(base_url,params)

    def test_wxCreate(self):
        u"可测试绑定已注册的手机号码，未注册的手机号码，thirdid动态生成"
        base_url = "http://120.76.209.16:29090/appsv2/app/wxCreateUser.do?"
        lon ="113.368757"
        lat = "23.152705"
        cityname = "广州"
        timestamp = time.strftime("%Y%m%d%H%M%S",time.localtime())
        nickname =timestamp+"测试账号"
        cityid ="76"
        mobile = "16111111120"
        validcode = "4427"    #手动从数据库查验证码
        self.get_validCode(mobile)
        newpwd = "e10adc3949ba59abbe56e057f20f883e"           #md5加密后的验证码
        thirdid ="oNh_lshvS3y5NBHzEnXjI4R0XUHc"+timestamp
        logopath = "http://wx.qlogo.cn/mmhead/sTJptKvBQLJHNtRK8EzCyDB2VTv8wbLxtK08dsF6YWk113ZzMZK3ug/0"
        os = "Android"
        appversion ="402000"
        devcode = "d3c73bed-09f8-3bb2-b411-772d6f8e867f"
        key_list = [thirdid,devcode,timestamp]
        common_method = Common_method ()
        key = common_method.get_key(key_list)
        params ={
            "lon":lon,
            "lat":lat,
            "cityname":cityname,
            "cityid":cityid,
            "nickname":nickname,
            "mobile":mobile,
            "validcode":validcode,
            "newpwd":newpwd,
            "thirdid":thirdid,
            "logopath":logopath,
            "timestamp":timestamp,
            "os":os,
            "appversion":appversion,
            "devcode":devcode,
            "key":key,
            "uid":"10784976"          #游客id,跟devcode必须对应
        }
        response = requests.get("http://192.168.1.243:29090/appsv2/app/wxCreateUser.do",params=params)



