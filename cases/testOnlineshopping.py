import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method

class OnlineshoppingTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_homepageRecommend(self):
        u"测试获取首页网购推荐列表"
        base_url ="http://wx2.ismartgo.com/mksv/goods/getbysubject"
        params = {
            "lon" : "116.512392" ,
            "appversion" : "401000",
            "cityid" : 52,
            "timestamp" : "20171113182937",
            "uid" : 832776,
            "page" : 1,
            "lat" : "39.933653",
            "os" : "Android",
            "devcode" : "6455aa44 - aa6d - 31ba - 9298 - b2102030d93d"
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"]["items"],[])