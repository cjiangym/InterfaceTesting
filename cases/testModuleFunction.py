import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
import re
from xlrd import xldate_as_tuple
from common.common_method import Common_method


#---------------------首页功能按钮，功能模块，精明豆页功能模块，我的页面功能按钮--------------------#

class HomebuttonListTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_homepageButtonList(self):
        u"测试获取首页功能按钮"
        sheet1 = Common_method.get_excle_sheet1(self)
        base_url =sheet1.cell_value(46,2)
        timestamp = Common_method.timestamp
        type = "1"
        key_list = [type,timestamp]
        key = Common_method.get_key(self,key_list)
        params = {
            "appversion" :Common_method.version,
            "devcode" :Common_method.devcode,
            "os" :Common_method.os,
            "timestamp" :timestamp,
            "key":key,
            "uid":sheet1.cell_value(46,4),
            "type":type
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["items"][0]["title"],"到店签到")

    def test_mypageButtonList(self):
        u"测试获取我的页面功能按钮"
        sheet1 = Common_method.get_excle_sheet1(self)
        base_url =sheet1.cell_value(46,2)
        timestamp = Common_method.timestamp
        type = "4"
        key_list = [type,timestamp]
        key = Common_method.get_key(self,key_list)
        params = {
            "appversion" :Common_method.version,
            "devcode" :Common_method.devcode,
            "os" :Common_method.os,
            "timestamp" :timestamp,
            "key":key,
            "uid":sheet1.cell_value(46,4),
            "type":type
        }
        response = requests.get(base_url,params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertEqual (result["data"]["items"][0]["title"], "我的兑换")