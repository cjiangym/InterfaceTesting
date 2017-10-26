import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from InterfaceTesting.run_all_cases import Common_method


class DailySignTest(unittest.TestCase):

    common_method = Common_method ()
    sheet1 = common_method.get_excle_sheet1 ()
    sheet2 = common_method.get_excle_sheet2()
    dict = common_method.get_common_params()

    def setUp(self):
        pass
    def setUp(self):
        pass

    def test_dailySign(self):
        u"测试每日签到"
        base_url = self.sheet1.cell_value(14,2)
        uid = str(math.floor(self.sheet1.cell_value(14,4)))
        appversion = self.dict["version"]
        params ={
            "uid":uid,
            "appversion":appversion
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        status = result["status"]
        signinfo = result["data"]["signInfo"]
        self.assertEqual(status,10001)
        self.assertNotEqual(len(signinfo),0)

    def test_shopSign(self):
        u"测试到店签到"
        base_url = self.sheet1.cell_value(15,2)
        beacon = "0"    #签到beacon，没有则为0
        lon = str(math.floor(self.sheet1.cell_value(15,4)))
        lat = str(math.floor(self.sheet1.cell_value(15,5)))
        uid = str(math.floor(self.sheet1.cell_value(15,6)))
        shopId = str(math.floor(self.sheet1.cell_value(15,7)))
        cityId = str(math.floor(self.sheet1.cell_value(15,8)))
        os = self.dict["os"]
        devcode = self.dict["version"]
        timestamp = self.dict["timestamp"]
        appversion = self.dict["version"]
        authkey = self.sheet1.cell_value(15,9)
        key_list = [uid,shopId,beacon,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        params = {
            "beacon":beacon,
            "lon":lon,
            "lat":lat,
            "uid":uid,
            "shopId":shopId,
            "cityId":cityId,
            "os":os,
            "devcode":devcode,
            "timestamp":timestamp,
            "appversion":appversion,
            "key":key
        }
        response = requests.get(base_url,params=params)



