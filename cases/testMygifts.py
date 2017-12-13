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


class MygiftsTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def gift_exchange(self):
        pass

    def test_subjectGiftList(self):
        u"测试查询兑换专区礼品"
        base_url = self.sheet1.cell_value(25,2)
        uid = self.sheet1.cell_value(25,4)
        if isinstance(uid,float):
            uid = str(math.floor(uid))
        params = {
            "uid" :uid,
            "timestamp" : self.common_method.timestamp,
            "appversion" :self.common_method.version,
            "os" :self.common_method.os,
            "devcode" : self.common_method.devcode
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["subjectGiftList"][0]["subjects"][0]["subjectName"],"爆款抢兑")

    def test_categoryGiftList(self):
        u"测试查询品类礼品"
        base_url = self.sheet1.cell_value (26, 2)
        uid = self.sheet1.cell_value (26, 4)
        if isinstance (uid, float):
            uid = str (math.floor (uid))
        params = {
            "uid": uid,
            "timestamp": self.common_method.timestamp,
            "appversion": self.common_method.version,
            "os": self.common_method.os,
            "devcode": self.common_method.devcode
        }
        response = requests.get (base_url, params=params)
        result = json.loads (response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual(len(result["data"]["categoryGiftList"]),0)

    def get_mygiftsList(self):
        base_url = self.sheet1.cell_value(39,2)
        params = {
            "appversion" :self.common_method.version,
            "devcode" :self.common_method.devcode,
            "giftType" :"1",          #只能传1或者2，且二者无区别
            "os" : self.common_method.os,
            "pageSize": "30",
            "pages" : "1",
            "uid" : self.sheet1.cell_value(39,4)
        }
        response_mygifts = requests.get(base_url,params=params)
        return  response_mygifts

    def test_mygiftsList(self):
        u"测试我的兑换列表"
        response = self.get_mygiftsList()
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        print(result)

    def test_giftDetail(self):
        u"测试已兑换的礼品详情"
        base_url = self.sheet1.cell_value(40,2)
        response_giftList = self.get_mygiftsList()
        self.assertEqual(response_giftList.status_code,200)
        result_giftList = json.loads(response_giftList.content)
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
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["giftdetail"]["giftNumber"],giftnum)