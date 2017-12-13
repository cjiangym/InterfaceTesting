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
from common.getRetails import get_Retails

class PromotionTest(unittest.TestCase):
    common_method = Common_method()
    sheet2 = common_method.get_excle_sheet(1)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_homepagePromotion(self):
        u"测试首页促销信息"
        base_url = self.sheet2.cell_value(7,2)
        uid = self.sheet2.cell_value(7,4)
        timestamp = self.common_method.timestamp
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
            "subscribe" :"0"
        }
        response = requests.get(base_url,params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads(response.content)
        self.assertNotEqual(result["data"]["retails"],[])

    def test_mySubscribed(self):
        u"测试首页我关注的零售商"
        base_url = self.sheet2.cell_value (8, 2)
        uid = self.sheet2.cell_value (8, 4)
        cityid = self.sheet2.cell_value (8, 5)
        timestamp = self.common_method.timestamp
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
        response = requests.get (base_url, params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertNotEqual (result["data"]["items"],[])

    def test_subscribe(self):
        u"测试关注零售商"
        retail_search = get_Retails(self)
        retail_result = json.loads(retail_search.content)
        base_url = self.sheet2.cell_value(9,2)
        uid =  self.sheet2.cell_value (9, 4)
        retailid = ""
        if retail_result["data"]["retails"] !=[]:
            for retails in retail_result["data"]["retails"]:
                if retails["subscribe"] ==2 :                #为1是已关注，为2是未关注
                    retailid = retails["retailId"]
                    break
            params = {
                "userid" :uid,
                "retailid" : retailid,
                "type" :1,                                  #1是关注，2是取消关注
                "appversion" :self.common_method.version,
                "os" :self.common_method.os,
                "timestamp" :self.common_method.timestamp,
                "devcode" :self.common_method.devcode
            }
            response = requests.get(base_url,params=params)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertEqual (result["data"], None)
            #检查我的关注列表是否有该零售商
            canMatch = False
            response_subscribe = self.common_method.get_mySubscribeList(uid)
            result_subscribe = json.loads(response_subscribe.content)
            for subscribeList in result_subscribe["data"]["subscribeList"]:
                if subscribeList["retailId"] == retailid:
                    canMatch = True
                    break
            self.assertTrue(canMatch)
        else:
            self.assertEqual(retail_result["msg"],"零售商列表查询失败")

    def test_cancleSubscribe(self):
        u"测试取消零售商"
        uid = self.sheet2.cell_value (10, 4),
        response_subscribe = self.common_method.get_mySubscribeList(uid)                 # 获取我的已关注列表
        result_subscribe = json.loads (response_subscribe.content)
        base_url = self.sheet2.cell_value(10,2)
        if result_subscribe["data"]["subscribeList"] !=[]:
            retailid = result_subscribe["data"]["subscribeList"][0]["retailId"]
            params = {
                "userid" :uid,
                "retailid" : retailid,
                "type" :2,                                              #1是关注，2是取消关注
                "appversion" :self.common_method.version,
                "os" :self.common_method.os,
                "timestamp" :self.common_method.timestamp,
                "devcode" :self.common_method.devcode
            }
            response = requests.get(base_url,params=params)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertEqual (result["data"], None)
            #检查我的关注列表是否有该零售商
            canMatch = True
            response_subscribe = self.common_method.get_mySubscribeList(uid)
            result_subscribe = json.loads(response_subscribe.content)
            for subscribeList in result_subscribe["data"]["subscribeList"]:
                if subscribeList["retailId"] == retailid:
                    canMatch = False
                    break
            self.assertTrue(canMatch)
        else:
            self.assertEqual(result_subscribe["msg"],"没有已关注的零售商，无法取消已关注零售商")

        '''
        @edit:cjiangym
        @time:2017-11-22
        '''
    def test_storehomePromotion(self):
        u"测试首页猜你喜欢促销信息"
        '''从excel表中获取接口地址'''
        base_url = self.sheet2.cell_value(11,2)
        userid = self.sheet2.cell_value(11,4)
        timestamp = self.common_method.timestamp
        list_key = [userid,timestamp]
        key = Key.get_key(self,list_key)
        params = {
            "appversion" : self.common_method.version,
            "cityid" : self.sheet2.cell_value(11,5),
            "devcode" : self.common_method.devcode,
            "subscribe" :0,
            "key" : key,
            "lon" : self.sheet2.cell_value(11,6),
            "lat" : self.sheet2.cell_value(11,7),
            "nextpage" :"" ,
            "os" :self.common_method.os,
            "timestamp": timestamp,
            "userid" : userid
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual (result["data"],"null")
        self.assertNotEqual(result["data"]["retails"],[])

    def test_retailPromotion(self):
        u"测试获取促销优惠列表"
        base_url = self.sheet2.cell_value(12,2)
        userid = self.sheet2.cell_value(12,4)
        timestamp = self.common_method.timestamp
        key_list = [userid,timestamp]
        key = Key.get_key(self,key_list)
        params = {
            "districtid":-2,
            "appversion": self.common_method.version,
            "cityid": self.sheet2.cell_value (12, 5),
            "devcode": self.common_method.devcode,
            "key": key,
            "lon": self.sheet2.cell_value (12, 6),
            "lat": self.sheet2.cell_value (12, 7),
            "nextpage": "",
            "os": self.common_method.os,
            "timestamp": timestamp,
            "userid": userid,
            "retailid":-1,
            "townid":-2,
            "distance":"",
            "shoptypeid":-1
        }
        response = requests.get (base_url, params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual (result["data"], "null")
        self.assertNotEqual (result["data"]["retails"],[])




