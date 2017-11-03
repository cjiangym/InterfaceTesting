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

    def exchangeGift(self,userid,giftid,gift_type):
        u"测试兑换礼品"
        base_url = self.sheet1.cell_value(27,2)
        uid = userid
        giftId = giftid
        giftType = gift_type
        if gift_type == "1":
            contactNumber = self.sheet1.cell_value(27,7)
            buyNumber =  self.sheet1.cell_value (27,8)
            key_list = [giftId,giftType,contactNumber,uid,buyNumber]
            key = self.common_method.get_key(key_list)
            params = {
                "uid": uid,
                "giftId": giftId,
                "contactPerson": self.sheet1.cell_value (27, 6),
                "contactNumber": contactNumber,
                "buyNumber": buyNumber,
                "province": self.sheet1.cell_value (27, 9),
                "province_id": self.sheet1.cell_value (27, 10),
                "city": self.sheet1.cell_value (27, 11),
                "city_id": self.sheet1.cell_value (27, 12),
                "district": self.sheet1.cell_value (27, 13),
                "district_id": self.sheet1.cell_value (27, 14),
                "town": self.sheet1.cell_value (27, 15),
                "town_id": self.sheet1.cell_value (27, 16),
                "deliveryAddress": self.sheet1.cell_value (27, 17),
                "address" : self.sheet1.cell_value(27,18),
                "giftType" : giftType,
                "key" : key
            }
        else:
            contactNumber = self.sheet1.cell_value (28, 6)
            buyNumber = self.sheet1.cell_value (28,7)
            key_list = [giftId, giftType, contactNumber, uid, buyNumber]
            key = self.common_method.get_key (key_list)
            params = {
                "buyNumber": buyNumber,
                "contactNumber": contactNumber,
                "giftId": giftId,
                "giftType": giftType,
                "uid": uid,
                "key" :key
            }
        response = requests.get(base_url,params=params)
        return response

    def test_exchangeGift_01(self):
        u"测试正常礼品兑换 - 实物礼品"
        uid = self.sheet1.cell_value(27,4)
        giftid = self.sheet1.cell_value(27,5)
        gift_type = "1"        #实物礼品
        response = self.exchangeGift(uid,giftid,gift_type)
        if response.status_code ==200:
            result = json.loads(response.content)
            if result["data"]:
                self.assertEqual(result["status"],10001)
                gift_numbet = result["data"]["giftnumber"]
                self.assertNotEqual(result["data"]["giftnumber"],None)
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(response.status_code,200)

    def test_exchangeGift_02(self):
        u"测试正常礼品兑换 - 虚拟礼品"
        uid = self.sheet1.cell_value (28, 4)
        giftid = self.sheet1.cell_value (28, 5)
        gift_type = "2"                               # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            if result["data"]:
                self.assertEqual (result["status"], 10001)
                gift_numbet = result["data"]["giftnumber"]
                self.assertNotEqual (result["data"]["giftnumber"], None)
            else:
                self.assertEqual (result["msg"], 0)
        else:
            self.assertEqual (response.status_code, 200)

    def test_exchangeGift_03(self):
        u"测试异常礼品兑换 - 库存不足"
        uid = self.sheet1.cell_value (27, 4)
        giftid = self.sheet1.cell_value (29, 4)
        gift_type = "2"                               # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            self.assertEqual(result["data"],None)
            self.assertEqual (result["status"], 20004)
            self.assertEqual (result["msg"], "礼品已经兑换完啦")



