import unittest
import requests
import json
import xlrd
import hashlib
import math
from InterfaceTesting.run_all_cases import Common_method

#定位相关case
class CityLocationTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    #获取接口地址
    def get_url(self,base_url,locationName,lon,lat,uid):
        #版本号
        appversion = Common_method.__dict__["version"]
        #设备号
        devcode = Common_method.__dict__["devcode"]
        #时间戳
        timestamp = Common_method.__dict__["timestamp"]
        #加密字符串
        list_key = [uid,locationName,timestamp]
        key = Common_method.get_key(self,list_key)
        #list拼接口地址url
        list_url1 = ["appversion", "devcode", "locationName", "lon", "lat", "uid", "timestamp","key"]
        list_url2 = [appversion, devcode, locationName, lon, lat, uid, timestamp,key]
        list_url3 = Common_method.get_url (self,list_url1,list_url2)  # 生成例如：thirdid=aaa&key=joekehfkrjfkdl&appversion=401000格式
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

    '''
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
    def test_get_allcity(self):
        u"测试获取所有城市"
        common_method = Common_method()
        sheet1 = common_method.get_excle_sheet1()
        base_url = sheet1.cell_value(4,2)
        uid = str(math.floor(sheet1.cell_value(4,6)))
        dict = common_method.get_common_params()
        appversion = dict["version"]
        devcode = dict["devcode"]
        os = dict["os"]
        timestamp = dict["timestamp"]
        #获得加密key
        key_list = [timestamp]
        key = common_method.get_key(key_list)
        #接口地址
        list1= ["appversion","devcode","os","timestamp","uid","key"]
        list2 =[appversion,devcode,os,timestamp,uid,key]
        list3 = common_method.get_url(list1,list2)
        self.url = base_url+list3
        print(self.url)
        #执行
        response = requests.get(self.url)
        result = json.loads(response.content)
        print(result)
        status = result["status"]
        city_0 = result["data"]["citys"][0]
        city_0_address = city_0["address"]
        self.assertEqual(status,10001)
        self.assertIsNot(city_0_address,"")

    def test_getAreaData(self):
        u"测试获取区域数据areaData"
        common_method = Common_method()
        sheet1 = common_method.get_excle_sheet1()
        base_url = sheet1.cell_value(13,2)
        cityName = sheet1.cell_value(13,5)
        uid = str(math.floor(sheet1.cell_value(13,6)))
        dict = common_method.get_common_params()
        appversion = dict["version"]
        devcode = dict["devcode"]
        os = dict["os"]
        list1 = ["appversion","devocde","os","cityName","uid"]
        list2 = [appversion,devcode,os,cityName,uid]
        list3 = common_method.get_url(list1,list2)
        self.url = base_url +list3
        print(self.url)
        response = requests.get(self.url)
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

