import unittest
import requests
import json
import xlrd
import hashlib
import math
from common.common_method import Common_method
from common.getKey import Key

#定位相关case
class CityLocationTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    dict = common_method.get_common_params()
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testGetpositonCity_01(self):
        u"获取当前定位城市"
        base_url = self.sheet1.cell_value (3, 2)
        appversion = Common_method.__dict__["version"]
        devcode = Common_method.__dict__["devcode"]
        timestamp = Common_method.__dict__["timestamp"]
        locationName = self.sheet1.cell_value (3, 5)
        lon = str(self.sheet1.cell_value (3, 6))
        lat = str(self.sheet1.cell_value (3, 7))
        uid = str (math.floor (self.sheet1.cell_value (3, 4)))
        list_key = [uid, locationName, timestamp]       #加密key
        key = Key.get_key(self,list_key)
        params = {
            "appversion":appversion,
            "devcode":devcode,
            "locationName":locationName,
            "lon":lon,
            "lat":lat,
            "uid":uid,
            "timestamp":timestamp,
            "key":key}
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        status = result["status"]
        data = result["data"]
        self.assertEqual(status,10001)
        self.assertIn("address",data)
        print(result)

    def test_getAllcity(self):
        u"测试获取所有城市"
        common_method = Common_method()
        base_url = self.sheet1.cell_value(4,2)
        uid = self.sheet1.cell_value(4,4)
        appversion = self.dict["version"]
        devcode = self.dict["devcode"]
        os = self.dict["os"]
        timestamp = self.dict["timestamp"]
        list_key = [timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "appversion":appversion,
            "devcode":devcode,
            "os":os,
            "timestamp":timestamp,
            "uid":uid,
            "key":key
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(result)
        status = result["status"]
        city_0 = result["data"]["citys"][0]
        city_0_address = city_0["address"]
        self.assertEqual(status,10001)
        self.assertIsNot(city_0_address,"")

    def test_getAreaData(self):
        u"测试获取区域数据areaData"
        base_url = self.sheet1.cell_value(13,2)
        uid = self.sheet1.cell_value(13,6)
        if isinstance(uid,float):
            uid = math.floor(uid)
        params = {
            "appversion":self.common_method.version,
            "devocde":self.common_method.devcode,
            "os":self.common_method.os,
            "cityName":self.sheet1.cell_value(13,5),
            "uid":uid
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        print(result)
        status = result["status"]
        district_0 = result["data"]["districts"][0]
        district_1 = result["data"]["districts"][1]
        self.assertEqual(status,10001)
        self.assertEqual(district_0["districtId"],-2)
        self.assertEqual(district_0["districtName"],"附近")
        self.assertEqual(district_0["towns"][0]["townName"],"附近（智能范围）")
        self.assertEqual (district_1["districtId"], -1)
        self.assertEqual (district_1["districtName"], "全部商区")
        self.assertEqual (district_1["towns"][0]["townName"], "全部")






'''
if __name__ == 'location':
    print("location")
    suites = unittest.TestSuite()
    suites.addTest(getlocation("testGetSessonId"))
    suites.addTest(getlocation("testGetpositonCity"))
    runner = unittest.TextTestRunner()
    runner.run(suites)
'''

