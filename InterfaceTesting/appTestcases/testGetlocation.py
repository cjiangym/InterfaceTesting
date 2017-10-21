import unittest
import requests
import json
import xlrd
import hashlib
import math
from InterfaceTesting.run_all_cases import Common_method

#定位相关case
class TestCityLocation(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    #基础参数
    def get_url(self,base_url,locationName,lon,lat,uid):
        #版本号
        appversion = Common_method.__dict__["version"]
        #设备号
        devcode = Common_method.__dict__["devcode"]
        #时间戳
        timestamp = Common_method.__dict__["timestamp"]
        #加密字符串
        list_key = [uid,locationName,timestamp]
        key = Common_method.get_key(list_key)
        #list拼接口地址url
        list_url1 = ["appversion", "devcode", "locationName", "lon", "lat", "uid", "timestamp","key"]
        list_url2 = [appversion, devcode, locationName, lon, lat, uid, timestamp,key]
        list_url3 = Common_method.get_url (list_url1,list_url2)  # 生成例如：thirdid=aaa&key=joekehfkrjfkdl&appversion=401000格式
        url = base_url + list_url3
        print(url)
        return url

    def testGetpositonCity_01(self):
        u"获取当前定位城市 - 广州"
        sheet1 = Common_method.get_excle_sheet1(self)
        #获取接口地址前缀
        base_url = sheet1.cell_value (3, 2)
        # 城市名称
        locationName = sheet1.cell_value (3, 3)
        # 经度
        lon = str(sheet1.cell_value (3, 4))
        # 纬度
        lat = str(sheet1.cell_value (3, 5))
        # 用户id
        uid = str (math.floor (sheet1.cell_value (3, 6)))
        self.url = self.get_url(base_url,locationName,lon,lat,uid)
        response = requests.get(self.url)
        result = json.loads(response.content)
        status = result["status"]
        data = result["data"]
        self.assertEqual(status,10001)
        self.assertIn("address",data)
        print(result)

    def testGetpositonCity_02(self):
        u"获取当前定位城市 - 北京"
        sheet1 = Common_method.get_excle_sheet1(self)
        # 获取接口地址前缀
        base_url = sheet1.cell_value (4, 2)
        # 城市名称
        locationName = sheet1.cell_value (4, 3)
        # 经度
        lon = str (sheet1.cell_value (4, 4))
        # 纬度
        lat = str (sheet1.cell_value (4, 5))
        # 用户id
        uid = str (math.floor (sheet1.cell_value (4, 6)))
        self.url = self.get_url(base_url, locationName, lon, lat, uid)
        response = requests.get(self.url)
        result = json.loads(response.content)
        status = result["status"]
        data = result["data"]
        self.assertEqual(status,10001)
        self.assertIn("address",data)
        print(result)



'''
if __name__ == 'location':
    print("location")
    suites = unittest.TestSuite()
    suites.addTest(getlocation("testGetSessonId"))
    suites.addTest(getlocation("testGetpositonCity"))
    runner = unittest.TextTestRunner()
    runner.run(suites)
'''

