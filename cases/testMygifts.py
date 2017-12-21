import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.getKey import Key
from  config import  serverAddressConfig


class MygiftsTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    svrAddr = serverAddressConfig.sv_29090

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def gift_exchange(self):
        pass

    def test_subjectGiftList(self):
        u"测试查询兑换专区礼品"
        base_url = self.sheet1.cell_value(25,2)
        url = self.svrAddr + base_url
        uid = self.sheet1.cell_value(25,4)
        params = {
            "uid" :uid,
            "timestamp" : serverAddressConfig.timestamp,
            "appversion" :serverAddressConfig.version,
            "os" :serverAddressConfig.os,
            "devcode" : serverAddressConfig.devcode
        }
        response = requests.get(url,params=params)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual(result["data"]["subjectGiftList"],[])

    def test_categoryGiftList(self):
        u"测试查询品类礼品"
        base_url = self.sheet1.cell_value (26, 2)
        url = self.svrAddr + base_url
        uid = self.sheet1.cell_value (26, 4)
        if isinstance (uid, float):
            uid = str (math.floor (uid))
        params = {
            "uid": uid,
            "timestamp": serverAddressConfig.timestamp,
            "appversion": serverAddressConfig.version,
            "os": serverAddressConfig.os,
            "devcode": serverAddressConfig.devcode
        }
        response = requests.get (url, params=params)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual(result["data"]["categoryGiftList"],[])

    def get_mygiftsList(self):
        base_url = self.sheet1.cell_value(39,2)
        url = self.svrAddr + base_url
        params = {
            "appversion" :serverAddressConfig.version,
            "devcode" :serverAddressConfig.devcode,
            "giftType" :"1",          #只能传1或者2，且二者无区别
            "os" : serverAddressConfig.os,
            "pageSize": "30",
            "pages" : "1",
            "uid" : self.sheet1.cell_value(39,4)
        }
        response_mygifts = requests.get(url,params=params)
        return  response_mygifts

    def test_mygiftsList(self):
        u"测试我的兑换列表"
        try:
            self.response = self.get_mygiftsList()
        except:
            self.assertTrue(None,"我的兑换列表查询失败")
        self.assertEqual(self.response.status_code,200)
        result = json.loads(self.response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual (result["data"],{})

    def test_giftDetail(self):
        u"测试已兑换的礼品详情"
        base_url = self.sheet1.cell_value(40,2)
        url = self.svrAddr + base_url
        try:
            self.response_giftList = self.get_mygiftsList()
        except:
            self.assertTrue(None,"我的兑换列表查询失败")
        result_giftList = json.loads(self.response_giftList.content)
        if result_giftList["data"]["userGiftList"]:
            uid = self.sheet1.cell_value (39, 4)
            giftnum = result_giftList["data"]["userGiftList"][0]["giftNumber"]
        else:
            uid = "784"
            giftnum = "171107000120"
        list_key = [uid,giftnum]
        key = Key.get_key(self,list_key)
        params = {
            "userid" : uid,
            "giftnum" : giftnum,
            "key" :key
        }
        response = requests.get(url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["giftdetail"]["giftNumber"],giftnum)