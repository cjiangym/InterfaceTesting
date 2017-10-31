import unittest
import math
import _md5
import hashlib
import requests
from InterfaceTesting.run_all_cases import Common_method

class Login():
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()

    def phone_login(self):
        base_url = self.sheet1.cell_value (5, 2)  # 接口地址
        phone = self.sheet1.cell_value (5, 5)  # 手机号码
        if isinstance (phone, float):  # 判断单元格值的类型
            phone = str (math.floor (phone))  # 转换成str类型
        password = self.sheet1.cell_value (5, 6)  # 密码
        password_md5 = hashlib.md5 (password.encode ("utf-8")).hexdigest ()  # 密码通过md5加密
        userId = str (math.floor (self.sheet1.cell_value (5, 4)))  # 游客id
        appversion = self.common_method.version  # 版本号
        devcode = self.common_method.devcode  # 设备号
        os = self.common_method.os  # 操作系统
        type = "2"  # 类型
        params = {
            "appversion": appversion,
            "devcode": devcode,
            "phone": phone,
            "password": password_md5,
            "os": os,
            "type": type,
            "uid": userId
        }
        response = requests.get(base_url, params=params)
        return response