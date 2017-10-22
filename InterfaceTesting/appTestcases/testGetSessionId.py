#!E:/python
import unittest
import requests
import json
import xlrd
import math
from InterfaceTesting.run_all_cases import Common_method

#sessionId
class SessionIdTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def get_url(self,base_url,lon,lat,uid):
        app_version = Common_method.__dict__["version"]
        client = "ios"
        devcode = Common_method.__dict__["devcode"]
        os = Common_method.__dict__["os"]
        reqtime = "2017-10-17 16:11:20"
        userkey = "123"
        list_url1 = ["appversion", "devcode", "client", "lon", "lat", "uid", "os", "reqtime","uid","userkey"]
        list_url2 = [app_version, devcode, client, lon, lat, uid, os, reqtime,uid,userkey]
        list_url3 = Common_method.get_url (self,list_url1,list_url2)  # 生成例如：thirdid=aaa&key=joekehfkrjfkdl&appversion=401000格式
        url = base_url + list_url3
        return url

    def testGetSessionId(self):
        u"获取sessionId"
        sheet1 = Common_method.get_excle_sheet1 (self)
        base_url = sheet1.cell_value(2,2)
        lon = str(sheet1.cell_value(2,4))
        lat = str(sheet1.cell_value(2,5))
        uid = str(math.floor(sheet1.cell_value(2,6)))
        self.url = self.get_url(base_url,lon,lat,uid)
        print(self.url)
        response = requests.get(self.url)
        result = json.loads(response.content)
        print(result)
        data = result["data"]
        print(data)
        status = result["status"]
        self.assertIn("expire",data)
        self.assertEqual(status,10001)
