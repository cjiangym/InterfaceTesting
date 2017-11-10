import unittest
import math
import _md5
import hashlib
import requests
import json
from common.common_method import Common_method


class Login():

    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()

   #手机号码登录
    def phone_login(self,phone,psw):
        base_url = self.sheet1.cell_value (5, 2)  # 接口地址
        self.phone = phone                        # 手机号码
        if isinstance (self.phone, float):  # 判断单元格值的类型
            self.phone = str(math.floor(self.phone))  # 转换成str类型
        self.psw = psw                       # 密码
        password_md5 = hashlib.md5 (self.psw.encode ("utf-8")).hexdigest ()       # 密码通过md5加密
        userId = str (math.floor (self.sheet1.cell_value (5, 4)))  # 游客id
        appversion = self.common_method.version  # 版本号
        devcode = self.common_method.devcode  # 设备号
        os = self.common_method.os  # 操作系统
        type = "2"  # 类型
        params = {
            "appversion": appversion,
            "devcode": devcode,
            "phone": self.phone,
            "password": password_md5,
            "os": os,
            "type": type,
            "uid": userId
        }
        response = requests.get(base_url, params=params)
        result = json.loads(response.content)
        response_dict ={
            "data" :result["data"],
            "msg" :result["msg"],
            "status" :result["status"]
        }
        return response_dict

    #微信登录
    def wx_login(self,thirdId):
        base_url = self.sheet1.cell_value (7, 2)
        self.thirdid = thirdId
        uid = str(math.floor (self.sheet1.cell_value (7, 4)))  # 游客id
        appversion = self.common_method.version  # 版本号
        devcode =self.common_method.devcode # 设备号
        os = self.common_method.os     # 操作系统
        timestamp = self.common_method.timestamp  # 时间戳
        list_key = [self.thirdid, devcode, timestamp]  # 字符串加密
        key = self.common_method.get_key (list_key)
        params = {
            "thirdid": self.thirdid,
            "uid": uid,
            "appversion": appversion,
            "devcode": devcode,
            "os": os,
            "timestamp": timestamp,
            "key": key
        }
        response_wxlogin = requests.get (base_url, params=params)
        result_wxlogin = json.loads(response_wxlogin.content)
        response_dict = {
            "data": result_wxlogin["data"],
            "msg": result_wxlogin["msg"],
            "status": result_wxlogin["status"]
        }
        return  response_dict


