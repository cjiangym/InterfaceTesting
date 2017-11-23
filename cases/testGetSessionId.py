import unittest
import requests
import json
import xlrd
import math
from common.common_method import Common_method


#sessionId
class SessionIdTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_getSessionId(self):
        u"测试获取sessionId"
        base_url = self.sheet1.cell_value(2,2)
        lon = str(self.sheet1.cell_value(2,4))
        lat = str(self.sheet1.cell_value(2,5))
        uid = str(math.floor(self.sheet1.cell_value(2,6)))
        appversion = Common_method.__dict__["version"]
        client = Common_method.__dict__["os"]
        devcode = Common_method.__dict__["devcode"]
        os = Common_method.__dict__["os"]
        reqtime = "2017-10-17 16:11:20"
        userkey = "123"               #没有时默认为123
        params = {
         "appversion":appversion,
         "devcode":devcode,
         "client":client,
         "lon":lon,
         "lat":lat,
         "uid":uid,
         "os":os,
         "reqtime":reqtime,
         "userkey":userkey
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        print(response.url)
        print(result)
        self.assertIn("expire",result["data"])
        self.assertEqual(result["status"],10001)
