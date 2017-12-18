import unittest
import math
import _md5
import hashlib
import requests
import json
from common.common_method import Common_method
from common.getKey import Key
from config import serverAddressConfig


class Login():
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    svrAddr = serverAddressConfig.sv_29090

   #手机号码登录
    def phone_login(self,phone,psw):
        base_url = self.sheet1.cell_value(5, 2)   # 接口地址
        password_md5 = hashlib.md5(psw.encode ("utf-8")).hexdigest()       # 密码通过md5加密
        userId = self.sheet1.cell_value (5, 4)                              # 游客id
        version = serverAddressConfig.version  # 版本号
        devcode = serverAddressConfig.devcode  # 设备号
        os = serverAddressConfig.os  # 操作系统
        type = "2"  # 类型
        params_name =["appversion","devcode","phone","password","os","type","uid"]
        params_value = [version,devcode,phone,password_md5,os,type,userId]
        response = self.common_method.get_response(self.svrAddr,base_url, params_name,params_value)
        result = json.loads(response.content)
        return result

    #微信登录
    def wx_login(self,thirdId):
        base_url = self.sheet1.cell_value (7, 2)
        uid = str(math.floor (self.sheet1.cell_value (7, 4)))  # 游客id
        version = serverAddressConfig.version  # 版本号
        devcode =serverAddressConfig.devcode # 设备号
        os = serverAddressConfig.os     # 操作系统
        timestamp = serverAddressConfig.timestamp  # 时间戳
        list_key = [thirdId, devcode, timestamp]  # 字符串加密
        key = Key.get_key(self,list_key)
        params_name = ["thirdid", "uid", "appversion", "devcode", "os", "timestamp", "key"]
        params_value = [thirdId, uid, version, devcode, os, timestamp, key]
        response_wxlogin = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
        result_wxlogin = json.loads(response_wxlogin.content)
        return  result_wxlogin


