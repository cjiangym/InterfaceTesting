import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from cases.testCoupon import CouponTest

class ExchangegiftTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1()
    coupon = CouponTest()

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def gift_exchange(self):
        pass

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
                "pay_money":0,
                "couponids":"",
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
                "pay_money": 0,
                "couponids": "",
                "key" :key
            }
        response = requests.get(base_url,params=params)
        return response

    """
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
    """

    def test_exchange_03(self):
        u"测试异常礼品兑换 - 库存不足"
        uid = self.sheet1.cell_value (29, 5)
        giftid = self.sheet1.cell_value (29, 4)
        gift_type = "2"                               # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print(result)
            self.assertEqual(result["data"],{})
            self.assertEqual (result["status"], 20004)
            self.assertEqual (result["msg"], "礼品已经兑换完啦")

    def test_exchange_04(self):
        u"测试异常礼品兑换 - 支付金额不够"
        base_url = self.sheet1.cell_value (30, 2)
        uid = self.sheet1.cell_value (30, 5)
        giftid = self.sheet1.cell_value (30, 4)
        gift_type ="2"
        contactNumber = "13450244170"
        buyNumber = "1"
        key_list = [giftid, gift_type, contactNumber, uid, buyNumber]
        key = self.common_method.get_key (key_list)
        params = {
            "uid": uid,
            "giftId": giftid,
            "contactPerson": "测试",
            "contactNumber": contactNumber,
            "buyNumber": buyNumber,
            "province": "广东",
            "province_id": "6",
            "city": "广州",
            "city_id": "76",
            "district": "天河区",
            "district_id": "1613",
            "town": "五山",
            "town_id": "10753",
            "deliveryAddress": "广东广州天河区五山",
            "address": "乐天创意园",
            "giftType": gift_type,
            "pay_money": 7.98,
            "couponids":"03dCrSJ6G+4=",
            "key": key
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        self.assertEqual(result["status"],20001)
        self.assertEqual(result["msg"],"金额不匹配")

    def test_exchange_05(self):
        u"测试异常礼品兑换 - 优惠券id有误"
        base_url = self.sheet1.cell_value (30, 2)
        uid = self.sheet1.cell_value (30, 5)
        giftid = self.sheet1.cell_value (30, 4)
        gift_type = "1"
        contactNumber = "13450244170"
        buyNumber = "1"
        key_list = [giftid, gift_type, contactNumber, uid, buyNumber]
        key = self.common_method.get_key (key_list)
        params = {
            "uid": uid,
            "giftId": giftid,
            "contactPerson": "测试",
            "contactNumber": contactNumber,
            "buyNumber": buyNumber,
            "province": "广东",
            "province_id": "6",
            "city": "广州",
            "city_id": "76",
            "district": "天河区",
            "district_id": "1613",
            "town": "五山",
            "town_id": "10753",
            "deliveryAddress": "广东广州天河区五山",
            "address": "乐天创意园",
            "giftType": gift_type,
            "pay_money": 4,
            "couponids": "abcjoeur",
            "key": key
        }
        response = requests.get (base_url, params=params)
        result = json.loads (response.content)
        self.assertEqual(result["msg"],"下单失败，请稍后重试")
    '''
    def test_coupon_exchange(self):
        u"测试条码兑换"
        pass
    '''
    def test_exchange_06(self):
        u"测试异常礼品兑换 - 精明豆不够"
        uid = self.sheet1.cell_value (31, 5)
        giftid = self.sheet1.cell_value (31, 4)
        gift_type = "1"  # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual (result["data"], {})
            self.assertEqual (result["status"], 20003)
            self.assertEqual (result["msg"], "哎呀~精明豆不够，兑换失败")

    def test_exchange_07(self):
        u"测试异常礼品兑换 - 礼品未上线"
        uid = self.sheet1.cell_value (32, 5)
        giftid = self.sheet1.cell_value (32, 4)
        gift_type = "1"  # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual (result["data"], {})
            self.assertEqual (result["status"], 20001)
            self.assertEqual (result["msg"], "该礼品已下架啦")

    def test_exchange_08(self):
        u"测试异常礼品兑换 - 礼品已过期"
        uid = self.sheet1.cell_value (33, 5)
        giftid = self.sheet1.cell_value (33, 4)
        gift_type = "1"  # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual (result["data"], {})
            self.assertEqual (result["status"], 20001)
            self.assertEqual (result["msg"], "该礼品已下架啦")

    def test_exchange_09(self):
        u"测试异常礼品兑换 - 礼品暂停使用"
        uid = self.sheet1.cell_value (34, 5)
        giftid = self.sheet1.cell_value (34, 4)
        gift_type = "1"  # 虚拟礼品
        response = self.exchangeGift (uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual (result["data"], {})
            self.assertEqual (result["status"], 20001)
            self.assertEqual (result["msg"], "该礼品已下架啦")

    def test_exchange_10(self):
        u"测试异常礼品兑换 - 等级不够"
        uid = self.sheet1.cell_value (35,5)
        giftid = self.sheet1.cell_value (35, 4)
        gift_type = "1"           # 实物礼品，2虚拟礼品
        response = self.exchangeGift(uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual (result["data"], {})
            self.assertEqual (result["status"], 20004)
            self.assertEqual (result["msg"], "该商品需要V2及以上才能兑换哦，赶紧去升级吧")

    def test_exchange_11(self):
        u"测试异常礼品兑换 - 不在规定时间内注册"
        uid = self.sheet1.cell_value (36,5)
        giftid = self.sheet1.cell_value (36, 4)
        gift_type = "1"           # 实物礼品，2虚拟礼品
        response = self.exchangeGift(uid, giftid, gift_type)
        if response.status_code == 200:
            result = json.loads (response.content)
            print (result)
            self.assertEqual(result["data"], {})
            self.assertEqual(result["status"], 20004)
            self.assertEqual(result["msg"], "您不符合兑换条件哦")


