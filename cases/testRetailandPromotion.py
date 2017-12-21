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
from config import serverAddressConfig

class PromotionTest(unittest.TestCase):
    common_method = Common_method()
    sheet2 = common_method.get_excle_sheet(1)
    svrAddr = serverAddressConfig.svr2_29094

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_homepagePromotion(self):
        u"测试首页促销信息"
        base_url = self.sheet2.cell_value(7,2)
        url = self.svrAddr + base_url
        uid = self.sheet2.cell_value(7,4)
        timestamp = serverAddressConfig.timestamp
        list_key = [uid,timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "userid" : uid,
            "cityid" :self.sheet2.cell_value(7,5),
            "lon" :self.sheet2.cell_value(7,6),
            "lat":self.sheet2.cell_value(7,7),
            "key" :key,
            "nextpage":"",
            "timestamp" :timestamp,
            "subscribe" :"0",
            "appversion" : serverAddressConfig.version,
            "devcode" :serverAddressConfig.devcode,
            "os":serverAddressConfig.os
        }
        response = requests.get(url,params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"]["retails"],[])

    def test_mySubscribed(self):
        u"测试首页我关注的零售商"
        base_url = self.sheet2.cell_value (8, 2)
        url = self.svrAddr + base_url
        uid = self.sheet2.cell_value (8, 4)
        cityid = self.sheet2.cell_value (8, 5)
        timestamp = serverAddressConfig.timestamp
        list_key = [uid,cityid, timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "uid": uid,
            "cityid": cityid,
            "lon": self.sheet2.cell_value (8, 6),
            "lat": self.sheet2.cell_value (8, 7),
            "key": key,
            "nextpage": "",
            "timestamp": timestamp,
            "subscribe": "0"
        }
        response = requests.get (url, params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual (result["data"], None)
        self.assertNotEqual (result["data"],{})


    def test_retailList(self):
        u"测试所有可关注/已关注零售商列表"
        base_url =  self.sheet2.cell_value (6, 2)  # 搜索促销商店
        url = self.svrAddr + base_url
        params_search = {
            "districtid": "-2",  # 默认值
            "shoptypeid": "-1",  # 默认值
            "townid": "-2",  # 默认值
            "distance": "",
            "cityid": self.sheet2.cell_value(6, 5),
            "lon": self.sheet2.cell_value(6, 7),
            "lat": self.sheet2.cell_value(6, 8),
            "nextpage": "",
            "keyword": self.sheet2.cell_value (6, 6),
            "userid": self.sheet2.cell_value (6, 4)
        }
        response = requests.get(url, params=params_search)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual (result["data"], None)
        return result

    def test_mySubscribeList(self):
        u"测试已关注零售商列表"
        base_url = self.sheet2.cell_value(12,2)
        url = self.svrAddr + base_url
        params = {
            "userid": self.sheet2.cell_value(12,4),
            "page": 1,
            "cityid": self.sheet2.cell_value(12,5),
            "lon":self.sheet2.cell_value(12,6),
            "lat": self.sheet2.cell_value(12,7),
            "appversion":serverAddressConfig.version
        }
        response = requests.get (url, params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        return result

    def test_subscribe(self):
        u"测试关注零售商"
        try:
            self.retail_result = self.test_retailList()
        except:
            self.assertTrue(None,"获取零售商列表失败")
        base_url = self.sheet2.cell_value(9,2)
        url = self.svrAddr + base_url
        uid =  self.sheet2.cell_value (9, 4)
        retailid = ""
        for retails in self.retail_result["data"]["retails"]:
            if retails["subscribe"] ==2 :                #为1是已关注，为2是未关注
                retailid = retails["retailId"]
                break
        params = {
            "userid" :uid,
            "retailid" : retailid,
            "type" :1,                                  #1是关注，2是取消关注
            "appversion" :serverAddressConfig.version,
            "os" :serverAddressConfig.os,
            "timestamp" :serverAddressConfig.timestamp,
            "devcode" :serverAddressConfig.devcode
        }
        response = requests.get(url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"], None)
        #检查我的关注列表是否有该零售商
        canMatch = False
        try:
            self.result_subscribe = self.test_mySubscribeList()
        except:
            self.assertTrue(None,"获取已关注的零售商列表失败")
        for subscribeList in self.result_subscribe["data"]["subscribeList"]:
            if subscribeList["retailId"] == retailid:
                canMatch = True
                break
        self.assertTrue(canMatch,"关注失败")

    def test_cancleSubscribe(self):
        u"测试取消零售商"
        uid = self.sheet2.cell_value (10, 4)
        try:
            self.result_subscribe = self.test_mySubscribeList()                 # 获取我的已关注列表
        except:
            self.assertTrue(None,"查询我的已关注列表失败")
        base_url = self.sheet2.cell_value(10,2)
        url = self.svrAddr + base_url
        if self.result_subscribe["data"]["subscribeList"] !=[]:
            retailid = self.result_subscribe["data"]["subscribeList"][0]["retailId"]
            params = {
                "userid" :uid,
                "retailid" : retailid,
                "type" :2,                                              #1是关注，2是取消关注
                "appversion" :serverAddressConfig.version,
                "os" :serverAddressConfig.os,
                "timestamp" :serverAddressConfig.timestamp,
                "devcode" :serverAddressConfig.devcode
            }
            response = requests.get(url,params=params)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertEqual (result["data"], None)
            #检查我的关注列表是否有该零售商
            canMatch = True
            try:
                result_subscribe = self.test_mySubscribeList()
            except:
                self.assertTrue(None,"查询我的已关注列表失败")
            for subscribeList in result_subscribe["data"]["subscribeList"]:
                if subscribeList["retailId"] == retailid:
                    canMatch = False
                    break
            self.assertTrue(canMatch,"取消关注失败")

    def test_retailPromotion(self):
        u"测试获取促销优惠列表"
        base_url = self.sheet2.cell_value(11,2)
        url = self.svrAddr + base_url
        userid = self.sheet2.cell_value(11,4)
        timestamp = serverAddressConfig.timestamp
        key_list = [userid,timestamp]
        key = Key.get_key(self,key_list)
        params = {
            "districtid":-2,
            "appversion": serverAddressConfig.version,
            "cityid": self.sheet2.cell_value (11, 5),
            "devcode": serverAddressConfig.devcode,
            "key": key,
            "lon": self.sheet2.cell_value (11, 6),
            "lat": self.sheet2.cell_value (11, 7),
            "nextpage": "",
            "os": serverAddressConfig.os,
            "timestamp": timestamp,
            "userid": userid,
            "retailid":-1,
            "townid":-2,
            "distance":"",
            "shoptypeid":-1
        }
        response = requests.get (url, params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual (result["data"], None)
        self.assertNotEqual (result["data"]["retails"],[])




