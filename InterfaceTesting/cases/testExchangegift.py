import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from InterfaceTesting.run_all_cases import Common_method

class ExchangegiftTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()

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

    def test_exchangeGift(self):
        u"测试兑换礼品"
        base_url = self.sheet1.cell_value(27,2)
        uid = self.sheet1.cell_value(27,4)
        giftId = self.sheet1.cell_value(27,5)
        params = {
            "address" : self.sheet1.cell_value(),
            "giftType" : "1",
            "city_id" : self.sheet1.cell_value(),
            "contactNumber" : self.sheet1.cell_value(),
            "city" :self.sheet1.cell_value(),
            "buyNumber" : self.sheet1.cell_value(),
            "timestamp" : self.sheet1.cell_value(),
            "province_id" : self.sheet1.cell_value(),
            "province" : self.sheet1.cell_value(),
            "district_id" :self.sheet1.cell_value(),
            "os" : self.sheet1.cell_value(),
            "deliveryAddress" :self.sheet1.cell_value(),
            "devcode" : self.sheet1.cell_value(),
            "town_id" : self.sheet1.cell_value(),
            "contactPerson" :self.sheet1.cell_value(),
            "town" :self.sheet1.cell_value()
            "key" :
            "giftId":self.sheet1.cell_value()
            "district" :self.sheet1.cell_value()
            "uid" :
        }

