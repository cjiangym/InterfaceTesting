#将游客账号的精明豆同步到登录账号（一台设备仅能同步一次）

import unittest
import requests
import  json
import math
from InterfaceTesting.run_all_cases import Common_method

class SynchroBeanTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testSynchroBean(self):
        #获取测试用例excle
        sheet1 = Common_method.get_excle_sheet1(self)
        base_url = sheet1.cell_value(12,2)
        uid = str(math.floor(sheet1.cell_value(12,6)))
        #一台设备仅能同步一次，所以需对设备编号测试
        devcode = sheet1.cell_value(12,7)
        imei = devcode    #前期的设备编号字段标识
        dict = Common_method.get_common_params(self)
        appversion = dict["version"]
        os = dict["os"]
        #拼接接口地址
        list1 = ["appversion","devcode","imei","os","uid"]
        list2 = [appversion,devcode,imei,os,uid]
        list3 = Common_method.get_url(list1,list2)
        self.url = base_url+list3
        print(self.url)
        #执行接口
        response = requests.get(self.url)
        #判断结果
        result = json.loads(response.content)

