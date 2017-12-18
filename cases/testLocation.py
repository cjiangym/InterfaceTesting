import unittest
import requests
import json
import xlrd
import hashlib
import math
from common.common_method import Common_method
from common.getKey import Key
from config import serverAddressConfig


class CityLocationTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    svrAddr = serverAddressConfig.sv_29090

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testGetpositonCity_01(self):
        u"获取当前定位城市"
        base_url = self.sheet1.cell_value (3, 2)
        appversion = serverAddressConfig.version
        devcode = serverAddressConfig.devcode
        timestamp = serverAddressConfig.timestamp
        locationName = self.sheet1.cell_value (3, 5)
        lon = self.sheet1.cell_value (3, 6)
        lat = self.sheet1.cell_value (3, 7)
        uid = self.sheet1.cell_value (3, 4)
        list_key = [uid, locationName, timestamp]       #加密key
        key = Key.get_key(self,list_key)
        params_name = ["appversion","devode","locationName","lon","lat","uid","timestamp","key"]
        params_value = [appversion,devcode,locationName,lon,lat,uid,timestamp,key]
        response = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        assertResult = self.sheet1.cell_value(3,8)
        self.assertEqual(result["status"],10001)
        self.assertIn(result["data"]["name"],assertResult)

    def test_getAllcity(self):
        u"测试获取所有城市"
        base_url = self.sheet1.cell_value(4,2)
        uid = self.sheet1.cell_value(4,4)
        appversion = serverAddressConfig.version
        devcode = serverAddressConfig.devcode
        os = serverAddressConfig.os
        timestamp = serverAddressConfig.timestamp
        list_key = [timestamp]
        key = Key.get_key(self,list_key)
        params_name = ["appversion","devcode","os","timestamp","uid","key"]
        params_value = [appversion,devcode,os,timestamp,uid,key]
        try:
            self.response = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
            self.assertEqual(self.response.status_code,200)
        except:
            self.assertTrue(None,"兑换失败")
        result = json.loads(self.response.content)
        city_0 = result["data"]["citys"][0]
        city_0_address = city_0["address"]
        self.assertEqual(result["status"],10001)

    def test_getAreaData(self):
        u"测试获取区域数据areaData"
        base_url = self.sheet1.cell_value(13,2)
        url = self.svrAddr + base_url
        uid = self.sheet1.cell_value(13,6)
        if isinstance(uid,float):
            uid = math.floor(uid)
        params = {
            "appversion":serverAddressConfig.version,
            "devocde":serverAddressConfig.devcode,
            "os":serverAddressConfig.os,
            "cityName":self.sheet1.cell_value(13,5),
            "uid":uid
        }
        response = requests.get(url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual (result["data"],"null")
        self.assertEqual(result["data"]["districts"][0]["districtId"],-2)
        self.assertEqual(result["data"]["districts"][0]["districtName"],"附近")
        self.assertEqual(result["data"]["districts"][0]["towns"][0]["townName"],"附近（智能范围）")
        self.assertEqual(result["data"]["districts"][1]["districtId"], -1)
        self.assertEqual(result["data"]["districts"][1]["districtName"], "全部商区")
        self.assertEqual(result["data"]["districts"][1]["towns"][0]["townName"], "全部")






'''
if __name__ == 'location':
    print("location")
    suites = unittest.TestSuite()
    suites.addTest(getlocation("testGetSessonId"))
    suites.addTest(getlocation("testGetpositonCity"))
    runner = unittest.TextTestRunner()
    runner.run(suites)
'''

