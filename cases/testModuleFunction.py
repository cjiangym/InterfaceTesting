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
from common.getKey import Key


#---------------------首页功能按钮，功能模块，精明豆页功能模块，我的页面功能按钮--------------------#

class HomebuttonListTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_homepageButtonList(self):
        u"测试获取首页功能按钮"
        base_url =self.sheet1.cell_value(46,2)
        timestamp = Common_method.timestamp
        type = "1"
        list_key = [type,timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "appversion" :Common_method.version,
            "devcode" :Common_method.devcode,
            "os" :Common_method.os,
            "timestamp" :timestamp,
            "key":key,
            "uid":self.sheet1.cell_value(46,4),
            "type":type
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["items"][0]["title"],"到店签到")

    def test_mypageButtonList(self):
        u"测试获取我的页面功能按钮"
        base_url =self.sheet1.cell_value(46,2)
        timestamp = Common_method.timestamp
        type = "4"
        list_key = [type,timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "appversion" :Common_method.version,
            "devcode" :Common_method.devcode,
            "os" :Common_method.os,
            "timestamp" :timestamp,
            "key":key,
            "uid":self.sheet1.cell_value(46,4),
            "type":type
        }
        response = requests.get(base_url,params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertEqual (result["data"]["items"][0]["title"], "我的兑换")

    def test_recommenModule(self):
        u"测试首页推荐模块功能"
        base_url = self.sheet1.cell_value(45,2)
        uid = self.sheet1.cell_value(45,4)
        cityid = self.sheet1.cell_value(45,5)
        timestamp = self.common_method.timestamp
        list_key = [uid,cityid,timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "cityid":cityid,
            "key":key,
            "lon":self.sheet1.cell_value(45,6),
            "lat":self.sheet1.cell_value(45,7),
            "timestamp":timestamp,
            "uid":uid,
            "os":self.common_method.os,
            "devcode":self.common_method.devcode,
            "appversion":self.common_method.version
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["shop"]["title"],"附近推荐")

    def test_beanGmaeList(self):
        u"测试精明豆页面板块功能按钮"
        base_url = self.sheet1.cell_value(47,2)
        params = {
            "cityid": self.sheet1.cell_value(47,5),
            "lon": self.sheet1.cell_value (45, 6),
            "lat": self.sheet1.cell_value (45, 7),
            "timestamp": self.common_method.timestamp,
            "uid": self.sheet1.cell_value(47,4),
            "os": self.common_method.os,
            "devcode": self.common_method.devcode,
            "appversion": self.common_method.version
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["modules"][0]["module"],"线下赚豆")